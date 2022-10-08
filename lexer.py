from classes import *




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

LETTERS="azertyuiopqsdfghjklmmwxcvbnéèêëàâäüûïîöôùç"
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


class Error:
    def __init__(self,pos_start,pos_end,error_name,details):
        self.pos_start=pos_start
        self.pos_end=pos_end
        self.error_name=error_name
        self.details=details
        
    def __repr__(self):
        result=f'{self.error_name}, file:{self.details}'
        result+=f", from {self.pos_start} to {self.pos_end}"
        return result
    
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
    def __init__(self,type_,value=None) -> None:
        self.type=type_
        self.value=value
        
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
            if self.text[self.ptr] in DIGITS:
                a=self.make_number()
                if isinstance(a,Error):
                    return a
                tokens.append(a)
            elif self.text[self.ptr]=="'"or self.text[self.ptr]=='"':
                a=self.make_string()
                if isinstance(a,Error):
                    return a
                tokens.append(a)
            elif self.text[self.ptr]=="/" and self.ptr+1<len(self.text) and self.text[self.ptr+1]=="/":
                    tokens.append(Token(TOKENS["//"]))
                    self.ptr+=2
            elif self.text[self.ptr]=="=" and self.ptr+1<len(self.text) and self.text[self.ptr+1]=="=":
                    tokens.append(Token(TOKENS["=="]))
                    self.ptr+=2
            elif self.text[self.ptr]=="-" and self.ptr+1<len(self.text) and self.text[self.ptr+1]=="=":
                    tokens.append(Token(TOKENS["-="]))
                    self.ptr+=2
            elif self.text[self.ptr]=="+" and self.ptr+1<len(self.text) and self.text[self.ptr+1]=="=":
                    tokens.append(Token(TOKENS["+="]))
                    self.ptr+=2
            elif self.text[self.ptr]=="<" and self.ptr+1<len(self.text) and self.text[self.ptr+1]=="=":
                    tokens.append(Token(TOKENS[">="]))
                    self.ptr+=2
            elif self.text[self.ptr]=="=" and self.ptr+1<len(self.text) and self.text[self.ptr+1]=="=":
                    tokens.append(Token(TOKENS[">="]))
                    self.ptr+=2
            elif self.text[self.ptr]=="!" and self.ptr+1<len(self.text) and self.text[self.ptr+1]=="=":
                    tokens.append(Token(TOKENS["!="]))
                    self.ptr+=2
            elif self.text[self.ptr] in LETTERS:
                a=""
                c=0
                while self.ptr+c <len(self.text) and self.text[self.ptr+c] in LETTERS:
                    if self.ptr+c<len(self.text):
                        a+=self.text[self.ptr+c]
                        c+=1
                if a in KEYWORDS.keys():
                    tokens.append(Token(KEYWORDS[a]))
                elif a in TYPES:
                    tokens.append(Token(a))
                else:
                    tokens.append(Token(TOKENS["identifier"],a))
                self.ptr+=c
            elif self.text[self.ptr]in TOKENS.keys():
                tokens.append(Token(TOKENS[self.text[self.ptr]]))
                self.ptr+=1
            else:
                self.ptr+=1
        return tokens
    def make_number(self):
        dot=0
        s=""
        while self.ptr<len(self.text) and self.text[self.ptr] in DIGITS+".":
            if self.text[self.ptr]==".":
                dot+=1
            if dot>1:
                return Error(self.ptr,self.ptr,"too many '.' in number",self.fn)
            s+=self.text[self.ptr]
            self.ptr+=1
        if "."in s:  
            return  Token("float",floap(s))
        return Token("int",ount(s))
    def make_string(self):
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
            return Token("STRING",s)
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
            return Token("STRING",s)
            


