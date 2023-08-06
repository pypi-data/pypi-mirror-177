import requests
from os.path import join
from ds4biz_commons.utils.dict_utils import ObjectDict


def application_json(response):
    return response.json()

def html_text(response):
    return response.text

def content(response):
    return response.content

def object_dict(response):
    return ObjectDict(response.json())


class URLRequest:
    def __init__(self,base,response_converter=application_json,request_converter=None,**kwargs):
        self.request_converter = request_converter
        self.__base = base
        self.kwargs = kwargs
        self.response_converter = response_converter
    
    def __getattr__(self,path):
        return URLRequest(join(self.__base,path),self.response_converter,self.request_converter,**self.kwargs)
    
    def __getitem__(self,path):
        return URLRequest(join(self.__base,path),self.response_converter,self.request_converter,**self.kwargs)

    def __str__(self):
        return "URLRequest: %s"%self.__base
    
    def __repr__(self):
        return "URLRequest: %s"%self.__base
    
    
    def __call__(self,**kwargs):
        if "json" in kwargs:
            return self.post(**kwargs)
            
        return self.get(**kwargs)
    
    def _check_and_return(self,response):
        response.raise_for_status()
        if self.response_converter:
            return self.response_converter(response)
        else:
            return response
    
    def get(self,**kwargs):
        args=dict(self.kwargs,**kwargs)
        
        resp = requests.get(self.__base,**args)
        return self._check_and_return(resp)
    
    def post(self,**kwargs):
        args=dict(self.kwargs,**kwargs)
        if "json" in args and self.request_converter:
            args['json']=self.request_converter(args['json'])
        resp = requests.post(self.__base,**args)
        return self._check_and_return(resp)

    def put(self,**kwargs):
        args=dict(self.kwargs,**kwargs)
        if "json" in args and self.request_converter:
            args['json']=self.request_converter(args['json'])
        resp = requests.put(self.__base,**args)
        return self._check_and_return(resp)

    def delete(self,**kwargs):
        args=dict(self.kwargs,**kwargs)
        resp = requests.delete(self.__base,**args)
        return self._check_and_return(resp)
    
    def get_base(self):
        return self.__base
    
    def __setstate__(self, state):
        self.__dict__ = state

    def __getstate__(self):
        return self.__dict__
