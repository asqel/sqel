from typing import overload
from lexer import *


class floap:
    def __init__(self,n) -> None:
        self.val=float(n)
    
    def __add__(s,o):
        if isinstance(s,floap) and isinstance(o,floap):
            return floap(o.val+s.val)
    def __sub__(s,o):
        if isinstance(s,floap) and isinstance(o,floap):
            return floap(s.val-o.val)
        
    def __mul__(s,o):
        if isinstance(s,floap) and isinstance(o,floap):
            return floap(s.val*o.val)
    
    def __truediv__(s,o):
        if isinstance(s,floap) and isinstance(o,floap):
            if o.val==0:return Error(None,None,"Division by 0",None)
            return floap(s.val/o.val)
    
    def __floordiv__(s,o):
        if isinstance(s,floap) and isinstance(o,floap):
            return floap(s.val//o.val)
        
    def __mod__(s,o):
        if isinstance(s,floap) and isinstance(o,floap):
            return floap(s.val%o.val)
        
    def __pow__(s,o):
        if isinstance(s,floap) and isinstance(o,floap):
            return floap(s.val**o.val)
    def __str__(s):
        if isinstance(s,ount):
            return str(int(s.val))
        return str(s.val)
        
class ount(floap):
    def __init__(self, n) -> None:
        super().__init__(int(n))