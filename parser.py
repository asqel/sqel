from  lexer import *

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
    
    def findBestOp(t):
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
            return Error("error in expression")
        a:Token
        b:Token
        a=None
        b=None
        if 0<=op_idx-1:
            a=t[op_idx-1]
        if op_idx+1<len(t):
            b=t[op_idx+1]
        PluMinOp=[TOKENS["+"],TOKENS["'-"]]
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
            elif a.type not in PluMinOp and b.type not in PluMinOp:#?(+/-)?
                t.pop(op_idx+1)
                t.pop(op_idx)
                t[op_idx-1]=a.value+ b.value if op.type==TOKENS["+"] else a.value-b.value
                        
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
                    val=self.evalExpr(self.getExpr())
                    VARS["GLOBAL"][name]=[type_,val]
                    
     
############################
#RUN

def run(fn,text):
    lexer=Lexer(fn,text)
    tokens=lexer.make_tokens()
    parser=Parser(tokens)
    parser.parse()


run("stdio","""
    
    string b=7+(3+5)/4%13//7.08;
    """)


