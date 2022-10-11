from cgitb import text
from classes import *


class While:
    def __init__(self,start,end,condition,tokens) -> None:
         self.type="While"
         self.start=start
         self.end=end
         self.tok=tokens
         self.condition=condition
         
    def __repr__(self) -> str:
         return f"""While:({str(self.condition)}){
             {str(self.tok)}
         }
     
     """

####################################
#CONSTANTS



DIGITS="1234567890"


VARS={}
FUNCDEF={}#id:{FuncDef}
FUNCDEFCLASS={}#[id,class]:{VarDef}
FUNCVARS={}#{"function name":[[a=2],[a=3]]}plusieur liste si il ya de la recustion
TYPES=[
    "string",
    "int",
    "ount",
    "floap",
    "boolean",
    "float",
    "list",
    "dict",
    "bool",
    "char"
]

KEYWORDS={
    "func":"FUNCTION",
    "function":"FUNCTION",
    "fun":"FUNCTION",
    "def":"FUNCTION",
    "global":"GLOBAL",
    "private":"PRIVATE",
    "swap":"SWAP",
    "return":"RETURN",
    "goto":"GOTO",
    "if":"IF",
    "else":"ELSE",
    "elif":"ELIF",
    "while":"WHILE"
}

LETTERS="azertyuiopqsdfghjklmmwxcvbnéèêëàâäüûïîöôùç_"
LETTERS+=LETTERS.upper()

class Expr:
    def __init__(self,tok):
        self.type="expr"
        self.tok=tok
    def __repr__(self) -> str:
         return "E:"+str(self.tok)

     

class VarCall:
    def __init__(self,name) -> None:
         self.name=name
         self.type="VarCall"

class VarDef:
    def __init__(self,name,type_,val,tag="global",other=None):
        """
        other is for private Var to tell to wich class and variable that  is linked
        tag="global"|"private"|"function"|"constant"
        """
        self.VarType=type_
        self.type="VarDef"
        self.val=val
        self.tag=tag
        self.other=other
    def __repr__(self):
        return f'{self.type} | ({self.tag}/{self.other}) : {self.val}'

#######################################
#ERROR



    
class IllegalCharError(Error):
    def __init__(self,pos_start,pos_end,details):
        super().__init__(pos_start,pos_end,"Illegal Character",details)

########################################
#TOKENS

TOKENS={
    "identifier":"IDENTIFIER",
    ".":"DOT",
    ":":"COLON",
    ",":"COMMA",
    "?":"TERNAYOP",
    "-=":"MINVARSET",
    "+=":"PLUSVARSET",
    "!=":"DIFF",
    "<=":"LEESEQ",
    ">=":"GREATEQ",
    "<":"LESS",
    ">":"GREAT",
    "&":"AND",
    "|":"OR",
    "=":"VARSET",
    "==":"EQ",
    "^":"POW",
    ";":"SEMICOL",
    ">>":"rshift",
    "<<":"lshift",
    "+":"PLUS",
    "-":"MINUS",
    "*":"MUL",
    "/":"DIV",
    "//":"EUCLDIVE",
    "%":"MOD",
    "(":"LPAREN",
    ")":"RPAREN",
    "[":"LBRAC",
    "]":"RBRAC",
    "{":"LACCO",
    "}":"RACCO"
}
OPS=["PLUS","MINUS","DIV","MUL","EUCLDIVE","MOD","POW"]
PARENTHESES=[ "LPAREN","RPAREN","LBRAC","RBRAC","LACCO","RACCO"]
LOGICOP=["EQ","DIFF","LEESEQ","GREATEQ","LESS","GREAT","AND","OR",]
class Token:
    def __init__(self,type_,value=None,line_start=0,line_end=None) -> None:
        self.type=type_
        self.value=value
        self.line_start=0
        self.line_end=line_end
        if self.line_end==None:
            self.line_end=self.line_start
        
    def isTok(self):
        return self.value==None
        
    
    def __repr__(self) -> str:
        if self.value:return  f"T:({self.type}:{self.value})"
        return f"T:({self.type})"


class FuncCall:
    def __init__(self,identifier,args):
        self.identifier=identifier
        self.type="FuncCall"
        self.args=args
    def __repr__(self) -> str:
        a=f"{self.identifier}:("
        a+=str(self.args)
        a+=")"
        return a

class FunctionDef:
    def __init__(self,id,args,tok) -> None:
        self.id=id
        self.args=args
        self.tok=tok
        
        
        
def findPar(t,l,type_left=TOKENS["("],type_right=TOKENS[")"]):
    """"
    t:tokens
    l:left parenthes index
    return right parenthes index
    
    """
    c=0
    for  i in range(l+1,len(t)):
        if t[i].type==type_left:
            c+=1
        elif t[i].type==type_right and c>0:
            c-=1
        elif t[i].type==type_right and c==0:
            return i 
        
    
         
         
def getLineOfIdx(t,idx):
    a=1
    for i in range(0,len(t)):
        if t[i]=="\n":a+=1
        if i==idx:
            return a
################################
#LEXER
    
    
class Lexer:
    def __init__(self,fn,text) -> None:
        self.fn=fn
        self.text=text 
        self.ptr=0
    def make_tokens(self)->list|Error:
        tokens=[]
        while self.ptr<len(self.text):
            if self.text[self.ptr] in  DIGITS:
                if self.ptr+1<len(self.text) and self.text[self.ptr+1]=="b":
                    tokens.append(Token("boolean",boolean(bool(int(self.text[self.ptr]))),getLineOfIdx(self.text,self.ptr)))
                    self.ptr+=2
            if self.text[self.ptr] in DIGITS:
                a=self.make_number()
                if isinstance(a,Error):
                    return a
                tokens.append(a)
            #elif self.text[self.ptr]=="$":
            #    a=self.make_quaternion()             
            #    if isinstance(a,Error):
            #        return a
            #    tokens.append(a)   
            elif self.text[self.ptr]=="'"or self.text[self.ptr]=='"':
                a=self.make_string()
                if isinstance(a,Error):
                    return a
                tokens.append(a)
            elif self.text[self.ptr]=="/" and self.ptr+1<len(self.text) and self.text[self.ptr+1]=="/":
                    tokens.append(Token(TOKENS["//"],None,getLineOfIdx(self.text,self.ptr),getLineOfIdx(self.text,self.ptr+1)))
                    self.ptr+=2
            elif self.text[self.ptr]=="=" and self.ptr+1<len(self.text) and self.text[self.ptr+1]=="=":
                    tokens.append(Token(TOKENS["=="],None,getLineOfIdx(self.text,self.ptr),getLineOfIdx(self.text,self.ptr+1)))
                    self.ptr+=2
            elif self.text[self.ptr]=="-" and self.ptr+1<len(self.text) and self.text[self.ptr+1]=="=":
                    tokens.append(Token(TOKENS["-="],None,getLineOfIdx(self.text,self.text,self.ptr),getLineOfIdx(self.text,self.text,self.ptr+1)))
                    self.ptr+=2
            elif self.text[self.ptr]=="+" and self.ptr+1<len(self.text) and self.text[self.ptr+1]=="=":
                    tokens.append(Token(TOKENS["+="],None,getLineOfIdx(self.text,self.text,self.ptr),getLineOfIdx(self.text,self.text,self.ptr+1)))
                    self.ptr+=2
            elif self.text[self.ptr]=="<" and self.ptr+1<len(self.text) and self.text[self.ptr+1]=="=":
                    tokens.append(Token(TOKENS[">="],None,getLineOfIdx(self.text,self.text,self.ptr),getLineOfIdx(self.text,self.text,self.ptr+1)))
                    self.ptr+=2
            elif self.text[self.ptr]=="=" and self.ptr+1<len(self.text) and self.text[self.ptr+1]=="=":
                    tokens.append(Token(TOKENS[">="],None,getLineOfIdx(self.text,self.text,self.ptr),getLineOfIdx(self.text,self.text,self.ptr+1)))
                    self.ptr+=2
            elif self.text[self.ptr]=="!" and self.ptr+1<len(self.text) and self.text[self.ptr+1]=="=":
                    tokens.append(Token(TOKENS["!="],None,getLineOfIdx(self.text,self.text,self.ptr),getLineOfIdx(self.text,self.text,self.ptr+1)))
                    self.ptr+=2
            elif self.text[self.ptr]=="<" and self.ptr+1<len(self.text) and self.text[self.ptr+1]=="<":
                    tokens.append(Token(TOKENS["<<"],None,getLineOfIdx(self.text,self.ptr),getLineOfIdx(self.text,self.ptr+1)))
                    self.ptr+=2
            elif self.text[self.ptr]==">" and self.ptr+1<len(self.text) and self.text[self.ptr+1]==">":
                    tokens.append(Token(TOKENS[">>"],None,getLineOfIdx(self.text,self.ptr),getLineOfIdx(self.text,self.ptr+1)))
                    self.ptr+=2
            elif self.text[self.ptr] in LETTERS:
                start=getLineOfIdx(self.text,self.ptr)
                a=""
                c=0
                while self.ptr+c <len(self.text) and self.text[self.ptr+c] in LETTERS:
                    if self.ptr+c<len(self.text):
                        a+=self.text[self.ptr+c]
                        c+=1
                if a in KEYWORDS.keys():
                    end=getLineOfIdx(self.text,self.ptr+c)
                    tokens.append(Token(KEYWORDS[a],None,start,end))
                elif a in TYPES:
                    end=getLineOfIdx(self.text,self.ptr+c)
                    tokens.append(Token(a,None,start,end))
                else:
                    end=getLineOfIdx(self.text,self.ptr+c)
                    tokens.append(Token(TOKENS["identifier"],a,start,end))
                self.ptr+=c
            elif self.text[self.ptr]in TOKENS.keys():
                tokens.append(Token(TOKENS[self.text[self.ptr]],None,start))
                self.ptr+=1
            else:
                self.ptr+=1
        return tokens
    def make_complex(self):
        self.ptr+=1
        while self.text[self.ptr] in "\n \t" and self.ptr<len(self.text):
            self.ptr+=1
        if self.text[self.ptr] in "ijk":
            return
    def make_number(self):
        start=getLineOfIdx(self.text,self.ptr)
        dot=0
        s=""
        while self.ptr<len(self.text) and self.text[self.ptr] in DIGITS+".":
            if self.text[self.ptr]==".":
                dot+=1
            if dot>1:
                return Error(self.ptr,self.ptr,"too many '.' in number",self.fn)
            s+=self.text[self.ptr]
            self.ptr+=1
        end=getLineOfIdx(self.text,self.ptr)
        if "."in s:  
            return  Token("floap",floap(s),start,end)
        return Token("ount",ount(s),start,end)
    def make_string(self):
        start=getLineOfIdx(self.text,self.ptr)
        s=""
        
        if self.text[self.ptr]=="'":
            self.ptr+=1
            first=self.ptr-1
            find=0
            while self.ptr<len(self.text):
                if self.text[self.ptr]=="'":find=1;break
                s+=self.text[self.ptr]
                self.ptr+=1
            self.ptr+=1
            if not find :
                 return Error(first,first,"String error: ' was never closed ",self.fn)
            return Token("string",string(s),start,getLineOfIdx(self.ptr))
        elif self.text[self.ptr]=='"':
            self.ptr+=1
            first=self.ptr-1
            find=0
            while self.ptr<len(self.text):
                if self.text[self.ptr]=='"':find=1;break
                s+=self.text[self.ptr]
                self.ptr+=1
            self.ptr+=1
            if not find :
                 return Error(first,first,'String error: " was never closed ',self.fn)
            return Token("string",string(s),start,getLineOfIdx(self.text,self.ptr))
            


