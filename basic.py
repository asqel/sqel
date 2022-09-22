####################################
#CONSTANTS

DIGITS="1234567890"


VARS={
    "GLOBAL":{},
    "FUNC":{},
    "CONSTANT":{},
    "PRIVATE":{}
}
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
    "if":"IF"
}

LETTERS="azertyuiopqsdfghjklmmwxcvbn"
LETTERS+=LETTERS.upper()



class var:
    def __init__(self,type_,val):
        self.type=type_
        self.val=val
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

class Token:
    def __init__(self,type_,value=None) -> None:
        self.type=type_
        self.value=value
    
    def __repr__(self) -> str:
        if self.value:return  f"{self.type}:{self.value}"
        return f"{self.type}"

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
            return  Token("FLOAT",float(s))
        return Token("INT",int(s))
    def make_string(self):
        s=""
        if self.text[self.ptr]=="'":
            self.ptr+=1
            while self.ptr<len(self.text) and self.text[self.ptr]!="'":
                s+=self.text[self.ptr]
                self.ptr+=1
            self.ptr+=1
            if self.ptr>=len(self.text):
                return Error(None,None,"String error: ' was never closed ",self.fn)
            return Token("STRING",s)
        elif self.text[self.ptr]=='"':
            self.ptr+=1
            while self.ptr<len(self.text) and self.text[self.ptr]!='"':
                s+=self.text[self.ptr]
                self.ptr+=1
            self.ptr+=1
            if self.ptr>=len(self.text):
                return Error(None,None,"String error: ' was never closed ",self.fn)
            return Token("STRING",s)
            
class Function:
    def __init__(self,tokens,name,arg=()):
        self.tokens=tokens
        self.name=name
        self.arg=()

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
        
        
        
    def parse(self):
        while self.ptr<len(self.tokens):
            if self.tokens[self.ptr].type==KEYWORDS["def"] and self.ptr+1<len(self.tokens):
                if self.tokens[self.ptr+1].type==TOKENS["identifier"]:
                    name=self.tokens[self.ptr+1]
                    if self.ptr+2<len(self.tokens):
                        lpar_idx=self.ptr+2
                        c=3
                        count=0
                        rpar_dix=None
                        while self.ptr+c<len(self.tokens):
                            if self.tokens[self.ptr+c].type==TOKENS["("]:
                                count+=1
                            elif self.tokens[self.ptr+c].type==TOKENS[")"] and count>0:
                                count-=1
                            elif self.tokens[self.ptr+c].type==TOKENS[")"] and count==0:
                                rpar_idx=self.ptr+c
                                break
                            c+=1
                        if rpar_dix==None:
                            pass#error '(' was never closed
                        arg=[]
                        a=1+lpar_idx
                        while a<rpar_idx:
                            if  self.tokens[a].type in TYPES and a+1<rpar_idx and self.tokens[a+1].type==TOKENS["identifier"]:
                                arg.append({"type":self.tokens[a].type,"identifier":self.tokens[a+1].value})
                                a+=2
                            elif self.tokens[a].type==TOKENS[","]:
                                a+=1
                            else:
                                a+=1
                                pass #error
                            
                            #ensuite faut faire pareil mais pour les " { " 
                        print(arg)            
            elif self.tokens[self.ptr].type==KEYWORDS["private"] and self.ptr+4<len(self.tokens):
                if self.tokens[self.ptr+1].type in TYPES and self.tokens[self.ptr+2].type==TOKENS["identifier"] and self.tokens[self.ptr+3].type==TOKENS["="]:
                    name=self.tokens[self.ptr+2].value
                    ty=self.tokens[self.ptr+1].type
                    self.ptr+=4
                    val=self.getExpr()
                            
                            
            self.ptr+=1
                
            
            
            
        


############################
#RUN

def run(fn,text):
    lexer=Lexer(fn,text)
    tokens=lexer.make_tokens()
    print(tokens)
    print(VARS)
    parser=Parser(tokens)
    parser.parse()


run("stdio","""private int a=3+4*(5+a(8)%3);
    """)