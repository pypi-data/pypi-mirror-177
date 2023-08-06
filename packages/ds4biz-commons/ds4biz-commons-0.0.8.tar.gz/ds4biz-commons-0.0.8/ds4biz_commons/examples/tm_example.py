from ds4biz_commons.model.taskmanagement import TaskManager, Task

def f(a,b):
    ret=[]
    while True:
        ret.append("a")
    print(a+b)


tm=TaskManager(workers=8,logger=print)

tm.submit(task=Task("a", f, (10,20), mem=2**30,t=1))

tm.shutdown()