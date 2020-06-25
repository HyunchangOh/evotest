hctest={}
hclocals={}
class InfiniteLoopException(Exception):
    pass
def function1(a):

    global hclocals
    hctest['1.1']=False
    if a>10:
        hctest['1.1']=True
        a+=1
    else:
        hclocals['0'] =locals()
        return a


    hclocals['0'] = locals()
def function2(b):

    global hclocals
    hctest['1.2']=False
    if b<0:
        hctest['1.2']=True
        b-=1
    hclocals['0'] =locals()
    return b
    hclocals['0'] = locals()
