# description like this
# abc
# 123

#import numpy as np

# recommended, imports everything as hb2
# like this , need to make via functions
import helloworldbasic4message.utility2 as hb4

# also recommended imports specifics
from helloworldbasic4message.utility2 import SomeClass as SomeClassExtra
from helloworldbasic4message.utility2 import somefunction











# in the implmetation call a=hb5.getSomeClass(2)
# or a=hb5.SomeClass(2)

def getSomeClass(v):
    return hb4.SomeClass(v)

def do_somefunction(x):
    return hb4.somefunction(x)




def test101():
    #hb2.utilB_saygoodbye("abc")

    print("test 101")
    a=hb4.SomeClass(208)
    hb4.somefunction(a)
    return 1


def test102():
    print("test 102")
    b=SomeClassExtra(3)
    hb4.somefunction(b)
    return 1

def test103():
    print("test 103")
    d=SomeClassExtra(14)
    print("type=",type(d) )
    somefunction(d)
    return 1




def test201():
    l=np.array([100,200])
    return l




def saygreeting(name):
    return hb4.utilA_sayhello(name)


test103()










