from lexer import *
from classes import *


def print_func(x):
    if type(x)==list:
        for i in x:
            print_func(i)
    
    elif x.type==TOKENS["identifier"] and x.value in VARS.keys():
        print(VARS[x.value]["value"].value,end="")
    else:
        print(x.value,end="")
    return Null()
        
def input_func(x):
    return Token("string",string(input()))

def ount_conv(k):
    x=k
    if type(k)!=Token:
        x=k[0]
    return Token("ount",ount(int(str(x.value))),x.line_start,x.line_end)

def string_conv(k):
    x=k
    if type(k)!=Token:
        x=k[0]
    return Token("string",string(x.value),x.line_start,x.line_end)
    
def open_window(x):
    if x!=None:
        return False
    print("pourquoi")

funcs={"print":{"builtin":True,"key":print_func},
                            "input":{"builtin":True,"key":input_func},
                            "ount_conv":{"builtin":True,"key":ount_conv},
                            "string_conv":{"builtin":True,"key":string_conv},
                            "open_window":{"builtin":True,"key":open_window}
       }

