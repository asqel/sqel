####################################
#CONSTANTS

DIGITS="1234567890"


#######################################
#ERROR


class Error:
    def __init__(self,error_name,details):
        self.error_name=error_name
        self.details=details
        
    def as_string(self):
        result=f'{self.error_name}:{self.details}'
        return result
    
class IllegalCharError(Error):
    def __init__(self,details):
        super().__init__("Illegal Character",details)


########################################
#TOKENS


TT_INT="TT_INT"
TT_FLOAT="FLOAT"
TT_PLUS="PLUS"
TT_MINUS="MINUS"
TT_DIV="DIV"
TT_MUL="MUL"
TT_LPAREN="LPAREN"
TT_RPAREN="RPAREN"


class Token:
    def __init__(self,type_,value) -> None:
        self.type=type_
        self.value=value
    
    def __repr__(self) -> str:
        if self.value:return  f"{self.type}:{self.value}"
        return f"{self.type}"

################################
#LEXER
    
class lexer:
    def __init__(self,text) -> None:
        self.text=text
        self.pos=-1
        self.current_char=None
        self.advance()
    def advance(self):
        self.pos+=1
        self.current_char=self.text[self.pos]  if self.pos<len(self.text) else None
    
    def make_tokens(self):
        tokens=[]
        
        while self.current_char!=None:
            if self.current_char in " \t":
                self.advance()
            elif self.current_char in DIGITS:
                tokens.apppend(self.make_number())
            elif self.current_char=="+":
                tokens.append(TT_PLUS)
                self.advance()
            elif self.current_char=="-":
                tokens.append(TT_MINUS)
                self.advance()
            elif self.current_char=="*":
                tokens.append(TT_MUL)
                self.advance()
            elif self.current_char=="/":
                tokens.append(TT_DIV)
                self.advance()
            elif self.current_char=="(":
                tokens.append(TT_LPAREN)
                self.advance()
            elif self.current_char==")":
                tokens.append(TT_RPAREN)
                self.advance()
            else:
                char=self.current_char
                self.advance()
                return [], IllegalCharError("'"+char+"'")
        
        return tokens,None
    def make_number(self):
        num_str=''
        dot_count=0
        
        while self.current_char!=None and self.current_char in DIGITS+".": 
            if self.current_char==".":
                if self.current_char==1:break
                dot_count+=1
                num_str+="."
            else:
                num_str+=self.current_char
                
        if dot_count==0:
            return Token(TT_INT,int(num_str))
        else:
            return Token(TT_FLOAT,float(num_str))
        
        
        
        
############################
#RUN

def run(text):
    