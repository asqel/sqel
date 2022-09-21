text=""
validname="azertyuiopqsdfghjklmwxcvbn"
validname+=validname.upper()+"_"
vars={}
num="1234567890"
op="+-*/"


def expr_analyser(t):
    s=[""]
    if "("not in t:
        for i in t:
            if i in num:
                if s[-1] in op:
                    s.append(i)
                else:
                    s[-1]+=i
            elif i in op:
                s.append(i)
        while s[0].strip()=="" or s[0].strip()==" ":
            s.pop(0)
        a=[]
        for i in range(1,len(t)):
            if t[i]=="*":
                a.append(int(t[i-1])*int(t[i+1]))
            elif t[i]=="/":
                a.append(int(t[i-1])/int(t[i+1]))
            else:
                a.append(t[i])
        s=[]
        for i in range(1,len(a)):
            if t[i]=="+":
                s.append(int(t[i-1])+int(t[i+1]))
            elif t[i]=="/":
                s.append(int(t[i-1])-int(t[i+1]))
        return s[0]
    
def create_var(text,row,col):
    global vars
    if col==0 and text[row][col]=="l":
        if text[row][col+1]=="e" and text[row][col+2]=="t":
            col+=3
            if text[row][col]!=" ":
                raise Exception(f"error on line : {row} and collumne : {col}")
            while text[row][col]==" ":
                col+=1
            varname=""
            while text[row][col] in validname:
                varname+=text[row][col]
                col+=1
            while text[row][col]==" ":
                col+=1
            if text[row][col]!="=":
                raise Exception(f"variable can't have space in them row : {row} and collumne : {col}")
            vars[varname]=expr_analyser(text[row][col+1:])


text="""
let a=3+3;
let b=3+4;
print( a  , b )


"""
text=text.split(";")
for i in range(0,len(text)):
    while text[i].startswith("\n"):
        text[i]=text[i][1:]
    while text[i].endswith("\n"):
        text[i]=text[i][:-1]
    if text[i].startswith("let"):
        create_var(text,i,0)
    if text[i].startswith("print(") and text[i].endswith(")"):
        for i in text[i].split("print(")[1].split(")")[0].split(","):
            print(vars[i.strip()])
print(vars)






