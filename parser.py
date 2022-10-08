import os
from  lexer import *
import sys
from funcs import *
from op import *
from  classes import *

def findPar(t,left_idx):
    c=0
    for i in range(left_idx+1,len(t)):
        if t[i].type==TOKENS["("]:c+=1
        elif t[i].type==TOKENS[")"] and c>0:c-=1
        elif t[i].type==TOKENS[")"] and c==0:return i

class Parser:
    def __init__(self,tokens,fn):
        self.tokens=tokens
        self.ptr=0
        self.fn=fn
        
    def makeExpr(self,t):
        tok_expr=[]
        p=0
        while p<len(t):
            if t[p].type==TOKENS["identifier"]:
                name=t[p].value
                if p+1<len(t) and t[p+1].type==TOKENS["("]:
                    left=p+1
                    right=findPar(t,left)
                    if right==None:return Error(left,left,"'(' was never closed",self.fn)
                    a=[]
                    for i in range(left+1,right):
                        a.append(t[i])
                    tok_expr.append(FuncCall(name,self.makeExpr(a)))
                    p=right+1
                else:
                    tok_expr.append(t[p])
                    p+=1
            elif t[p].type==TOKENS["("]:
                left=p
                right=findPar(t,left)      
                if right==None:return Error(left,left,"'(' was never closed",self.fn)
                a=[]
                for i in range(left+1,right):
                        a.append(t[i])
                tok_expr.append(Expr(self.makeExpr(a)))
                p=right+1
            else:
                tok_expr.append(t[p])
                p+=1   
        return tok_expr
    
    def findBestOp(self,t):
        for i in range(len(t)):#scan for pow(^)
            if t[i].type==TOKENS["^"]:
                return i
        for i in range(len(t)):#scan for MUL DIV MOD EUCLIDIVE(* / % //)
            if t[i].type in [TOKENS["*"],TOKENS["/"],TOKENS["%"],TOKENS["//"]]:
                return i
        for i in range(len(t)):
            if t[i].type in [TOKENS["+"],TOKENS["-"]]:
                return i
        for i in range(len(t)):#scan for logic operation 
            if t[i].type in LOGICOP:
                return i
        return None
    
    def evalExpr(self,expr:Expr):
        for i in range(len(expr.tok)):
            if isinstance(expr.tok[i],Expr):
                expr.tok[i]=self.evalExpr(expr.tok[i])
        
        op=self.findBestOp(expr.tok)
        if op ==None:
            if len(expr.tok)==1:
                return expr.tok[0]
            else:
                return Error(None,None,"error in expression",self.fn)
        elif expr.tok[op].type==TOKENS["^"]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                return Error(op,op,"Error in expression : missing parameter for ^ (pow) operator ",self.fn)
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=pow_op(a,b)
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
        elif expr.tok[op].type==TOKENS["*"]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                return Error(op,op,"Error in expression : missing parameter for * (mul) operator ",self.fn)
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=mul_op(a,b)
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
        elif expr.tok[op].type==TOKENS["/"]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                return Error(op,op,"Error in expression : missing parameter for / (div) operator ",self.fn)
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=div_op(a,b)
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
        elif expr.tok[op].type==TOKENS["%"]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                return Error(op,op,"Error in expression : missing parameter for / (div) operator ",self.fn)
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=mod_op(a,b)
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
        elif expr.tok[op].type==TOKENS["//"]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                return Error(op,op,"Error in expression : missing parameter for / (div) operator ",self.fn)
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=euclidiv_op(a,b)
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
        elif expr.tok[op].type==TOKENS["+"]:
            a=None
            b=None
            if op+1<len(expr.tok):
                b=expr.tok[op+1]
            if op-1>=0:
                a=expr.tok[op-1]
            if b==None:return Error(None,None,"error in expression",self.fn)
            c=add_op(a,b,expr.tok,op)
        elif expr.tok[op].type==TOKENS["-"]:
            a=None
            b=None
            if op+1<len(expr.tok):
                b=expr.tok[op+1]
            if op-1>=0:
                a=expr.tok[op-1]
            if b==None:return Error(None,None,"error in expression",self.fn)
            c=min_op(a,b,expr.tok,op)
        return self.evalExpr(expr)
        
                    
                
                
        
    def parse(self):
        global VARS
        while self.ptr<len(self.tokens):
            if self.tokens[self.ptr].type in TYPES:
                if self.ptr+3<len(self.tokens):#Type Identifer Eq Expr
                    if self.tokens[self.ptr].type in TYPES and self.tokens[self.ptr+1].type==TOKENS["identifier"] and self.tokens[self.ptr+2].type==TOKENS["="]:
                        name=self.tokens[self.ptr+1]
                        name_idx=self.ptr+1
                        type_=self.tokens[self.ptr]
                        self.ptr+=3
                        e=[]
                        semi=None
                        for i in range(name_idx+2,len(self.tokens)):
                            if self.tokens[i].type==TOKENS[";"]:semi=i;break
                            e.append(self.tokens[i])
                        if semi==None:
                            return Error(name_idx,None,"missing ';' ",self.fn)
                        val=self.evalExpr(Expr(self.makeExpr(e)))
                        if isinstance(val,Error):return val
                        VARS[name.value]={"name":name,"type":type_,"value":val}
                        self.ptr=semi+1
            elif self.tokens[self.ptr].type==TOKENS["identifier"]:
                name=self.tokens[self.ptr]
                if self.ptr+2<len(self.tokens):
                    l=self.ptr+1
                    r=findPar(self.tokens,l)
                    if r==None:
                        return Error(l,l,"'(' was never closed",self.fn)
                    e=[]
                    for i in range(l+1,r):
                        e.append(self.tokens[i])
                    e=self.makeExpr(e)
                    val=self.evalExpr(Expr(e))
                    funcs["print"]["key"](val )
                    self.ptr=r+1

            else:
                self.ptr+=1       
     
############################
#RUN

def run(fn,text):
    lexer=Lexer(fn,text)
    tokens=lexer.make_tokens()
    parser=Parser(tokens,fn)
    a=parser.parse()
run("stdio","""
    print(3)
    string a ="salut";
    print(a)
    """)