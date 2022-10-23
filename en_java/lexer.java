package en_java;

import java.util.HashMap;

public class lexer{
    public static final int ptr=0;
    public static final token[] tokens={};
    final static public HashMap<String,String> TOKENS=new HashMap<String,String>(){{
        put("+","PLUS");
        put("-","MINUS");
    }} ;

    public static token make_number(){
        return null;
    }

    public static token[] lexe(String text){
        while(ptr<tokens.length){

        }


        return tokens;
        
    }
}