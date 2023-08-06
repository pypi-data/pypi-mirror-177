from ds4biz_commons.business.sampling import Values, DictValues, Calls
v=Values(1,2,3)

def f(a,b,c=2):
    return a+b+c

for el in Calls(f,a=Values(v,v),b=2,c=Values(*range(5))):
    print(el)