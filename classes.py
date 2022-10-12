from lexer import *
class Error:
    def __init__(self,pos_start,pos_end,error_name,details):
        self.pos_start=pos_start
        self.pos_end=pos_end
        self.error_name=error_name
        self.details=details
        self.type="Error"
        self.line_start=None
        self.line_end=None
        
    def isTok(self):return 0
        
    def __repr__(self):
        result=f'{self.error_name}, file:{self.details}'
        result+=f", from {self.pos_start} to {self.pos_end}"
        return result
  
class  string:
    def __init__(self,s) -> None:
        self.val=str(s)
    def __add__(self,o):
        return string(self.val+str(o))
    def __str__(self):
        return str(self.val)
    def __mul__(s,o):
        if isinstance(o,ount):
            return string(s.val*o.val)
        
    def __bool__(s):
        return bool(s.val)    
    
    
class Null:
    def __init__(self) -> None:
        self.type=None
        self.value=None
        self.line_start=None
        self.line_end=None
    def __eq__(s,o):
        return o==None


#floap(float)     //    ount(int)     //       comp(complex)   //boolean(bool)
class floap:
    def __init__(self,n) -> None:
        if "__floap__"in dir(n) and str(type(n.__floap__))=="<class 'method'>":
            self.val=float(n.__floap__())
        elif isinstance(n,(bool,float,int,ount,boolean,floap,str)):
            self.val=float(n)

    def __pow__(s,o):
        return floap(s.val**o.val)
    def __float__(s):
        return float(s.val)
    def __str__(s):
        return str(s.val)

    def __int__(s):
        return int(s.val)


class comp:
    def __init__(self,r,i=0) -> None:
        if "__comp__" in dir(r) and str(type(r.__comp__))=="<class 'method'>":
            a=r.__comp__()
            self.re=float(a[0])
            self.im=float(a[1])
        elif isinstance(r,(bool,float,int,str)) and  isinstance(i,(bool,float,int,str)):
            self.re=float(r)
            self.im=float(i)
class ount:
    
    def __init__(s,n):
        if "__ount__"in dir(n) and str(type(n.__ount__))=="<class 'method'>":
            s.val=n.__ount__()
        elif isinstance(n,(bool,float,int,str)):
            s.val=int(n)
    def __str__(s):return str(s.val) if s.val!=0 else str("0")
    def __int__(s):return int(s.val)
    def __float__(s):return float(s.val)
    def __ount__(s):return s
    def __floap__(s):return s.val
    def __boolean__(s):return bool(s)
    def __comp__(s):return s.val,0 
    def  __rshift__(a,b):
        if  isinstance(b,ount):return ount(a.val>>b.val)
        if "__ount__"in dir(b) and str(type(b.__out__))=="<class 'method'>":
            return ount(a.val>>b.__ount__().val)
        else:
            return Error(None,None,f"unsuported operand '>>' type between {type(a)} and {type(b)}")
    def  __lshift__(a,b):
        if   isinstance(b,ount):return ount(a.val<<b.val)
        if "__ount__"in dir(b) and str(type(b.__out__))=="<class 'method'>":
            return ount(a.val<<b.__ount__().val)
        else:
            return Error(None,None,f"unsuported operand '<<' type between {type(a)} and {type(b)}")
    def __add__(a,b):
        if   isinstance(b,ount):return ount(a.val+b.val)
        if isinstance(b,tuple(num_lvl.keys())):
            t=max(num_lvl[type(b)],num_lvl[type(a)])
            t=lvl_num[t]
            a=t(a)
            b=t(b)
            return a+b
        if "__ount__"in dir(b) and str(type(b.__out__))=="<class 'method'>":
            return ount(a.val+b.__ount__().val)
        else:
            return Error(None,None,f"unsuported oper '+' and type between {type(a)} and {type(b)}",None)
    def __sub__(a,b):
        if   isinstance(b,ount):return ount(a.val-b.val)
        if isinstance(b,tuple(num_lvl.keys())):
            t=max(num_lvl[type(b)],num_lvl[type(a)])
            t=lvl_num[t]
            a=t(a)
            b=t(b)
            return a-b
        if "__ount__"in dir(b) and str(type(b.__out__))=="<class 'method'>":
            return ount(a.val-b.__ount__().val)
        else:
            return Error(None,None,f"unsuported oper '-' and type between {type(a)} and {type(b)}")
    def __mul__(a,b):
        if   isinstance(b,ount):return ount(a.val*b.val)
        if isinstance(b,tuple(num_lvl.keys())):
            t=max(num_lvl[type(b)],num_lvl[type(a)])
            t=lvl_num[t]
            a=t(a)
            b=t(b)
            return a*b
        if "__ount__"in dir(b) and str(type(b.__out__))=="<class 'method'>":
            return ount(a.val*b.__ount__().val)
        else:
            return Error(None,None,f"unsuported oper '*' and type between {type(a)} and {type(b)}",None)
    def __truediv__(a,b):
        if   isinstance(b,ount):return floap(a.val/b.val) if b.val!=0 else Error(None,None,"division by zero",None)
        if isinstance(b,tuple(num_lvl.keys())):
            t=max(num_lvl[type(b)],num_lvl[type(a)])
            if t<3:t=3
            t=lvl_num[t]
            a=t(a)
            b=t(b)
            return a/b
        if "__ount__"in dir(b) and str(type(b.__out__))=="<class 'method'>":
            return floap(a.val/b.__ount__().val)
        else:
            return Error(None,None,f"unsuported oper '/' and type between {type(a)} and {type(b)}")
    def __floordiv__(a,b):
        if   isinstance(b,ount):return ount(a.val//b.val) if b.val!=0 else Error(None,None,"floor division by zero",None)
        if isinstance(b,tuple(num_lvl.keys())):
            t=max(num_lvl[type(b)],num_lvl[type(a)])
            if t!=2:t=2
            t=lvl_num[t]
            a=t(a)
            b=t(b)
            return a//b
        if "__ount__"in dir(b) and str(type(b.__out__))=="<class 'method'>":
            return ount(a.val//b.__ount__().val)
        else:
            return Error(None,None,f"unsuported oper '//' and type between {type(a)} and {type(b)}")
    def __mod__(a,b):
        if   isinstance(b,ount):return ount(a.val%b.val) if b.val!=0 else Error(None,None,"modulo by zero",None)
        if isinstance(b,tuple(num_lvl.keys())):
            t=max(num_lvl[type(b)],num_lvl[type(a)])
            if t!=2 and t!=4:t=2
            t=lvl_num[t]
            a=t(a)
            b=t(b)
            return a%b
        if "__ount__"in dir(b) and str(type(b.__out__))=="<class 'method'>":
            return ount(a.val%b.__ount__().val)
        else:
            return Error(None,None,f"unsuported oper '%' and type between {type(a)} and {type(b)}")
    def __pow__(a,b):
        if isinstance(b,ount):
            return ount(a.val**b.val) if not(a.val==0 and b.val==0) else Error(None,None,"zero pow zero",None)
        if isinstance(b,tuple(num_lvl.keys())):
            t=max(num_lvl[type(b)],num_lvl[type(a)])
            print(t)
            t=lvl_num[t]
            a=t(a)
            b=t(b)
            return a**b
        if "__ount__"in dir(b) and str(type(b.__out__))=="<class 'method'>":
            return ount(a.val**b.__ount__().val)
        else:
            return Error(None,None,f"unsuported oper '%' and type between {type(a)} and {type(b)}")
    def __bool__(s):
        return False if s.val==0 else True
    def __eq__(s,o):
        if o==None:
            return False
        if isinstance(o,(boolean,ount,floap)):
            return s.val==o.val
        else:
            return Error(None,None,f"unsuported operand '==' and type between {type(s)} and {type(o)}",None)
    def __le__(a,b):
        if isinstance(b,(boolean,ount,floap)):
            return a.val<=b.val
        else:
            return Error(None,None,f"unsuported operand '==' and type between {type(a)} and {type(b)}",None)
    def __ge__(a,b):
        if isinstance(b,(boolean,ount,floap)):
            return a.val>=b.val
        else:
            return Error(None,None,f"unsuported operand '==' and type between {type(a)} and {type(b)}",None)
    def __gt__(a,b):
        if isinstance(b,(boolean,ount,floap)):
            return a.val>b.val
        else:
            return Error(None,None,f"unsuported operand '==' and type between {type(a)} and {type(b)}",None)
    def __lt__(a,b):
        if isinstance(b,(boolean,ount,floap)):
            return a.val>b.val
        else:
            return Error(None,None,f"unsuported operand '==' and type between {type(a)} and {type(b)}",None)


class boolean(ount):
    def __init__(self,n) -> None:
        super().__init__(bool(n))
    def __ount__(s):
        return s.val
    def __bool__(s):
        return super().__bool__()
    def __str__(s):
        return str(bool(s))
    
num_lvl={boolean:2,ount:2,floap:3,comp:4}#toute les operation mathematique faite
lvl_num={2:ount,3:floap,4:comp}#sur des bool les transforme en ount ou plus 
