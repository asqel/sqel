import os
from  lexer import *
import sys
from op import *
from  classes import *


from random import randint
class func:
    def not_func(x):
        return Token("boolean",boolean(not x.value))

    def print_func(x):
        if type(x)==list:
            for i in x:
                func.print_func(i)

        elif x.type==TOKENS["identifier"] and x.value in VARS.keys():
            print(VARS[x.value]["value"].value)
        else:
            print(x.value)

    def input_func(x):
        return Token("string",string(input()))

    def ount_conv(k):
        x=k
        if type(k)!=Token:
            x=k[0]
        else:c=ount(int(x.value))
        return Token("ount",c,x.line_start,x.line_end)

    def random_func(a):
        return Token("ount",randint(0,int(a.value)),a.line_start,a.line_end)

    def string_conv(k):
        x=k
        if type(k)!=Token:
            x=k[0]
        return Token("string",string(x.value),x.line_start,x.line_end)

    def open_window(x):
        if x!=None:
            return False
        print("pourquoi")

    def import_func(x):
        path=str(x.value)
        if type(x.value)!=string:print(Error(x.line_start,x.line_end,"import only takes string arguments",None));exit()
        if not os.path.exists(str(path)):print(Error(x.line_start,x.line_end,f"import only takes absolute path or maybe the file does  not exist : {path}",None));exit()
        if not os.path.isfile(path):print(Error(x.line_start,x.line_end,f"import only takes path of file : {path}",None));exit()
        l=Lexer(path,open(path,"r").read())
        t=l.make_tokens()
        p=Parser(t,path)
        p.parse()
    



funcs={"print":{"builtin":True,"key":func.print_func},
                            "input":{"builtin":True,"key":func.input_func},
                            "to_ount":{"builtin":True,"key":func.ount_conv},
                            "to_string":{"builtin":True,"key":func.string_conv},
                            "open_window":{"builtin":True,"key":func.open_window},
                            "not":{"builtin":True,"key":func.not_func},
                            "random":{"builtin":True,"key":func.random_func},
                            "import":{"builtin":True,"key":func.import_func}
       }



class Parser:
    def __init__(self,tokens,fn):
        self.tokens=tokens
        self.ptr=0
        self.fn=fn
        self.abs_tokens=tokens.copy()
        
    def makeExpr(self,t):
        tok_expr=[]
        p=0
        while p<len(t):
            if t[p].type==TOKENS["identifier"]:
                name=t[p].value
                if p+1<len(t) and t[p+1].type==TOKENS["("]:
                    left=p+1
                    right=findPar(t,left)
                    if right==None:
                        print(Error(t[left].line_start,t[left].line_end,"'(' was never closed",self.fn))
                        exit()
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
                if right==None:
                    print(Error(t[left].line_start,t[left].line_end,"'(' was never closed",self.fn))
                    exit()
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
            if t[i]!=None and t[i].type==TOKENS["^"]:
                return i
        for i in range(len(t)):#scan for MUL DIV MOD EUCLIDIVE(* / % //)
            if t[i]!=None and t[i].type in [TOKENS["*"],TOKENS["/"],TOKENS["%"],TOKENS["//"]]:
                return i
        for i in range(len(t)):
            if t[i]!=None and t[i].type in [TOKENS["+"],TOKENS["-"]]:
                return i
        for i in range(len(t)):
            if t[i]!=None and t[i].type in [TOKENS[">>"],TOKENS["<<"]]:
                return i
        for i in range(len(t)):#scan for logic operation 
            if t[i]!=None and t[i].type in COMPAR_OP:
                return i
        for i in range(len(t)):#scan for logic operation 
            if t[i]!=None and t[i].type in LOGICA_OP:
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
                print(expr)
                print(Error(expr.tok[0].line_start,expr.tok[0].line_end,"error in expression",self.fn))
                exit()
            else:
                return None
        elif expr.tok[op].type==TOKENS["^"]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                print(Error(expr.tok[op].line_start,expr.tok[op].line_end,"Error in expression : missing parameter for ^ (pow) operator ",self.fn))
                exit()
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=pow_op(a,b)
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
        elif expr.tok[op].type==TOKENS["*"]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                print(Error(expr.tok[op].line_start,expr.tok[op].line_end,"Error in expression : missing parameter for * (mul) operator ",self.fn))
                exit()
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=mul_op(a,b)
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
        elif expr.tok[op].type==TOKENS["/"]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                print(Error(expr.tok[op].line_start,expr.tok[op].line_end,"Error in expression : missing parameter for / (div) operator ",self.fn))
                exit()
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=div_op(a,b)
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
        elif expr.tok[op].type==TOKENS["%"]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                print(Error(expr.tok[op].line_start,expr.tok[op].line_end,"Error in expression : missing parameter for % (modulo) operator ",self.fn))
                exit()
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=mod_op(a,b)
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
        elif expr.tok[op].type==TOKENS["//"]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                print(Error(expr.tok[op].line_start,expr.tok[op].line_end,"Error in expression : missing parameter for // (euclidiv) operator ",self.fn))
                exit()
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=euclidiv_op(a,b)
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
        elif expr.tok[op].type==TOKENS[">>"]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                print(Error(expr.tok[op].line_start,expr.tok[op].line_end,"Error in expression : missing parameter for >> (rshift) operator ",self.fn))
                exit()
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
                print(Error(expr.tok[op].line_start,expr.tok[op].line_end,"Error in expression : missing parameter for << (lshift) operator ",self.fn))
                exit()
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
            if b==None:
                print(Error(expr.tok[op].line_start,expr.tok[op].line_end,"error in expression : missing parameter for + (add) operator",self.fn))
                exit()
            c=add_op(a,b,expr.tok,op)
        elif expr.tok[op].type==TOKENS["-"]:
            a=None
            b=None
            if op+1<len(expr.tok):
                b=expr.tok[op+1]
            if op-1>=0:
                a=expr.tok[op-1]
            if b==None:
                print(Error(expr.tok[op].line_start,expr.tok[op].line_end,"error in expression : missing parameter for - (minus) operator",self.fn))
                exit()
            c=min_op(a,b,expr.tok,op)
        elif expr.tok[op].type==TOKENS["=="]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                print(Error(expr.tok[op].line_start,expr.tok[op].line_end,"error in expression : missing parameter for == (eq) operator ",self.fn))
                exit()
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=eq_op(a,b)
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
        elif expr.tok[op].type==TOKENS["!="]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                print(Error(expr.tok[op].line_start,expr.tok[op].line_end,"error in expression : missing parameter for != (diff) operator",self.fn))
                exit()
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=eq_op(a,b)
            c.value=not c.value
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
        elif expr.tok[op].type==TOKENS[">"]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                print(Error(expr.tok[op].line_start,expr.tok[op].line_end,"error in expression : missing parameter for > (gt) operator ",self.fn))
                exit()
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=gt_op(a,b)
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
            
        elif expr.tok[op].type==TOKENS["<"]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                print(Error(expr.tok[op].line_start,expr.tok[op].line_end,"error in expression : missing parameter for < (lt) operator ",self.fn))
                exit()
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=gt_op(b,a)
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
            
        elif expr.tok[op].type==TOKENS["<="]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                print(Error(expr.tok[op].line_start,expr.tok[op].line_end,"error in expression : missing parameter for <= (le) operator ",self.fn))
                exit()
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=eq_op(a,b)
            d=gt_op(a,b)
            d.value=not d.value
            c=or_op(d,c)
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
        
        elif expr.tok[op].type==TOKENS[">="]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                print(Error(expr.tok[op].line_start,expr.tok[op].line_end,"error in expression : missing parameter for >= (ge operator",self.fn))
                exit()
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=eq_op(a,b)
            d=gt_op(a,b)
            c=or_op(d,c)
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
        
        
        elif expr.tok[op].type==TOKENS["&"]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                print(Error(expr.tok[op].line_start,expr.tok[op].line_end,"error in expression : missing parameter for & (and) operator ",self.fn))
                exit()
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=and_op(a,b)
            expr.tok.pop(op+1)
            expr.tok.pop(op)
            expr.tok[op-1]=c
        
        elif expr.tok[op].type==TOKENS["|"]:
            if not(op-1>=0 and op+1<len(expr.tok)):
                print(Error(expr.tok[op].line_start,expr.tok[op].line_end,"error in expression : missing parameter for | (or) operatorr ",self.fn))
                exit()
            a=expr.tok[op-1]
            b=expr.tok[op+1]
            c=or_op(a,b)
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
                if r_par==None:
                    print(Error(self.tokens[start].line_start,self.tokens[start].line_end,"'(' was never closed",self.fn))
                    exit()
                e=[]
                for i in range(l_par+1,r_par):
                    e.append(self.tokens[i])
                e=Expr(self.makeExpr(e))
                if not( r_par <len(self.tokens) and self.tokens[r_par+1].type==TOKENS["{"]):
                    print(Error(self.tokens[l_par].line_start,self.tokens[l_par].line_end,"error in while"))
                    exit()
                l_brac=r_par+1
                r_brac=findPar(self.tokens,l_brac,TOKENS["{"],TOKENS["}"])
                if r_brac==None:
                    print(Error(self.tokens[l_brac].line_start,self.tokens[l_brac].line_end,"'{' was never closed",self.fn))
                    exit()
                t=[]
                for i in range(l_brac+1,r_brac):
                    t.append(self.tokens[i])
                p=Parser(t,self.fn)
                t=p.make_while()
                p=Parser(t,self.fn)
                t=p.make_if()
                t=self.makeExpr(t)
                
                k=[]
                oui=True
                for i in  range(len(self.tokens)):
                    if start<=i<=r_brac and oui==True:
                        oui=False
                        k.append(While(start,r_brac,e,t))
                    if not start<=i<=r_brac:
                        k.append(self.tokens[i])
                self.tokens=k.copy()
                k=[]
                self.ptr=start+1
                        
            else:
                self.ptr+=1
        self.ptr=0
        return self.tokens
    
    def make_if(self):
        while self.ptr<len(self.tokens):
            if self.tokens[self.ptr].type==KEYWORDS["if"] and self.ptr+1<len(self.tokens):
                start=self.ptr
                l_par=self.ptr+1
                r_par=findPar(self.tokens,l_par)
                if r_par==None:
                    print(Error(self.tokens[start].line_start,self.tokens[start].line_end,"'(' was never closed",self.fn))
                    exit()
                e=[]
                for i in range(l_par+1,r_par):
                    e.append(self.tokens[i])
                e=Expr(self.makeExpr(e))
                if not( r_par <len(self.tokens) and self.tokens[r_par+1].type==TOKENS["{"]):
                    print(Error(self.tokens[l_par].line_start,self.tokens[l_par].line_end,"error in if"))
                    exit()
                l_brac=r_par+1
                r_brac=findPar(self.tokens,l_brac,TOKENS["{"],TOKENS["}"])
                if r_brac==None:
                    print(Error(self.tokens[l_brac].line_start,self.tokens[l_brac].line_end,"'{' was never closed",self.fn))
                    exit()
                t=[]
                for i in range(l_brac+1,r_brac):
                    t.append(self.tokens[i])
                p=Parser(t,self.fn)
                t=p.make_if()
                p=Parser(t,self.fn)
                t=p.make_while()
                t=self.makeExpr(t)
                k=[]
                oui=True
                for i in  range(len(self.tokens)):
                    if start<=i<=r_brac and oui==True:
                        oui=False
                        k.append(If(start,r_brac,e,t))
                    if not start<=i<=r_brac:
                        k.append(self.tokens[i])
                self.tokens=k
                self.ptr=start+1
                        
            else:
                self.ptr+=1
        self.ptr=0
        return self.tokens
    
    def parse(self):
        global VARS
        self.make_if()
        self.make_while()
        self.ptr=0
        while self.ptr<len(self.tokens):
            #print(self.tokens[self.ptr],"salut les",self.uuid,"su")
            
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
                            print(Error(self.tokens[name_idx].line_start,self.tokens[name_idx].line_end,"missing ';' ",self.fn))
                            exit()
                        val=self.evalExpr(Expr(self.makeExpr(e).copy()))#le probleme il est la 
                        if isinstance(val,Error):
                            print(val)
                            exit()
                        if val.value.__class__.__name__!=type_.type:
                            print(Error(name.line_start,name.line_end,f"missmatch type '{type_.type}' was expected but '{val.value.__class__.__name__}' was returned",self.fn))
                            exit()
                        VARS[name.value]={"name":name,"type":type_.type,"value":val}
                        self.ptr=semi+1
                        
            elif type(self.tokens[self.ptr])==FuncCall:
                a=self.ptr
                if self.tokens[self.ptr].identifier in funcs.keys():
                    c=self.evalExpr(Expr(self.tokens[self.ptr].args.copy()))
                    funcs[self.tokens[self.ptr].identifier]["key"]( c if len(self.tokens[self.ptr].args)!=0 else None )
                    self.ptr=a+1
            elif self.tokens[self.ptr].type==TOKENS["identifier"]:
                name=self.tokens[self.ptr]
                name_idx=self.ptr
                if self.ptr+2<len(self.tokens):
                    if name.value in funcs.keys():
                        l=self.ptr+1
                        r=findPar(self.tokens,l)
                        if r==None:
                            print(Error(self.tokens[l].line_start,self.tokens[l].line_end,"'(' was never closed",self.fn))
                            exit()
                        e=[]
                        for i in range(l+1,r):
                            e.append(self.tokens[i])
                        e=self.makeExpr(e)
                        val=self.evalExpr(Expr(e.copy()))
                        funcs[name.value]["key"](val)
                        self.ptr=r+1
                    elif name.value in VARS.keys():
                        e=[]
                        semi=None
                        for i in range(name_idx+2,len(self.tokens)):
                            if self.tokens[i].type==TOKENS[";"]:semi=i;break
                            e.append(self.tokens[i])
                        if semi==None:
                            print(Error(self.tokens[name_idx].line_start,self.tokens[name_idx].line_end,"missing ';' ",self.fn))
                            exit()
                        val=self.evalExpr(Expr(self.makeExpr(e).copy()))#le probleme il est la 
                        if isinstance(val,Error):return val
                        if val.value.__class__.__name__!=VARS[name.value]["value"].value.__class__.__name__:
                            print(Error(name.line_start,name.line_end,f"missmatch type '{type_.type}' was expected but '{val.value.__class__.__name__}' was returned",self.fn))
                            exit()
                        VARS[name.value]["value"]=val
                        self.ptr=semi+1
                    else:
                        print(Error(name.line_start,name.line_end,f"identifier '{name.value}' not defined",self.fn))
                        exit()
                        
                    
            elif type(self.tokens[self.ptr])==While:
                cond=self.tokens[self.ptr].condition.tok.copy()
                t=self.tokens[self.ptr].tok.copy()
                while (bool(self.evalExpr(  Expr(self.tokens[self.ptr].condition.tok.copy())).value)):
                    p=Parser(t.copy(),self.fn)
                    p.parse()
                    self.tokens[self.ptr].condition.tok=cond.copy()
                    self.tokens[self.ptr].tok=t.copy()
                self.ptr+=1
            elif type(self.tokens[self.ptr])==If:
                cond=self.tokens[self.ptr].condition.tok.copy()
                t=self.tokens[self.ptr].tok.copy()
                if (bool(self.evalExpr(  Expr(self.tokens[self.ptr].condition.tok.copy())).value)):
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


run(__file__,"""
        import("C:/Users/axel/Documents/GitHub/sqel/a.qel");
        print(random(10));/* random(x): renvoie 1 chiffre random entre 0(inclus) et x(inclus)*/
        ount end =1000;
        ount i =0;
        while(i<end){
            boolean b=1b;
            ount p=2;
            if (i==2){
                print(i)
                }
            if (i>2){
                while(p<to_ount(i^0.5)+3){/* jai pas fini les floap donc faut les convertir en ount */
                if(i%p==0){
                    b=0b;


                }
                p=p+1;
                }
            }

            if (b & i>2){
                print(i);
                }
            i=i+1;


        }

    """)
