to run a programm put the code in the main.qel and run parser.py


types:  
    ount  
    booulean  
    string  
    floap(not suported)  
    comp(not supported)  

string :" " or ' '   
ount : just a number  
boolean : 1b or 0b  

and: &  
or : |  

less than= <  
greater than = >  
less equal = <=  
greater equal = >=  

equal = ==  
not equal = !=  


pow : ^  
mul : *  
div : /  
euclidiv(floor div) : //  
modulo : %  

add : +  
sub : -  

r shift bit : >>  
l shift bit : <<  


functions:  
    to_ount(x): converte x to a ount  
    to_string(x): converte x to a string  
    random(x): return a random number between 0(included) and x(included)  
    open_window(x): print('pourquoi')  
    import(x): import file x (x must be asbolute path of file)  
    print(x): print x to prompt  
    input():read prompt and returned it to a string  
    not(x): reverte boolean value of x  
    get_path(): return the absolute path of the file in a string
    get_folder(x): return the absolute path of the parent folder of the path x in a string
    time(): return time in floap

if(boolean value){  
    instructions  
}  
while(boolean value){  
    instructions  
}  

ex:  
    if(a>0){  
        print(2/a)  
    }  


operation order:  
    1:pow(^)  
    2:mul(*),div(/),euclidiv(//),modulo(%)  
    3:add(+),sub(-)  
    4:r shift(>>),l shift(<<)  
    5:less than(<),greater than(>),less equal(<=),greater equal(>=),equal(==),not equal(!=)  
    6:and(&),or(|)  

delcare variable:  
    Type Name = Value;  

change variable value::  
    Name=Value;  

to make commentary:  
    /* this a commentary */  