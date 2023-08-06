from ds4biz_commons.utils.wrappers import FunctionWrapper
import time
from typing import Callable, Union
import logging
import random
from functools import wraps
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import TimeoutError
import functools
from ds4biz_commons.utils.function_utils import getfunctions
from ds4biz_commons.config import AppConfig

class FunctionLogger(FunctionWrapper):
    """Logs the arguments of a function call and the result"""
    
    def pre(self, f, args, kwargs):
        self.logfun("Executing %s with args %s %s"%(f.__qualname__,args,kwargs))

    def post(self, f, args, kwargs,pre_result,ret):
        self.logfun("%s executed with args %s %s Result %s"%(f.__qualname__,args,kwargs,ret))




class TimerLogger(FunctionWrapper):
    """Logs the execution time of a function"""
    
    def pre(self, f, args, kwargs):
        return time.time()
    
    def post(self, f, args, kwargs, pre_result, ret):
        
        elapsed=time.time()-pre_result
        
        self.logfun("%s: Elapsed time %f seconds"%(f.__qualname__,elapsed))
        return elapsed


class Delay(FunctionWrapper):
    """Delays the function by a given amount of time. 
    
    * delay: number of seconds or a zero-argument caller (e.g. lambda:random.random()*5 will randomly delay a function in [0,5] seconds)
    """
    def __init__(self,delay:Union[float,Callable] = 1.0,logfun=logging.debug):
        super().__init__(logfun)
        self.delay=delay
        
    def pre(self, f, args, kwargs):
        if callable(self.delay):
            t=self.delay()
        else:
            t=self.delay
        self.logfun("Delaying %s %f seconds"%(f.__name__,t))
        time.sleep(t)

class ExceptionRaiser(FunctionWrapper):
    """ Raise an exception with a given probability. Useful for debugging purposes"""        
    def __init__(self,probability=1.0,message = "Unexpected exception!",exception=Exception,logfun=logging.debug):
        super().__init__(logfun)
        self.message = message
        self.exception = exception
        self.probability = probability

    def pre(self, f, args, kwargs):
        toss=random.random()
        if toss<=self.probability:
            raise self.exception(self.message)

class ExceptionCatcher:
    def __init__(self,logfun=logging.error):
        self.logfun=logfun
        
    def __call__(self,f):
        @functools.wraps(f)
        def temp(*args,**kwargs):
            try:
                return f(*args,**kwargs)
            except Exception as inst:
                self.logfun(inst)
            return None
        return temp

    

class TimeLimiter:
    def __init__(self,timeout,logfun=logging.debug):
        self.timeout = timeout
        self.logfun = logfun
    def __call__(self,f):
        @wraps(f)
        def temp(*args,**kwargs):
            pool=ThreadPoolExecutor()
            ret=pool.submit(f,*args,**kwargs)
            pool.shutdown(wait=False)
            try:
                return ret.result(self.timeout)
            except TimeoutError as err:
                raise Exception("%s function with args %s,%s has exceeded timeout of %f seconds"%(f.__name__,args,kwargs,self.timeout))
        return temp



class Retry:
    """If the function execution fails it tries to call it again up to n times"""
    def __init__(self,n,logfun=logging.debug):
        self.logfun=logfun
        self.n = n

    def __call__(self,f):
        @functools.wraps(f)
        def temp(*args,**kwargs):
            for i in range(self.n):
                self.logfun("tentative %d for function %s with args %s %s"%(i+1,f.__name__,args,kwargs))
                try:
                    return f(*args,**kwargs)
                except Exception as inst:
                    self.logfun("Failed: %s"%inst)
            raise Exception("Failed after %d tries for function %s with args %s %s"%(self.n,f.__name__,args,kwargs))
            
        return temp


class WrapperChain(FunctionWrapper):
    """Chaining multiple decorators and using them as a single one"""
    def __init__(self,*wrappers):
        self.wrappers = wrappers
    def __call__(self,f):
        ret=f
        for wrapper in self.wrappers[::-1]:
            ret=wrapper(ret)
        
        return ret

    

def decorate(obj,conditions,decorators,verbose=True):
    
    for container,(name,f) in getfunctions(obj, conditions):
        if verbose:
            AppConfig.logger.info("Decorating",name,"in",container.__name__)
        temp=f
        for dec in decorators:
            temp=dec(temp)
        setattr(container, name, temp)


if __name__=="__main__":
    
    import logging
    logger = logging.getLogger(__name__)
    logging.basicConfig()
    logger.setLevel(logging.DEBUG)
    lf=logger.debug
    
    wc=WrapperChain(TimerLogger(lf),Retry(200,lf),ExceptionRaiser(.99,message="Pretty sick"))
    
    #@TimerLogger(lf)
    #@FunctionLogger(lf)
    #@Delay(3,logfun=lf)
    @wc
    def f(a,b):
        return a+b
    f(1,3)
    