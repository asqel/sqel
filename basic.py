
from re import A
from string import digits


DIGITS="1234567890"

TT_INT="INT"
TT_FLOAT="FLOAT"
TT_PLUS="PLUS"
TT_MINUS="MINUS"
TT_DIV="DIV"
TT_MUL="MUL"
TT_MOD="MOD"
TT_LPAREN="LPAREN"
TT_RPAREN="RPAREN"


class Token:
    def __init__(self,type_,value=None) -> None:
        self.type=type_
        self.value=value
    
    def __repr__(self) -> str:
        if self.value:return  f"{self.type}:{self.value}"
        return f"{self.type}"

class Lexer:
    def __init__(self,fn,text) -> None:
        self.text=text
        self.fn=fn
        self.ptr=0

    def make_token(self):
        tokens=[]
        while self.ptr<len(self.text):
            char=self.text[self.ptr]
            if char=="+":
                tokens.append(Token(TT_PLUS))
            elif char=="-":
                tokens.append(Token(TT_MINUS))
            elif char=="*":
                tokens.append(Token(TT_MUL))
            elif char=="/":
                tokens.append(Token(TT_DIV))
            elif char=="%":
                tokens.append(Token(TT_MOD))
            elif char=="(":
                tokens.append(Token(TT_LPAREN))
            elif char==")":
                tokens.append(Token(TT_RPAREN))
            elif char in digits:
                self.make_number()

            self.ptr+=1
        return tokens

    def make_number(self):
        ptr_ini=self.ptr

############################
#RUN



def run(fn,text):
    lexer=Lexer(fn,text)
    token,error=lexer.make_token()

a=3
b=a
a+=2
print(b,a)