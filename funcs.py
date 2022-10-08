from lexer import *


def print_func(x):
    if x.type==TOKENS["identifier"]:
        print(VARS[x.value]["value"].value,end="")
    else:
        print(x.value,end="")
        
    


funcs={"print":{"builtin":True,"key":print_func}}

