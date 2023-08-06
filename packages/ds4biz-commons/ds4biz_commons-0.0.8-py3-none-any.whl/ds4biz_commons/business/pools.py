"""
A  module to simplify the execution of functions through a pool (ThreadPoolExecutor, ProcessPoolExecutor, etc.)
"""
import functools
from concurrent.futures._base import as_completed

class Pooler:
    def __init__(self,pool):
        self.pool = pool
        self.data=[]
        
    def __call__(self,f):
        """This function wraps an existing function and executes with a pool
        """
        @functools.wraps(f)
        def temp(*args,**kwargs):
            future=self.pool.submit(f,*args,**kwargs)
            self.data.append(future)
            return future
        return temp
    
    def __iter__(self):
        """Iterate over the results"""
        return as_completed(self.data)
    
    def reset(self):
        self.data=[]
