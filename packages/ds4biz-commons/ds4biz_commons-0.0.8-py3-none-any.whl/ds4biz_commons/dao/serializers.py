import dill
import os


class FSSerializer:
    def load(self,path):
        raise Exception("Not implemented")
    def save(self,path,obj):
        raise Exception("Not implemented")
    
    
class DillFSSerializer(FSSerializer):
    def load(self, path):
        with open(path,"rb") as f:
            obj=dill.load(f)
            return obj
    def save(self,path,obj):
        with open(path, "wb") as dill_file:
            dill.dump(obj, dill_file)
            

class DillDirectorySerializer(FSSerializer):
    def load(self, path):
        dd=os.path.join(path,"content")
        with open(dd,"rb") as f:
            obj=dill.load(f)
            return obj
    def save(self,path,obj):
        if not os.path.exists(path):
            os.makedirs(path)
        path=os.path.join(path,"content")
        with open(path, "wb") as dill_file:
            dill.dump(obj, dill_file)

