#include <stdio.h>

 struct Token
    {
        char type[20];
    };

char tok_name[][2]={
    ".",
    ":",
    ",",
    "?",
    "-=",
    "+=",
    "!",
    "!=",
    "<=",
    ">=",
    "<",
    ">",
    "&"
    "|"
    "=",
    "==",
    "^",
    ";",
    ">>",
    "<<",
    "+",
    "-",
    "*",
    "/",
    "//",
    "%",
    "(",
    ")",
    "[",
    "]",
    "{",
    "}"
};

struct Token tokens[];
int main(){
   
    
    char text[] = "saluyt les ";
    
    return 0;
}