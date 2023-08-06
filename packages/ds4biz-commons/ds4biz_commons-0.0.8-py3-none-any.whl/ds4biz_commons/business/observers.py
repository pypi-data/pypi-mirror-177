import logging

logger=logging.getLogger(__name__)

class Observable(object):
    
    def __init__(self,*observers):
        self.observers=list(observers)
    
    def add_observer(self,observer):
        self.observers.append(observer)
    
    def notify(self,msg):
        for o in self.observer:
            try:
                o(msg)
            except Exception as inst:
                logger.exception(inst)
                
                
