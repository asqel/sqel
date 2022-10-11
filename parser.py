import os
from  lexer import *
import sys
from funcs import *
from op import *
from  classes import *

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
                    if right==None:return Error(t[left].line_start,t[left].line_end,"'(' was never closed",self.fn)
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
                if right==None:return Error(t[left].line_start,t[left].line_end,"'(' was never closed",self.fn)
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
        for i in range(len(t)):
            if t[i].type in [TOKENS[">>"],TOKENS["<<"]]:
                return i
        for i in range(len(t)):#scan for logic operation 
            
            if t[i].type in LOGICOP:
                return i
        return None
    
    def evalExpr(self,expr:Expr):
        global VARS
        for i in range(len(expr.tok)):
            if isinstance(expr.tok[i],Expr):
                expr.tok[i]=self.evalExpr(expr.tok[i])
            if type(expr.tok[i])==Token and expr.tok[i].type==TOKENS["identifier"]:
                if expr.tok[i].value in VARS.keys():
                    name=expr.tok[i].value
                    expr.tok[i]=Token(VARS[name]["type"],VARS[name]["value"].value,expr.tok[i].line_start,expr.tok[i].line_end)
            if type(expr.tok[i])==FuncCall:
                if expr.tok[i].identifier in funcs.keys():
                    expr.tok[i]=funcs[expr.tok[i].identifier]["key"](self.evalExpr(Expr(expr.tok[i].args)))
        op=self.findBestOp(expr.tok)
        if op ==None:
            if len(expr.tok)==1:
                return expr.tok[0]
            elif len(expr.tok)>1:
                return Error(expr.tok[0].line_start,expr.tok[0].line_end,"error in expression",self.fn)
            else:
                return None
        elif expr.tok[op].type==TOKENS["^"]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                return Error(expr.tok[op].line_start,expr.tok[op].line_end,"Error in expression : missing parameter for ^ (pow) operator ",self.fn)
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=pow_op(a,b)
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
        elif expr.tok[op].type==TOKENS["*"]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                return Error(expr.tok[op].line_start,expr.tok[op].line_end,"Error in expression : missing parameter for * (mul) operator ",self.fn)
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=mul_op(a,b)
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
        elif expr.tok[op].type==TOKENS["/"]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                return Error(expr.tok[op].line_start,expr.tok[op].line_end,"Error in expression : missing parameter for / (div) operator ",self.fn)
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=div_op(a,b)
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
        elif expr.tok[op].type==TOKENS["%"]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                return Error(expr.tok[op].line_start,expr.tok[op].line_end,"Error in expression : missing parameter for / (div) operator ",self.fn)
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=mod_op(a,b)
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
        elif expr.tok[op].type==TOKENS["//"]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                return Error(expr.tok[op].line_start,expr.tok[op].line_end,"Error in expression : missing parameter for / (div) operator ",self.fn)
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=euclidiv_op(a,b)
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
        elif expr.tok[op].type==TOKENS[">>"]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                return Error(expr.tok[op].line_start,expr.tok[op].line_end,"Error in expression : missing parameter for / (div) operator ",self.fn)
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            if a.type==TOKENS["identifier"] and a.value in VARS.keys():a=VARS[a.value]["value"]
            if b.type==TOKENS["identifier"] and b.value in VARS.keys():b=VARS[b.value]["value"]
            c=rshift_op(a,b)
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
        elif expr.tok[op].type==TOKENS["<<"]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                return Error(expr.tok[op].line_start,expr.tok[op].line_end,"Error in expression : missing parameter for / (div) operator ",self.fn)
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=lshift_op(a,b)
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
            if b==None:return Error(expr.tok[op].line_start,expr.tok[op].line_end,"error in expression",self.fn)
            c=add_op(a,b,expr.tok,op)
        elif expr.tok[op].type==TOKENS["-"]:
            a=None
            b=None
            if op+1<len(expr.tok):
                b=expr.tok[op+1]
            if op-1>=0:
                a=expr.tok[op-1]
            if b==None:return Error(expr.tok[op].line_start,expr.tok[op].line_end,"error in expression",self.fn)
            c=min_op(a,b,expr.tok,op)
        elif expr.tok[op].type==TOKENS["=="]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                return Error(expr.tok[op].line_start,expr.tok[op].line_end,"Error in expression : missing parameter for / (div) operator ",self.fn)
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=eq_op(a,b)
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
        elif expr.tok[op].type==TOKENS[">"]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                return Error(expr.tok[op].line_start,expr.tok[op].line_end,"Error in expression : missing parameter for / (div) operator ",self.fn)
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=gt_op(a,b)
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
            
        elif expr.tok[op].type==TOKENS["<"]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                return Error(expr.tok[op].line_start,expr.tok[op].line_end,"Error in expression : missing parameter for / (div) operator ",self.fn)
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=not gt_op(a,b)
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
        
        return self.evalExpr(expr)
        
        
    def make_while(self):
        while self.ptr<len(self.tokens):
            if self.tokens[self.ptr].type==KEYWORDS["while"] and self.ptr+1<len(self.tokens):
                start=self.ptr
                l_par=self.ptr+1
                r_par=findPar(self.tokens,l_par)
                if r_par==None:return Error(self.tokens[start].line_start,self.tokens[start].line_end,"'(' was never closed",self.fn)
                e=[]
                for i in range(l_par+1,r_par):
                    e.append(self.tokens[i])
                e=Expr(self.makeExpr(e))
                if not( r_par <len(self.tokens) and self.tokens[r_par+1].type==TOKENS["{"]):
                    return Error(self.tokens[l_par].line_start,self.tokens[l_par].line_end,"error in while")
                l_brac=r_par+1
                r_brac=findPar(self.tokens,l_brac,TOKENS["{"],TOKENS["}"])
                if r_brac==None:return Error(self.tokens[l_brac].line_start,self.tokens[l_brac].line_end,"'{' was never closed",self.fn)
                t=[]
                for i in range(l_brac+1,r_brac):
                    t.append(self.tokens[i])
                p=Parser(t,self.fn)
                t=p.make_while()
                t=self.makeExpr(t)
                k=[]
                oui=True
                for i in  range(len(self.tokens)):
                    if start<=i<=r_brac and oui==True:
                        oui=False
                        k.append(While(start,r_brac,e,t))
                    if not start<=i<=r_brac:
                        k.append(self.tokens[i])
                self.tokens=k
                self.ptr=r_brac+1
                        
            else:
                self.ptr+=1
        self.ptr=0
        return self.tokens
    def parse(self):
        global VARS
        self.make_while()
        
        self.ptr=0
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
                            return Error(self.tokens[name_idx].line_start,self.tokens[name_idx].line_end,"missing ';' ",self.fn)
                        val=self.evalExpr(Expr(self.makeExpr(e)))#le probleme il est la             
                        if isinstance(val,Error):return val
                        if val.value.__class__.__name__!=type_.type:
                            return Error(name.line_start,name.line_end,f"missmatch type '{type_.type}' was expected but '{val.value.__class__.__name__}' was returned",self.fn)
                        VARS[name.value]={"name":name,"type":type_.type,"value":val}
                        self.ptr=semi+1
                        
            elif type(self.tokens[self.ptr])==FuncCall:
                a=self.ptr
                if self.tokens[self.ptr].identifier in funcs.keys():
                    funcs[self.tokens[self.ptr].identifier]["key"](self.tokens[self.ptr].args if len(self.tokens[self.ptr].args)!=0 else None )
                    self.ptr=a+1
            elif self.tokens[self.ptr].type==TOKENS["identifier"]:
                name=self.tokens[self.ptr]
                if self.ptr+2<len(self.tokens):
                    if name.value not in funcs.keys():
                        return Error(self.tokens[self.ptr].line_start,self.tokens[self.ptr].line_end,f"identifier '{name.value}' not defined",self.fn)
                    l=self.ptr+1
                    r=findPar(self.tokens,l)
                    if r==None:
                         return Error(self.tokens[l].line_start,self.tokens[l].line_end,"'(' was never closed",self.fn)
                    e=[]
                    for i in range(l+1,r):
                        e.append(self.tokens[i])
                    e=self.makeExpr(e)
                    val=self.evalExpr(Expr(e))
                    funcs[name.value]["key"](val )
                    self.ptr=r+1
            elif type(self.tokens[self.ptr])==While:
                cond=self.tokens[self.ptr].condition.tok.copy()
                t=self.tokens[self.ptr].tok.copy()
                while (bool(self.evalExpr(  self.tokens[self.ptr].condition).value)):
                    p=Parser(t.copy(),self.fn)
                    p.parse()
                    self.tokens[self.ptr].condition.tok=cond.copy()
                    self.tokens[self.ptr].tok=t.copy()
                self.ptr+=1
            else:
                self.ptr+=1       
     
############################
#RUN

def run(fn,text):
    lexer=Lexer(fn,text)
    tokens=lexer.make_tokens()
    if isinstance(tokens,Error):
        print(tokens)
        return 1
    parser=Parser(tokens,fn)
    a=parser.parse()
    if isinstance(a,Error):
        print(a)
        return 1
run("stdio","""
    ount i = 1;
    ount k=ount_conv(input());
    while (k>i) {
        print(i);
        print("\n");
        ount i = i + 2;
    }
""")

