from genericpath import isfile
from lexer import *

def pow_op(a,b):
    return Token("int",a.value**b.value)

def mul_op(a,b):
    print('a',a,b,"waaaa")
    return Token("int",a.value*b.value)

def div_op(a,b):
    if b.value==0:
        return Error(None,None,"division by 0",None)
    return Token("int",a.value/b.value)

def euclidiv_op(a,b):
    if b.value==0:
        return Error(None,None,"division by 0",None)
    return Token("int",a.value % b.value)

def mod_op(a,b):
    return a.value%b.value

def add_op(a:Token,b:Token,t:list,idx):
    if a!=None and b!=None and not(a.isTok()) and not(b.isTok()):
        t.pop(idx+1)
        t.pop(idx)
        t[idx-1]=Token("int", a.value+b.value)
    elif a!=None and b!=None and not(a.isTok()) and b.type==TOKENS["+"]:
        t.pop(idx+1)
    elif a!=None and b!=None and a.type==TOKENS["+"] and not(b.isTok()):
        t.pop(idx-1)
    elif a!=None and b!=None and a.type==TOKENS["+"] and b.type==TOKENS["+"]:
        t.pop(idx+1)
        t.pop(idx)
    elif b!=None and a==None and not(b.isTok()):
        t[idx]=t[idx+1]
        t.pop(idx+1)
    elif b!=None and a==None and b.type==TOKENS["+"]:
        t.pop(idx+1)   
    else:
        return Error(None,None,"error in expression",None)
    
def min_op(a:Token,b:Token,t:list,idx):
    if a!=None and b!=None and not(a.isTok()) and not(b.isTok()):
        t.pop(idx+1)
        t.pop(idx)
        t[idx-1]=Token("int", a.value-b.value)
    elif a!=None and b!=None and not(a.isTok()) and b.type==TOKENS["-"]:
        t.pop(idx+1)
        t[idx]=Token(TOKENS["+"])
    elif a!=None and b!=None and a.type==TOKENS["-"] and not(b.isTok()):
        t[idx]=Token(TOKENS["+"])
        t.pop(idx-1)
    elif a!=None and b!=None and a.type==TOKENS["-"] and b.type==TOKENS["-"]:
        t.pop(idx+1)
        t.pop(idx)
    elif b!=None and a==None and not(b.isTok()):
        t[idx]=Token("int",-t[idx+1].value)
        t.pop(idx+1)
    elif b!=None and a==None and b.type==TOKENS["+"]:
        t.pop(idx+1)   
        t[idx]=Token(TOKENS["+"])
    else:
        return Error(None,None,"error in expression",None)

    
    








