from lark import Lark,tree
from lark.lexer import Lexer, Token
import sys

grammar = '''
start: program
program: function_decl_list main_function
function_decl_list: function_decl*
function_decl: "func"datatype IDENTIFIER "(" params ")" "{" stmts "}"
main_function: "func" "num" "main" "(" ")" "{" stmts "}"
params: [param ("," param)*]? 
param: datatype IDENTIFIER  | datatype "(" ")" IDENTIFIER  | datatype "[" "]" IDENTIFIER  | datatype "{" "}" IDENTIFIER 
datatype: "num" | "flag" | "str" | "void" | "char"
stmts: ((stmt ";" | function_decl | floop  |  wloop  |  if_cond  |  try  |  catch | iter";" ) stmts?)*
stmt: l | "continue" | "break" | "return" | "return" IDENTIFIER | "return" CONST |(IDENTIFIER "[" IDENTIFIER "]" "=" exp ) | l1

try : "try"  "{"  stmts  "}" 
catch :            "catch"  "{"  stmts  "}" 
throw : "throw"  "("  VAL1  ")" 
floop : "floop"  "("  assign  ";"  cond  ";"  iter  ")"  "{"  stmts  "}" 
wloop : "wloop"  "("  cond  ")"  "{"  stmts  "}" 
assign : "cook" datatype IDENTIFIER "=" CONST | "cook" datatype IDENTIFIER "=" exp | IDENTIFIER "=" CONST | IDENTIFIER "=" exp | IDENTIFIER "++" | IDENTIFIER "--"
cond : "!" c | c

binary_exp: binary_exp binary_op binary_exp
          | "(" binary_exp ")" | "!"binary_exp
          | "true"
          |"false"
          |IDENTIFIER

binary_op: "||" | "&&" | "==" | "!=" 


c : "(" c ")" | exp comp exp | "true" | "false" | c "||" c | c "&&" c
comp : ">=" | "<=" | "!=" | ">" | "<" | "==" | 
exp : (IDENTIFIER | IDENTIFIER "[" exp "]" | CONST | "(" exp ")" | exp op exp)* 
e1: ((datatype IDENTIFIER  | datatype "(" ")" IDENTIFIER  | datatype "[" "]" IDENTIFIER  | datatype "{" "}" IDENTIFIER ) e2*)*
e2: ("," e1)
op: "+" | "-" | "*" | "/" | "#" | "&" | "|" | "^" | "%"
if_cond : "if" "(" cond ")" "{" stmts "}" else_if_cond?
else_if_cond : ("else_if" "(" cond ")" "{" stmts "}" else_if_cond?)? | else_cond
else_cond : ("else" "{" stmts "}")?
iter: IDENTIFIER "=" exp | IDENTIFIER "++" | IDENTIFIER "--"
print : (IDENTIFIER ("," print)*  | val7 ("," print)* | IDENTIFIER "[" exp "]" ("," print)* )*
l1: "cook" "num" IDENTIFIER "=" "len" "(" IDENTIFIER ")"
    | "cook" datatype IDENTIFIER "=" "headof" "(" IDENTIFIER ")"
    | "cook" datatype IDENTIFIER "=" "tailof" "(" IDENTIFIER ")"
    | "cook" "num" IDENTIFIER "=" VAL2 ":" ":" IDENTIFIER
    | IDENTIFIER "=" "len" "(" IDENTIFIER ")"
    | IDENTIFIER "=" "headof" "(" IDENTIFIER ")"
    | IDENTIFIER "=" "tailof" "(" IDENTIFIER ")"
    | IDENTIFIER "=" VAL2 ":" ":" IDENTIFIER
    | "cook" datatype IDENTIFIER "=" IDENTIFIER "[" VAL2 "]"
    | IDENTIFIER "=" IDENTIFIER "[" VAL2 "]"

l: "cook" "num" IDENTIFIER "=" (VAL2 | exp)
  | "cook" "str" IDENTIFIER "=" VAL1 
    | "cook" "flag" IDENTIFIER "=" VAL3 
    | "cook" "char" IDENTIFIER "=" VAL9
    | "cook" "num" IDENTIFIER "=" "{" val4 "}" 
    | "cook" "str" IDENTIFIER "=" "{" val5 "}"
    | "cook" "flag" IDENTIFIER "=" "{" val6 "}"
    | "cook" "char" IDENTIFIER "=" "{" val10 "}"
    | "cook" IDENTIFIER "=" "[" val7 "]"
    | "cook" IDENTIFIER "=" "(" val7 ")"
    | "cook" datatype IDENTIFIER
    | "cook" datatype IDENTIFIER "[" IDENTIFIER "]"
    | "cook" datatype IDENTIFIER "[" (VAL2 | exp) "]"
    | IDENTIFIER "=" (VAL1 | VAL3 | VAL9 | VAL2 | exp)
    | IDENTIFIER "=" "[" val7 "]"
    | IDENTIFIER "=" IDENTIFIER "[" IDENTIFIER "]"
    | IDENTIFIER "=" IDENTIFIER "[" (VAL2 | exp) "]"
    | IDENTIFIER "=" IDENTIFIER "(" val7 ")"
    | "cook" datatype IDENTIFIER "=" (VAL2 | exp)
    | "cook" datatype IDENTIFIER "=" VAL3
    | "cook" datatype IDENTIFIER "=" "[" val7 "]"
    | "cook" datatype IDENTIFIER "=" IDENTIFIER "[" IDENTIFIER "]"
    | "cook" datatype IDENTIFIER "=" IDENTIFIER "[" (VAL2 | exp) "]"
    | "cook" datatype IDENTIFIER "=" IDENTIFIER "(" print ")"
    | "cook" datatype IDENTIFIER "=" IDENTIFIER "("  ")"
    | "echo" "(" print ")"
    | throw 
    | "cook" datatype IDENTIFIER "=" exp
    
CONST : VAL2 | VAL1 | "true" | "false"

VAL1: /"[^"]*"/
NUM1 : /[1-9]/
NUM2 : /[0-9]*/
VAL2: /[1-9][0-9]*/ | "0" 

VAL3 : "true" | "false"

val4 : ((VAL2 | exp) ( "," (VAL2 | exp) )*)*

val5 : (VAL1 ( "," VAL1 )*)*

val6 : (VAL3 ( "," VAL3 )*)*

val7 : ((VAL1 | VAL2 | VAL3 |  "len" "(" IDENTIFIER ")" | "headof" "(" IDENTIFIER ")" | "tailof" "(" IDENTIFIER ")" ) ( "," (VAL1 | VAL2 | VAL3 |  "len" "(" IDENTIFIER ")" | "headof" "(" IDENTIFIER ")" | "tailof" "(" IDENTIFIER ")" ) )*)*
VAL9 : /'([A-Za-z])'/
val10 : (VAL9 ( "," VAL9 )*)*
IDENTIFIER: /[a-zA-Z_][a-zA-Z0-9_]*/

%import common.WS
%ignore WS
'''


if __name__ == '__main__':
    
    file=sys.argv[1]
    
    # Take the contents of the file and give it as input to the parser
    sentence = open(file, 'r',encoding="utf8").read()
    
    parser = Lark(grammar, start='start', parser='lalr' ,debug=True)
    print(parser.parse(sentence).pretty())

