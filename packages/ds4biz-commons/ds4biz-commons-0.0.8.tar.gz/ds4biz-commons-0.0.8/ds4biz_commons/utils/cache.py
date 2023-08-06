import os
from functools import wraps
import dill
import hashlib
import time
import tempfile
import logging
from pathlib import Path
import inspect
from ds4biz_commons.dao.serializers import DillFSSerializer


logger=logging.getLogger(__name__)

def slug(data):
    return hashlib.md5(dill.dumps(data)).hexdigest()


tempdir=Path.home()/".cache"/"ds4biz"

class FSCache:
    def __init__(self,path=tempdir,key_function=slug):
        self.path = path
        self.key_function = key_function
        self.serializer = DillFSSerializer()
        os.makedirs(path, exist_ok=True)
        
        
    def __call__(self,f):
        @wraps(f)
        def temp(*args,**kwargs):
            fn=os.path.join(self.path,self.key_function((inspect.getsource(f),args,kwargs))) 
            if fn in self:
                logger.debug("Hitting cache for %s with args %s %s"%(f,args,kwargs))
                return self.serializer.load(fn)
            else:
                ret=f(*args,**kwargs)
                self.serializer.save(fn, ret)
                return ret
        return temp
    
    def __contains__(self,key):
        return os.path.exists(key)
        

class ExecutionTimeFSCache:
    def __init__(self,path=tempdir,t=5):
        self.path = path
        self.t = t
    
    def __call__(self,f):
        @wraps(f)
        def temp(*args,**kwargs):
            fn=os.path.join(self.path,slug((inspect.getsource(f),args,kwargs))) 
            if os.path.exists(fn):
                with open(fn,"rb") as o:
                    return dill.load(o)
            else:
                temp=time.time()
                ret=f(*args,**kwargs)
                elapsed=time.time()-temp
                if elapsed>self.t:
                    with open(fn,"wb") as o:
                        dill.dump(ret,o)
                return ret
        return temp


class WatchableFile:
    def __init__(self,path):
        self.path = path
        self.mtime=os.path.getmtime(self.path)
    


if __name__=="__main__":
    @ExecutionTimeFSCache(t=.3)
    def f(a,b):
        time.sleep(.5)
        return a+b
    
    for i in range(10):
        print(f(i,i))