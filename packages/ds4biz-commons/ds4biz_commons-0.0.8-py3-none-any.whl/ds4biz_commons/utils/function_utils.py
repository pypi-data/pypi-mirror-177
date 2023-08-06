import inspect
from _collections import defaultdict
import random

def myall(x,functions):
    for f in functions:
        if not f(x):
            return False
    return True

def condition(cc):
    if isinstance(cc, list):
        return lambda x:myall(x,cc)
    elif isinstance(cc, set):
        return lambda x:any([condition(c)(x) for c in cc])
    else:
        return cc

def getfunctions(obj,conditions=None):
    conditions=conditions or []
    for el in inspect.getmembers(obj, condition([inspect.isfunction]+conditions)):
        yield obj,el
    if inspect.isclass(obj):
        return
    for name,kl in inspect.getmembers(obj, inspect.isclass):
        yield from getfunctions(kl, conditions)

def partition(list,condition):
    a,b=[],[]
    for el in list:
        if condition(el):
            a.append(el)
        else:
            b.append(el)
    return a,b


class CondNode:
    def __init__(self,f=lambda x:True,action=None):    
        self.f = f
        self.action = action
        self.children={}
        
    def add(self,funs,action):
        if not funs:
            return
        
        else:
            n=funs.pop(0)
            if n not in self.children:
                self.children[n]=CondNode(n,None)
            if not funs:
                self.children[n].action=action
            else:
                self.children[n].add(funs,action)
            return self.children[n]
    def __call__(self,obj):
        if self.f(obj):
            flag=False
            for n in self.children.values():
                actions=n(obj)
                for action in actions:
                    if callable(action):
                        yield action(obj)
                    else:
                        yield action
                    flag=True
            if not flag:
                if callable(self.action):
                    yield self.action(obj)
                else:
                    yield self.action


def shuffled(it,shuffle=random.shuffle):
    ret=list(it)
    shuffle(ret)
    return ret

if __name__=="__main__":        
    c=CondNode()
    n=c.add([lambda x:len(x)<10], "CIAO")
      
    n.add([lambda x:x.startswith("s")],"SSSS")          
    n.add([lambda x:x.endswith("s")],"ENDSSSS")          
    for el in c("asaaasasa"):
        print(el)
    
    for el in shuffled(range(10)):
        print(el)
