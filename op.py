from genericpath import isfile
from classes import *
from lexer import *

def rshift_op(a,b):
    c=a.value>>b.value
    return Token(c.__class__.__name__,c,a.line_start,b.line_end)

def lshift_op(a,b):
    c=a.value<<b.value
    return Token(c.__class__.__name__,c,a.line_start,b.line_end)

def pow_op(a,b):
    c=a.value**b.value
    return Token(c.__class__.__name__,c,a.line_start,b.line_end)

def mul_op(a,b):
    c=a.value*b.value
    return Token(c.__class__.__name__,c,a.line_start,b.line_end)

def div_op(a,b):
    if b.value==0:
        return Error(a.start_line,b.end_line,"division by 0",None)
    c=a.value/b.value
    return Token(c.__class__.__name__,c,a.line_start,b.line_end)

def euclidiv_op(a,b):
    if b.value==0:
        return Error(a.start_line,b.end_line,"division by 0",None)
    c=a.value//b.value
    return Token(c.__class__.__name__,c,a.line_start,b.line_end)

def mod_op(a,b):
    if b.value==0:
        return Error(a.start_line,b.end_line,"modulo by 0",None)
    c=a.value%b.value
    return Token(c.__class__.__name__,c,a.line_start,b.line_end)

def add_op(a:Token,b:Token,t:list,idx):
    if a!=None and b!=None and not(a.isTok()) and not(b.isTok()):
        t.pop(idx+1)
        t.pop(idx)
        c=a.value+b.value
        t[idx-1]=Token(c.__class__.__name__,c,a.line_start,b.line_end)
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
        if type(a)==Null:
            t.pop(idx-1)
    elif b!=None and a==None and b.type==TOKENS["+"]:
        t.pop(idx+1)   
        if type(a)==Null:
            t.pop(idx-1)
    else:
        return Error(t[idx].line_start,t[idx].line_end,"error in expression",None)
    
def min_op(a:Token,b:Token,t:list,idx):
    if a!=None and b!=None and not(a.isTok()) and not(b.isTok()):
        t.pop(idx+1)
        t.pop(idx)
        c=a.value-b.value
        t[idx-1]=Token(c.__class__.__name__,c,a.line_start,b.line_end)
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
        c=-t[idx+1].value
        t[idx]=Token(c.__class__.__name__,c,a.line_start,b.line_end)
        t.pop(idx+1)
        if type(a)==Null:
            t.pop(idx-1)
    elif b!=None and a==None and b.type==TOKENS["+"]:
        t.pop(idx+1)   
        t[idx]=Token(TOKENS["+"],None,t[idx].line_start,t[idx].line_end)
        if type(a)==Null:
            t.pop(idx-1)
    else:
        return Error(t[idx].line_start,t[idx].line_end,"error in expression",None)

def eq_op(a,b):
    c=boolean(a.value==b.value)
    return Token(c.__class__.__name__,c,a.line_start,b.line_end)

def gt_op(a,b):
    c=boolean(a.value>b.value)
    return Token(c.__class__.__name__,c,a.line_start,b.line_end)

def and_op(a,b):
    c=boolean(a.value and b.value)
    return Token(c.__class__.__name__,c,a.line_start,b.line_end)

def or_op(a,b):
    c=boolean(a.value or b.value)
    return Token(c.__class__.__name__,c,a.line_start,b.line_end)




