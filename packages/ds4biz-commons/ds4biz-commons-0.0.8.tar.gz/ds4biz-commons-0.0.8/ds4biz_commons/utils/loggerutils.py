import logging
from ds4biz_commons.utils.requests_utils import URLRequest
import re
from typing import Dict


BASE_FORMAT='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d  - %(message)s'
DATE_FORMAT='%d-%m-%Y:%H:%M:%S'


class LoggerManager:
    def __init__(self,format=BASE_FORMAT):        
        self.format = format
        logging.basicConfig(format=self.format,level=logging.ERROR)
        
    def filter(self,name_regex=None):
        if name_regex==None:
            yield logging.root
        else:
            temp=logging.root.manager.loggerDict  # @UndefinedVariable
            
            for name in temp:
                if re.fullmatch(name_regex,name):
                    log=logging.getLogger(name)
                    yield log
    
    def config(self,levels:Dict[str,str]):
        for k,v in levels.items():
            for log in self.filter(k):
                log.setLevel(getattr(logging, v))


if __name__=="__main__":
    lm=LoggerManager()
    
    logger=logging.getLogger(__name__)
    lm.config({"__main__":"DEBUG"})
    #print(logging.root.manager.loggerDict['urllib3'].setLevel(logging.ERROR))
    
    u=URLRequest("https://distribution.livetech.site")
    
    logger.debug(u())
    
        
