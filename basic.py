####################################
#CONSTANTS

DIGITS="1234567890"


VARS={
    "GLOBAL":{},
    "FUNC":{},
    "CONSTANT":{},
    "PRIVATE":{}
}
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
            
            
            
            
            
            
            
        


############################
#RUN

def run(fn,text):
    lexer=Lexer(fn,text)
    tokens,error=lexer.make_tokens()
    




lexer=Lexer("st","1+2+2*3.6+'au'+/'hujù%'%   //2")

print(lexer.make_tokens())