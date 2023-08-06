from abc import abstractmethod
import itertools
import random
import logging
from ds4biz_commons.utils.function_utils import partition
import functools

class Options:
    @abstractmethod
    def __iter__(self):
        pass
    
    @abstractmethod
    def choice(self):
        pass
    
    def sample(self,n):
        for i in range(n):
            try:
                yield self.choice()
            except Exception as inst:
                logging.exception(inst)
    
    

class Values(Options):
    def __init__(self,*args):
        self.args = args
        
    def __iter__(self):
        for el in self.args:
            if isinstance(el, Options):
                for x in el:
                    yield x
            else:
                yield el
    def choice(self):
        temp=random.choice(self.args)
        while isinstance(temp, Options):
            temp=temp.choice()
        return temp



class DictValues(Options):
    def __init__(self,**kwargs):                
        self.kwargs = kwargs
    
    def __iter__(self):
        opts,fixed=partition(list(self.kwargs.items()), lambda x:isinstance(x[1],Options))
        for el in itertools.product(*[x[1] for x in opts]):
            temp=dict(zip((x[0] for x in opts),el))
            for k,v in fixed:
                temp[k]=v
            yield temp
    def choice(self):
        ret={}
        for k,v in self.kwargs.items():
            if isinstance(v, Options):
                ret[k]=v.choice()
            else:
                ret[k]=v
        return ret


class TupleValues(Options):
    def __init__(self,*args):    
        self.args = args
        
    def __iter__(self):
        temp=[]
        for arg in self.args:
            if not isinstance(arg, Options):
                temp.append(Values(arg))
            else:
                temp.append(arg)
        yield from itertools.product(*temp)
                
    def choice(self):
        ret=[]
        for v in self.args:
            if isinstance(v, Options):
                ret.append(v.choice())
            else:
                ret.append(v)
        return tuple(ret)
    
    
class CallObject:
    def __init__(self,f,**kwargs):
        self.f = f
        self.kwargs = kwargs
        
    def __call__(self):
        rkwargs={}
        for k,v in self.kwargs.items():
            if isinstance(v,CallObject):
                rkwargs[k]=v()
            else:
                rkwargs[k]=v
        return self.f(**rkwargs)
    
    def __str__(self):
        return str((self.f,self.kwargs))

    def __repr__(self):
        return str((self.f,self.kwargs))

"""class Calls(Options):
    def __init__(self,fun,**kwargs):
        self.fun = fun
        self.kwargs = kwargs

    def __iter__(self):
        for kwargs in DictValues(**self.kwargs):
            try:
                yield CallObject(self.fun,**kwargs)
            except Exception as inst:
                logging.exception(inst)    
    
    def choice(self):
        return CallObject(self.fun,**DictValues(**self.kwargs).choice())"""

class Calls(Options):
    def __init__(self,*funs,**kwargs):
        self.funs = Values(*funs)
        self.kwargs = kwargs

    def __iter__(self):
        for kwargs in DictValues(**self.kwargs):
            try:
                for f in self.funs:
                    print(f)
                    yield CallObject(f,**kwargs)
            except Exception as inst:
                logging.exception(inst)    
    
    def choice(self):
        return CallObject(self.funs.choice(),**DictValues(**self.kwargs).choice())
    
    
def fun2calls(f):
    @functools.wraps(f)
    def temp(**kwargs):
        return Calls(f,**kwargs)
    return temp


def to_dict_values(o):
    if isinstance(o, dict):
        return DictValues(**{k:to_dict_values(v) for (k,v) in o.items()})
    else:
        return o

def resolve(o):    
    if isinstance(o, dict):
        return {k:resolve(v) for (k,v) in o.items()}
    elif isinstance(o,CallObject):
        return o()
    elif callable(o):
        return o()
    else:
        return o

