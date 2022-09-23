from  lexer import *
import sys

class Parser:
    def __init__(self,tokens):
        self.tokens=tokens
        self.ptr=0
        
    def getExpr(self):
        tok_expr=[]
        while self.ptr<len(self.tokens):
            if self.tokens[self.ptr].type==TOKENS[";"]:
                break
            tok_expr.append(self.tokens[self.ptr])
            self.ptr+=1
        self.ptr+=1
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
    
    def EvalExpr(self,t:list):
        op:Token
        op_idx=self.findBestOp(t)
        if op_idx!=None:
            op=t[op_idx] 
        elif len(t)>1:
            return Error("error in expression",None,None,None)
        if len(t)==0:
            return Error("error in expression",None,None,None)
        a:Token
        b:Token
        a=None
        b=None
        if 0<=op_idx-1:
            a=t[op_idx-1]
        if op_idx+1<len(t):
            b=t[op_idx+1]
        PluMinOp=[TOKENS["+"],TOKENS["-"]]
        if op.type in PluMinOp:
            if a.type in PluMinOp and b.type in PluMinOp:#(+/-)(+/-)(+/-)
                c=0
                if a.type==TOKENS["-"]:c+=1
                if b.type==TOKENS["-"]:c+=1
                if op.type==TOKENS["-"]:c+=1
                if c%2==0:res=Token(TOKENS["+"])
                else:res=Token(TOKENS["-"])
                t.pop(op_idx+1)
                t.pop(op_idx)
                t[op_idx-1]=res
            elif a.type not in PluMinOp and b.type in PluMinOp:#?(+/-)(+/-)
                c=0
                if b.type==TOKENS["-"]:c+=1
                if op.type==TOKENS["-"]:c+=1
                if c%2==0:res=Token(TOKENS["+"])
                else:res=Token(TOKENS["-"])
                t.pop(op_idx+1)
                t[op_idx]=res
            elif a.type  in PluMinOp and b.type not in PluMinOp:#(+/-)(+/-)?
                c=0
                if a.type==TOKENS["-"]:c+=1
                if op.type==TOKENS["-"]:c+=1
                if c%2==0:res=Token(TOKENS["+"])
                else:res=Token(TOKENS["-"])
                t.pop(op_idx)
                t[op_idx-1]=res
            elif a.type not in PluMinOp+PARENTHESES and b.type not in PluMinOp+PARENTHESES:#?(+/-)?
                t.pop(op_idx+1)
                t.pop(op_idx)
                if op.type==TOKENS["+"]:
                    t[op_idx-1]=Token(str(type(a.value+b.value).__name__),a.value+b.value)
                elif op.type==TOKENS["-"]:
                    t[op_idx-1]=Token(str(type(a.value+b.value).__name__),a.value-b.value)
            elif a.type in PARENTHESES:
                rpar_idx=op_idx-1
                lpar_idx=None
                c=-2
                count=1
                while op_idx-c>=0:
                    if t[op_idx-c].type==TOKENS[")"]:count+=1
                    elif t[op_idx-c].type==TOKENS["("] and count>0:count-=1
                    elif t[op_idx-c].type==TOKENS["("] and count==0:lpar_idx=op_idx-c
                    c-=1
                tt=[]
                for i in range(lpar_idx+1,rpar_idx):
                    tt.append(t[i])
                e=self.EvalExpr(tt)
                to=[]
                notset=True
                for i in range(len(t)):
                    if lpar_idx<=i<=rpar_idx and notset:
                        to.append(e)
                        notset=False
                    else:to.append(t[i])
                t=to



                        
        if len(t)>1:
            return self.EvalExpr(t)
        return t
            
        
    def parse(self):
        while self.ptr<len(self.tokens):
            if self.ptr+3<len(self.tokens):#Type Identifer Eq Expr
                if self.tokens[self.ptr].type in TYPES and self.tokens[self.ptr+1].type==TOKENS["identifier"] and self.tokens[self.ptr+2].type==TOKENS["="]:
                    name=self.tokens[self.ptr+1]
                    type_=self.tokens[self.ptr]
                    self.ptr+=3
                    val=self.EvalExpr(self.getExpr())[0]
                    if isinstance(val,Error):return val
                    VARS[name]=Var(name,type_,val.value)
                    
     
############################
#RUN

def run(fn,text):
    lexer=Lexer(fn,text)
    tokens=lexer.make_tokens()
    parser=Parser(tokens)
    parser.parse()
    print(VARS)

run("stdio","""
    int b=3+(6+3)+3;
    """)