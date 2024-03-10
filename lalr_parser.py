from lark import Lark,tree,ast_utils
from lark.lexer import Lexer, Token
import sys

grammar = '''
program: function_decl_list 
function_decl_list: function_decl 
function_decl: "func" datatype IDENTIFIER "(" params ")" "{" stmts "}" function_decl | main_function
main_function: "func" "num" "main" "(" ")" "{" stmts "}" 
params: [param ("," param)*]? 
param: datatype IDENTIFIER  | datatype "(" ")" IDENTIFIER  | datatype "[" "]" IDENTIFIER  | datatype "{" "}" IDENTIFIER 
datatype: "num" | "flag" | "str" | "void" | "char"
stmts: (stmt ";" | function_decl | floop  |  wloop  |  if_cond  |  try  |  catch | iter";" )*
stmt: "continue" | "break" | "return" | "return" IDENTIFIER | "return" CONST |(IDENTIFIER "[" IDENTIFIER "]" "=" exp ) | l1

try : "try"  "{"  stmts  "}" 
catch :  "catch"  "{"  stmts  "}" 
throw : "throw"  "("  VAL1  ")" 
floop : "floop"  "("  assign  ";"  cond  ";"  iter  ")"  "{"  stmts  "}" 
wloop : "wloop"  "("  cond  ")"  "{"  stmts  "}" 
assign : "cook" datatype IDENTIFIER "=" CONST | "cook" datatype IDENTIFIER "=" exp | IDENTIFIER "=" CONST | IDENTIFIER "=" exp | IDENTIFIER "++" | IDENTIFIER "--"
cond : "!" c | c

c : "(" c ")" | (exp | "len" "(" IDENTIFIER ")" | "headof" "(" IDENTIFIER ")" | "tailof" "(" IDENTIFIER ")" | VAL2 | VAL1) comp (exp | "len" "(" IDENTIFIER ")" | "headof" "(" IDENTIFIER ")" | "tailof" "(" IDENTIFIER ")" | VAL2 | VAL1) | "true" | "false" | c "||" c | c "&&" c | exp
comp : ">=" | "<=" | "!=" | ">" | "<" | "=="  
exp : (IDENTIFIER | IDENTIFIER "[" (VAL2 | IDENTIFIER) "]" | "(" exp ")" | (exp | "len" "(" IDENTIFIER ")" | "headof" "(" IDENTIFIER ")" | "tailof" "(" IDENTIFIER ")" | VAL2) op (exp| "len" "(" IDENTIFIER ")" | "headof" "(" IDENTIFIER ")" | "tailof" "(" IDENTIFIER ")" | VAL2))?
e1: ((datatype IDENTIFIER  | datatype "(" ")" IDENTIFIER  | datatype "[" "]" IDENTIFIER  | datatype "{" "}" IDENTIFIER ) e2*)*
e2: ("," e1)
op: "+" | "-" | "*" | "/" | "#" | "&" | "|" | "^" | "%"

if_cond : "if" "(" cond ")" "{" stmts "}" (else_if_cond | else_cond)?
else_if_cond : "else_if" "(" cond ")" "{" stmts "}" (else_if_cond | else_cond)?
else_cond : "else" "{" stmts "}"
int_exp : VAL2 | "len" "(" IDENTIFIER ")" | "headof" "(" IDENTIFIER ")" | "tailof" "(" IDENTIFIER ")" | exp
iter: stmt | IDENTIFIER "++" | IDENTIFIER "--"
print : ((IDENTIFIER | CONST) ("," print)?  |  ("," print)? | (IDENTIFIER | CONST) "[" (exp | VAL2) "]" ("," print)? )? 

l1: "cook" datatype IDENTIFIER "=" int_exp
    | "cook" datatype IDENTIFIER "=" VAL2 ":" ":" IDENTIFIER
    | IDENTIFIER "=" "len" "(" IDENTIFIER ")"
    | IDENTIFIER "=" "headof" "(" IDENTIFIER ")"
    | IDENTIFIER "=" "tailof" "(" IDENTIFIER ")"
    | IDENTIFIER "=" VAL2 ":" ":" IDENTIFIER
    | l

l:"cook" datatype IDENTIFIER "=" "{" val11 "}" 
    | "cook" IDENTIFIER "=" "[" val7 "]"
    | "cook" IDENTIFIER "=" "(" val7 ")"
    | "cook" datatype IDENTIFIER
    | "cook" datatype IDENTIFIER "[" IDENTIFIER "]"
    | "cook" datatype IDENTIFIER "[" int_exp "]"
    | IDENTIFIER "=" "[" val7 "]"
    | IDENTIFIER "=" (exp | CONST)
    | IDENTIFIER "=" IDENTIFIER "[" int_exp "]"
    | IDENTIFIER "=" IDENTIFIER "(" val7 ")"
    | "cook" datatype IDENTIFIER "=" ( VAL3 | VAL1 | VAL9 )
    | "cook" datatype IDENTIFIER "=" "[" val7 "]"
    | "cook" datatype IDENTIFIER "=" IDENTIFIER "[" int_exp "]"
    | "cook" datatype IDENTIFIER "=" IDENTIFIER "(" val7 ")"
    | "cook" datatype IDENTIFIER "=" IDENTIFIER "("  ")"
    | "echo" "(" print ")"
    | throw 

    
CONST : VAL2 | VAL1 | "true" | "false" | VAL9

VAL1: /"[^"]*"/
NUM1 : /[1-9]/
NUM2 : /[0-9]*/
VAL2: /[1-9][0-9]*/ | "0" 

VAL3 : "true" | "false"

val4 : ((VAL2 ) ( "," (VAL2) )*)?
val11: ((VAL1 | VAL3 | VAL2 | VAL9) ( "," (VAL1 | VAL3 | VAL2 | VAL9) )*)?
val5 : (VAL1 ( "," VAL1 )*)?

val6 : (VAL3 ( "," VAL3 )*)?

val7 : ((VAL1 | VAL2 | VAL3 |  IDENTIFIER | VAL9 |  IDENTIFIER "[" exp "]" | "len" "(" IDENTIFIER ")" | "headof" "(" IDENTIFIER ")" | "tailof" "(" IDENTIFIER ")" ) ( "," (VAL1 | VAL2 | VAL3 | IDENTIFIER | VAL9 |  IDENTIFIER "[" exp "]" | "len" "(" IDENTIFIER ")" | "headof" "(" IDENTIFIER ")" | "tailof" "(" IDENTIFIER ")" ) )*)?
VAL9 : /'([A-Za-z])'/
val10 : (VAL9 ( "," VAL9 )*)?
IDENTIFIER: /[a-zA-Z_][a-zA-Z0-9_]*/
%import common.WS
%ignore WS
%import common.WS_INLINE
%ignore WS_INLINE
'''


if __name__ == '__main__':
    
    file=sys.argv[1]
    
    # Take the contents of the file and give it as input to the parser
    sentence = open(file, 'r',encoding="utf8").read()
    # sentence+="$"
    # print(sentence)
    parser = Lark(grammar, start='program', parser='lalr')
    print(parser.parse(sentence).pretty())