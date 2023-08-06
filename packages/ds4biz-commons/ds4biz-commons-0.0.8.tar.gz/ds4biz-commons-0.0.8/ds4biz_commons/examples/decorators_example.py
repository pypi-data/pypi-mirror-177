from ds4biz_commons.business.decorators import TimerLogger, FunctionLogger,\
    ExceptionRaiser, ExceptionCatcher, Retry


#TimerLogger automatically 
@TimerLogger(print)
def f(a,b):
    return a+b


class A:
    @TimerLogger(print)
    @FunctionLogger(print)
    def name(self,n):
        return "Fulvio"

print(f(2,4))
print(A().name("Giorgio"))

def g(a):
    return a*5

print(TimerLogger(print)(g)(10))
    
    
@Retry(10)
@ExceptionRaiser(.99)
def exc(a):
    return a

print(exc("a"))