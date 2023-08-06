from multiprocessing import Process,SimpleQueue
import signal
import resource
import threading
import logging



def timeout_handler(signum, frame):
    raise TimeoutError("Timeout")


class Task:
    def __init__(self,name,f,args,mem=None,t=None):        
        self.name = name
        self.f = f
        self.args = args
        self.mem = mem
        self.t = t
        
    def start(self,q):
        p=Process(target=self,args=(q,))
        p.start()
        return p
    def __call__(self,q):
        if self.mem:
            resource.setrlimit(resource.RLIMIT_AS,(self.mem,self.mem))
        if self.t:
            
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(self.t)
        try:
            
            res=self.f(*self.args)
            q.put((self.name,res,0))
        except MemoryError as e:
            
            q.put((self.name,None,TaskException("Memory error")))
        except TimeoutError as e:
            q.put((self.name,None,TaskException("Timeout error")))
        except Exception as e:
            q.put((self.name,None,e))
            

class TaskException(Exception):
    pass

class TaskManager:
    def __init__(self,workers=8,logger=logging.debug):
        self.logger = logger
        self.workers = workers
        self.tasks={}
        self.queue=SimpleQueue()
        threading.Thread(target=self.dequeue).start()
        self._shutdown=False
        self.waiting={}
        
    def submit(self,task:Task):
        if task.name in self.tasks:
            raise Exception("Task already exists "+task.name)
        
        if len(self.tasks)>self.workers:
            self.waiting[task.name]=task
        else:
            self.tasks[task.name]=task.start(self.queue)
        
    def dequeue(self):
        while True:
            try:
                res=self.queue.get()
                del self.tasks[res[0]]
                self.logger(res)
                if self._shutdown and not self.tasks and not self.waiting:
                    return
                if len(self.tasks)<self.workers and self.waiting:
                    self.submit(self.waiting.pop(next(iter(self.waiting.keys()))))
            except Exception as inst:
                logging.error(inst)
                                
    def cancel(self,name):
        if name in self.tasks:
            self.tasks[name].terminate()
            self.queue.put((name,None,TaskException("Terminated")))
        elif name in self.waiting:
            del self.waiting[name]
            self.queue.put((name,None,TaskException("Canceled")))

    def shutdown(self):
        self._shutdown=True


