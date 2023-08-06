import importlib
import pkgutil
import inspect
from _collections import defaultdict

def import_submodules(package, recursive=True):
    """ Import all submodules of a module, recursively, including subpackages

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    if isinstance(package, str):
        try:
            package = importlib.import_module(package)
        except:
            print("Err",package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        try:
            full_name = package.__name__ + '.' + name
            results[full_name] = importlib.import_module(full_name)
            if recursive and is_pkg:
                results.update(import_submodules(full_name))
        except:
            pass
    return results

class ClassByNameLoader:
    def __init__(self,base):
        self.base = base
        self.klasses=defaultdict(set)
        
        for el,m in import_submodules(base).items():
            for name,kl in inspect.getmembers(m, inspect.isclass):
                self.klasses[name].add(kl)
                
    def find(self,name):
        prefix=None
        if "." in name:
            prefix,name=name.rsplit(".",1)
        temp=self.klasses.get(name)
        if prefix:
            return {x for x in temp if x.__module__.endswith(prefix)}
        return temp
