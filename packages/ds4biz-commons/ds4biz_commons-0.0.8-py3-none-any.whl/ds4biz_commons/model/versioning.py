import datetime
import json
import shutil
from copy import deepcopy
from glob import glob

from ds4biz_commons.utils.gen_utils import object_hash
from ds4biz_commons.dao.serializers import DillFSSerializer
import os


class VersionedObject:

    def commit(self):
        raise Exception("Not implemented!")

    def checkout(self, branch):
        raise Exception("Not implemented!")

    def current(self):
        raise Exception("Not implemented!")

    def _uncommitted(self):
        raise Exception("Not implemented!")

    def substitute(self, branch):
        raise Exception("Not implemented!")

    def tag(self, tag_name):
        raise Exception("Not implemented!")

    def get_branches(self):
        raise Exception("Not implemented!")

    def get_tags(self):
        raise Exception("Not implemented!")

    def delete_repository(self):
        raise Exception("Not implemented!")

    def delete_branch(self, branch):
        raise Exception("Not implemented!")

    def lock(self):
        raise Exception("Not implemented!")

    def unlock(self):
        raise Exception("Not implemented!")

    def __is_locked(self, branch):
        raise Exception("Not implemented!")


class MemoryVersionedObject(VersionedObject):
    def __init__(self, object, title="", description=""):
        self.tags = {}
        self.current_branch = "master"
        self.branches = {"master": deepcopy(object)}
        self.locked_branches = set()
        self.metadata = {"title": title, "description": description}
        self.wk = deepcopy(object)

    def __call__(self):
        return self.wk

    def commit(self):
        if self.__is_locked(self.current()):
            raise Exception("Couldn't commit on branch {}: locked".format(self.current()))

        # if current branch is a tag, it can't be commited because tags are immutable
        if self.current() in self.get_tags():
            # reloading of the precedent state
            self.wk = deepcopy(self.tags[self.current()])
            raise Exception("Cannot commit a tagged branch: tags are immutable")

        self.metadata.update({"Last commit": "Branch {} at {}".format(self.current(), datetime.datetime.now())})
        self.branches[self.current()] = deepcopy(self.wk)
        return self

    def checkout(self, branch):
        if self.current() in self.branches and self._uncommitted():
            raise Exception("Working copy on branch %s contains uncommitted changes. "
                            "You should commit them before switching to branch %s" % (self.current(), branch))

        if branch not in self.branches and branch not in self.get_tags():
            self.branches[branch] = deepcopy(self.branches[self.current()])

        if branch in self.get_tags():
            self.current_branch = branch
            self.wk = deepcopy(self.tags[self.current()])

        if branch in self.get_branches():
            self.current_branch = branch
            self.wk = deepcopy(self.branches[self.current()])
        return self

    def current(self):
        return self.current_branch

    def _uncommitted(self):
        return object_hash(self.wk) != object_hash(self.branches[self.current()])

    def substitute(self, branch):
        if self.__is_locked(self.current()):
            raise Exception("Couldn't merge branch {}: locked".format(self.current()))
        if self.current() in self.get_tags():
            self.wk = deepcopy(self.tags[self.current()])
            raise Exception("Cannot merge a tagged branch: tags are immutable")
        # if self._uncommitted():
        #     raise Exception("Commit your changes before merging")

        if branch not in self.branches:
            raise Exception("Branch doesn't exist")

        self.branches[self.current()] = deepcopy(self.branches[branch])
        self.wk = deepcopy(self.branches[branch])

        return self

    def tag(self, tag):
        if self._uncommitted():
            raise Exception("Commit your changes before tagging")
        if tag in self.get_branches():
            raise Exception("Tag cannot have the same name of a branch")
        if tag in self.get_tags():
            raise Exception("Tag already exists")
        self.tags[tag] = deepcopy(self())
        return self

    def get_branches(self):
        return list(self.branches.keys())

    def get_tags(self):
        return list(self.tags.keys())

    def delete_repository(self):
        del self.tags
        del self.current_branch
        del self.branches
        del self.metadata
        del self.locked_branches
        del self.wk
        del self

    def delete_branch(self, branch):
        if branch not in self.get_branches() and branch not in self.get_tags():
            raise Exception("Branch doesn't exists")

        if self.__is_locked(branch):
            raise Exception("Couldn't delete branch {}: locked".format(branch))

        if branch == self.current():
            raise Exception("Couldn't delete current branch {}: checkout first".format(branch))

        del self.branches[branch]

    def lock(self):
        self.locked_branches.add(self.current())

    def unlock(self):
        self.locked_branches.remove(self.current())

    def __is_locked(self, branch):
        if branch not in self.get_branches() and branch not in self.get_tags():
            raise Exception("Branch doesn't exists")
        if branch in list(self.locked_branches):
            return True
        else:
            return False


class FSVersionedObject(VersionedObject):
    def __init__(self, path, object=None, serializer=DillFSSerializer(), title="", description=""):
        self.path = path
        self.serializer = serializer
        self.current_branch = "master"
        target = os.path.join(self.path, self.current())

        # Check if a repository with master branch already exists.
        # In negative case, the system builds the filesystem and save the serialized
        # object given in input to the constructor
        if "master" not in self.get_branches():
            self.__create_fs(target)
            # if object is None, an empty dictionary is save in filesystem
            if object is None:
                raise Exception("An object must be passed in input to newly created versioned object")
            else:
                self.serializer.save(os.path.join(target, "content"), object)
                self.wk = deepcopy(object)

        # In positive case, the system loads in memory the serialized object of the master branch.
        # If another object is passed in input to the constructor, the system raises an exception
        else:
            if object is not None:
                raise Exception("Cannot load passed object because an object associated to path {}, "
                                "with branch {}, already exists".format(self.path, self.current()))
            object = self.serializer.load(os.path.join(target, "content"))
            self.wk = deepcopy(object)

        # creation of metadata json file if not exists
        info_file_path = os.path.join(self.path, "metadata.json")
        if not os.path.exists(info_file_path):
            dict_object = dict(title=title, description=description)
            file_object = open(os.path.join(self.path, "metadata.json"), 'w')
            json.dump(dict_object, file_object)

    def __call__(self):
        return self.wk

    def __create_fs(self, target, branch=True):
        # auxiliary method to handle the creation of folders with files to indentify if branch is tagged or not
        os.makedirs(target, exist_ok=True)
        type_path = os.path.join(target, ".branch")
        if not os.path.exists(type_path):
            if branch:
                f = open(os.path.join(target, ".branch"), "w")
            else:
                f = open(os.path.join(target, ".tag"), "w")
            f.close()

    def commit(self):
        if self.__is_locked(self.current()):
            raise Exception("Couldn't commit on branch {}: locked".format(self.current()))

        target = os.path.join(self.path, self.current())
        # if current branch is a tag, it can't be commited because tags are immutable
        if self.current() in self.get_tags():
            # reloading of the precedent state
            self.wk = deepcopy(self.serializer.load(os.path.join(target, "content")))
            raise Exception("Cannot commit a tagged branch: tags are immutable")
            #return self
        self.__create_fs(target)
        self.serializer.save(os.path.join(target, "content"), deepcopy(self.wk))

        # update metadata json file with informations about last commit
        info_file_path = os.path.join(self.path, "metadata.json")
        with open(info_file_path, 'r') as f:
            dict_info = json.loads(f.read())
            dict_info.update({"Last commit": "Branch {} at {}".format(self.current(), datetime.datetime.now())})
            file_object = open(info_file_path, 'w')
            json.dump(dict_info, file_object)
        return self

    def checkout(self, branch):
        if self.current() in self.get_branches() and self._uncommitted():
            raise Exception("Working copy on branch %s contains uncommitted changes. "
                            "You should commit them before switching to branch %s" % (self.current(), branch))

        target = os.path.join(self.path, branch)

        # if checking-out new branch, it must be created from the current one
        if branch not in self.get_branches() and branch not in self.get_tags():
            self.__create_fs(target)
            self.serializer.save(os.path.join(target, "content"), self.wk)

        self.current_branch = branch
        obj = self.serializer.load(os.path.join(target, "content"))
        self.wk = deepcopy(obj)
        return self

    def current(self):
        return self.current_branch

    def _uncommitted(self):
        target = os.path.join(self.path, self.current())
        obj = self.serializer.load(os.path.join(target, "content"))
        return object_hash(self.wk) != object_hash(obj)

    def substitute(self, branch):
        # Method the merge the actual branch with the one passed in input
        merged_path = os.path.join(self.path, self.current())
        if self.__is_locked(self.current()):
            raise Exception("Couldn't merge branch {}: locked".format(self.current()))

        if self.current() in self.get_tags():
            self.wk = deepcopy(self.serializer.load(os.path.join(merged_path, "content")))
            raise Exception("Cannot merge a tagged branch: tags are immutable")

        if branch not in self.get_branches() and branch not in self.get_tags():
            raise Exception("Branch doesn't exist")

        merging_path = os.path.join(self.path, branch)
        obj = self.serializer.load(os.path.join(merging_path, "content"))
        self.wk = deepcopy(obj)
        self.serializer.save(os.path.join(merged_path, "content"), deepcopy(self.wk))
        return self

    def tag(self, tag):
        if self._uncommitted():
            raise Exception("Commit your changes before tagging")
        if tag in self.get_branches():
            raise Exception("Tag cannot have the same name of a branch")
        if tag in self.get_tags():
            raise Exception("Tag already exists")
        target = os.path.join(self.path, tag)
        self.__create_fs(target, branch=False)
        self.serializer.save(os.path.join(target, "content"), deepcopy(self.wk))
        return self

    def get_branches(self):
        branches = [p.split("/")[-2] for p in glob(os.path.join(self.path, "*", ".branch"))]
        return branches

    def get_tags(self):
        tags = [p.split("/")[-2] for p in glob(os.path.join(self.path, "*", ".tag"))]
        return tags

    def delete_repository(self):

        branches = self.get_branches()
        if any([br for br in branches if self.__is_locked(br)]):
            raise Exception("Couldn't delete repository because one or more branches are locked")
        shutil.rmtree(self.path)
        del self.path
        del self.serializer
        del self.current_branch
        del self.wk

    def delete_branch(self, branch):
        if branch not in self.get_branches() and branch not in self.get_tags():
            raise Exception("Branch doesn't exists")

        if self.__is_locked(branch):
            raise Exception("Couldn't delete branch {}: locked".format(branch))

        if branch == self.current():
            raise Exception("Couldn't delete current branch {}: checkout first".format(branch))

        shutil.rmtree(os.path.join(self.path, branch))

    def lock(self):
        target = os.path.join(self.path, self.current())
        lock_file = os.path.join(target, ".lock")
        if os.path.exists(lock_file):
            raise Exception("Branch {} already locked".format(self.current()))

        f = open(lock_file, "w")
        f.close()

    def unlock(self):

        target = os.path.join(self.path, self.current())
        lock_file = os.path.join(target, ".lock")
        if not os.path.exists(lock_file):
            # raise Exception("Branch {} already unlocked".format(branch))
            return
        os.remove(lock_file)

    def __is_locked(self, branch):
        if branch not in self.get_branches() and branch not in self.get_tags():
            raise Exception("Branch doesn't exists")

        if os.path.exists(os.path.join(self.path, branch, ".lock")):
            return True
        else:
            return False


if __name__ == "__main__":

    # vo = VersionedObject({})
    # vo.checkout("development")()["name"] = "Fulvio"
    # print(vo())
    # vo.commit()
    # print(vo.checkout("master")())
    # print(vo.checkout("development")())
    # vo()["name"] = "Cico"
    # vo.commit()
    # print(vo.checkout("master")())
    # vo.checkout("pippo").merge("development")()["name"] = "Marco"
    # vo.commit()
    # print(vo.checkout("master").merge("pippo")())
    # print(vo.branches)
    
    # print(vo.checkout("master").merge("development").tag("1.0")())
    # print(vo.branches,vo.tags)

    path = "/home/marco/Desktop/prova-versioning"

    # vo = FSVersionedObject(path)
    # print("Branches:", vo.get_branches())
    # print("Tags:", vo.get_tags())
    # vo.checkout("development")()["name"] = "Fulvio"
    # print("development: ", vo())
    # vo.commit()
    # print("master: ", vo.checkout("master")())
    # vo.merge("development")()
    # print("master mergiato con development", vo())
    # vo.tag("1.0")
    # print("Tag 1.0", vo())
    # vo.checkout("1.0")
    # vo()["name"] = "Marco"
    # try:
    #     vo.commit()
    # except Exception as e:
    #     print(str(e))
    # print("Tentativo di commit sul tag 1.0", vo())
    #
    # vo.checkout("development")()["name"] = "Cristiano"
    # vo.commit()
    #
    # try:
    #     vo.checkout("1.0").merge("development")
    # except Exception as e:
    #     print(str(e))
    # print("Tentativo di merge sul tag 1.0", vo())
    #
    # vo.checkout("development")
    # print("Development: ", vo())

    # vo = FSVersionedObject(path)
    # print("Branches:", vo.get_branches())
    # print("Tags:", vo.get_tags())
    # vo.checkout("development")()["name"] = "Fulvio"
    # vo.commit()
    # print("development: ", vo())
    #
    # vo.checkout("master")
    # vo.lock()
    # print("Master: ", vo())
    # vo.checkout("development")
    # vo.checkout("master")
    # vo()["surname"] = "marco"
    # vo.commit()
    # print("Master: ", vo())
    # print("master: ", vo.checkout("master")())
    # print("mio: ", vo.checkout("mio")())
    # print("mio mergiato con development: ", vo.merge("development")())
    # print("developement2 che dovrebbe essere uguale a mio   : ", vo.checkout("development2")())

    # vo = FSVersionedObject(path)
    # vo.delete_repository()
    # print(vo)
    # print(vo.get_branches())

    vo = MemoryVersionedObject({"name": "Marco", "surname": "Coluzza"}, title="prova_repo", description="descrizione di prova")
    print("Branches:", vo.get_branches())
    print("Tags:", vo.get_tags())
    print("master: ", vo())
    vo.checkout("development")()["name"] = "Fulvio"
    vo.commit()
    print("development: ", vo())

    vo.checkout("master")
    vo.lock()
    print("Master: ", vo())
    vo.checkout("development")
    vo.checkout("master")
    vo.unlock()
    vo()["surname"] = "Vota"
    vo.commit()
    print("Master: ", vo())
    print("metadati: ", vo.metadata)

    vo.checkout("pippo")
    print("pippo: ", vo())
    print("pippo mergiato con developmente", vo.substitute("development")())
    vo.tag("1.0")
    print("1.0: ", vo.checkout("1.0")())
    vo()["name"] = "Cristiano"
    try:
        vo.substitute("master")
    except Exception as e:
        print(str(e))
    print("1.0: ", vo())