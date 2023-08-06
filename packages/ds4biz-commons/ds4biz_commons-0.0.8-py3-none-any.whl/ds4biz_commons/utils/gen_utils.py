import json
import re
import hashlib
from urllib.parse import urlparse
from tempfile import NamedTemporaryFile, TemporaryFile
import time
import os


def slugify(obj,char="_",expr="[^a-zA-Z0-9]+"):
    slug=re.sub(expr,char,str(obj))
    return slug.strip(char)


def object_hash(obj):
    m = hashlib.sha256()
    if hasattr(obj, "__getstate__"):
        m.update(json.dumps(obj.__getstate__()).encode())
    else:
        m.update(str(obj).encode())
    return m.digest()


def get_host(url):
    parse=urlparse(url)
    return "{u.scheme}://{u.netloc}/".format(u=parse)


def stream_copy(source,dest,chunk_size=2**20,):
    while True:
        buffer=source.read(chunk_size)
        if buffer:
            dest.write(buffer)
            dest.flush()
            
        else:
            return

def find_file(name:str,path=".",recursive=True):
    """It returns the absolute path of a file. If recursive is True it searches in all the parents directories"""
    p=os.path.join(path,name)
    if os.path.exists(p):
        return p
    else:
        if recursive and path!="/":
            return find_file(name,os.path.dirname(os.path.abspath(path)))
        else:
            raise FileNotFoundError("File %s not found (in parent directories)"%name)

class TempFile:
    def __init__(self,stream,chunk_size=2**20,**kwargs):
        self.stream = stream
        self.kwargs = kwargs
        self.chunk_size = chunk_size
        
    def __enter__(self):
        self.file=TemporaryFile(**self.kwargs)
        stream_copy(self.stream, self.file)
        self.file.seek(0)
        return self.file
    
    def __exit__(self,exc, value, tb):
        result = self.file.__exit__(exc, value, tb)
        self.file.close()
        return result


if __name__=="__main__":
    print(find_file("dao/serializers.py"))