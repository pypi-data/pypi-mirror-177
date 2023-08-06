class BaseFactory:
    def __init__(self,klass="__klass__"):
        self.klass = klass
        self.transformers={}
    
    def register(self,name,transformer):
        self.transformers[name]=transformer
        
    def __call__(self,obj):
        if isinstance(obj, dict):
            if self.klass in obj:
                kl=obj[self.klass]
                args=self({k:self(v) for (k,v) in obj.items() if k!=self.klass})
                if isinstance(kl, type) or callable(kl):
                    return kl(**args)
                else:
                    return self.transformers[kl](**args)
            else:
                for k,v in obj.items():
                    return {k:self(v) for (k,v) in obj.items()}
        if isinstance(obj, list):
            return [self(v) for v in obj]
        
        if isinstance(obj, tuple):
            return (self(v) for v in obj)
        
        return obj
    

class BaseTransformer:
    def __init__(self,typefun=type):
        self.typefun = typefun
        self.transformers={}
        
    def __call__(self,obj):
        if isinstance(obj, dict):
            return {k:self(v) for (k,v) in obj.items()}
        elif isinstance(obj, (list,tuple)):
            return obj.__class__(self(x) for x in obj)
        else:
            typ=self.typefun(obj)
            if typ in self.transformers:
                return self.transformers[typ](obj)
            else:
                return obj
    def register(self,k,fun):
        self.transformers[k]=fun