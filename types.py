class ComplexNumber:
    def __init__(self,re,im=0):
        self.re=re
        self.im=im

    def __add__(self,other):
        re1=self
        im1=0
        if isinstance(self,ComplexNumber):
            re1=self.re
            im1=self.im

        re2=self
        im2=0
        if isinstance(other,ComplexNumber):
            re2=other.re
            im2=other.im

        return ComplexNumber(re1+re2,im1+im2)
    
    def __sub__(self,other):
        if isinstance(self,int)or  isinstance(self,float) :
            re1=self
        im1=0
        if isinstance(self,ComplexNumber):
            re1=self.re
            im1=self.im

        re2=self
        im2=0
        if isinstance(other,ComplexNumber):
            re2=other.re
            im2=other.im

        return ComplexNumber(re1-re2,im1-im2)