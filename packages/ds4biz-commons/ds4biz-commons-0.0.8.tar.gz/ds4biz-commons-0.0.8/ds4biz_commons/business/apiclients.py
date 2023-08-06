from ds4biz_commons.utils.requests_utils import URLRequest, object_dict,\
    application_json
import os
from urllib.parse import urlparse
from _collections import defaultdict
from distutils.version import LooseVersion
        
class ApiClient(URLRequest):
    def __init__(self,url="http://localhost:8080/swagger.json",response_converter=application_json,**kwargs):  
        self.url = url
        u=URLRequest(url,response_converter=object_dict)
        self.swagger=u()
        t=Trie()
        tt=defaultdict(dict)
        for el in self.swagger.paths:
            fp=os.path.join(self.swagger.basePath,el.strip("/"))
            t.insert(fp.split("/"))
            for m in self.swagger.paths[el]:
                summary=self.swagger.paths[el][m].summary
                tt[fp][m]={"summary":summary,"parameters":self.swagger.paths[el][m].parameters}
            
        lp=longest_prefix(t)
        lps="/".join(lp).strip("/")
        
        pp=urlparse(url)
        super().__init__("{u.scheme}://{u.netloc}/{lps}".format(u=pp,lps=lps),response_converter,**kwargs)
        self.mapping={}
        for el in trie_ending_tokens(t):
            k=".".join(el[len(lp):])
            info=tt["/".join(el)]
            for kk,vv in info.items():
                pars=[]
                for x in vv['parameters']:
                    if x.type:
                        pars.append((x.name,x))
                    if x.schema:
                        sch=x.schema['$ref'] or x.schema['type']
                        pars.append((x.name,sch))
                        
                self.mapping[k,kk.upper()]=vv['summary']+", parameters %s"%pars
            #self.mapping[el[-1]]=multiple_keys(temp,el)
            
        
    def docs(self):
        return list(self.mapping.items())
    
    def definitions(self):
        for k,v in self.swagger.definitions.items():
            yield k,v
        
        
class Trie:
    def __init__(self):
        self.children = {}
        self.seq_end=False
    
    def insert(self,el_list):
        if el_list:
            head=el_list[0]
            if not head in self.children:
                self.children[head]=Trie()
            self.children[head].insert(el_list[1:])
        else:
            self.seq_end=True
        return self
    def __repr__(self):
        return str(self.children)

def trie_ending_tokens(t,acc=[]):
    if t.seq_end:
        yield list(acc)
    for c,v in t.children.items():
        for el in trie_ending_tokens(v, acc+[c]):
            yield el

def longest_prefix(t):
    n=len(t.children)
    if n==0 or n>1:
        return []
    else:
        k=next(iter(t.children.keys()))
        return [k]+longest_prefix(t.children[k])

        
class DockerRegistry:
    """A client for docker v2 registry"""
    def __init__(self,url,auth=None):
        self.r = URLRequest(url,auth=auth,response_converter=object_dict).v2
        
    def all(self):
        """Retrieve all repositories names"""
        
        return self.r._catalog().repositories
    
    def tags(self,repo,include_dev=True):
        """Retrieve all tags for a given repo"""
        temp=self.r[repo].tags.list().tags
        if not include_dev:
            temp= [x for x in temp if not x.endswith("-dev")]
        
        return sorted(temp,key=LooseVersion,reverse=True)

        
    