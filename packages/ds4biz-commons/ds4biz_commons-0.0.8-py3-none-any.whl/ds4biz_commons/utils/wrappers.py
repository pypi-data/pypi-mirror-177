from functools import wraps
import logging

class FunctionWrapper:
    def __init__(self,logfun=logging.debug):
        self.logfun = logfun
    def pre(self,f,args,kwargs):
        pass
    def post(self,f,args,kwargs,pre_result,ret):
        pass
    
    def __call__(self,f):
        @wraps(f)
        def wrapper(*args,**kwargs):
            pre_result = self.pre(f,args,kwargs)
            ret=f(*args,**kwargs)
            self.post(f,args,kwargs,pre_result,ret)
            return ret
        return wrapper
    
