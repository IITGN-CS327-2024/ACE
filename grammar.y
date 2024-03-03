%{
#include <stdio.h>
#include <stdlib.h>
%}

%token FUNC ID NUM_FLAG STR_FLAG BOOL MAIN_TOKEN CONST FLAG NUM VAL1 _digit
%token FLOOP WLOOP COOK GE LE NEQ GT LT IF ELSE ELSE_IF AND OR INC DEC TRUE FALSE ECHO
%left ADDOP SUBOP
%left MULOP DIVOP
%left AND OR
%left EQ NEQ LT LE GT GE
%left '(' ')'
%left ','
%left '='
%left IF ELSE WHILE FOR RETURN BREAK CONTINUE '{' '}'


%start program

%%

program:
    | func_decl
    | main_func
    ;

func_decl:
    FUNC ID '(' e1 ')' '{' stmts '}'
    ;

main_func:
    FUNC MAIN_TOKEN '(' e1 ')' '{' stmts '}'
    ;

e1:
    dt ID e2
    | /* empty */
    ;

e2: 
    ',' e1
    | /* empty */
    ;

dt:
    NUM_FLAG
    | FLAG
    | STR_FLAG
    ;

stmts:
    stmt ';' stmts
    | wloop stmts
    | floop stmts
    | if_cond stmts
    | /* empty */
    ;

floop:
    FLOOP '(' assign ';' cond ';' iter ')' '{' stmts '}'
    ;

wloop:
    WLOOP '(' cond ')' '{' stmts '}'
    ;

assign:
    dt ID '=' CONST
    | dt ID '=' ID
    | ID '=' CONST
    | ID '=' ID
    | ID INC
    | ID DEC
    ;

cond:
    '!' c
    | c
    ;

c:
    '(' c ')'
    | exp comp exp
    | c AND c
    | c OR c
    | FLAG
    | TRUE
    | FALSE
    ;

comp:
    GE
    | LE
    | NEQ
    | GT
    | LT
    ;

exp:
    ID
    | NUM
    | exp op exp
    | '(' exp ')'
    | /*empty*/
    ;

op:
    '+'
    | '-'
    | '*'
    | '/'
    ;

if_cond:
    IF '(' cond ')' '{' stmts '}' else_if_cond
    ;

else_if_cond:
    ELSE_IF '(' cond ')' '{' stmts '}' else_cond
    | /* empty */
    ;

else_cond:
    ELSE '{' stmts '}'
    | /* empty */
    ;

iter:
    ID '=' exp
    | ID INC
    | ID DEC
    ;

stmt:
    l
    | /* empty */
    ;

l:
    COOK STR_FLAG ID '=' VAL1
    | COOK NUM_FLAG ID '=' VAL2
    | COOK FLAG ID '=' VAL3
    | COOK NUM_FLAG ID '=' '{' VAL4 '}'
    | COOK STR_FLAG ID '=' '{' VAL5 '}'
    | COOK FLAG ID '=' '{' VAL6 '}'
    | COOK ID '=' '[' VAL7 ']'
    | COOK ID '=' '(' VAL7 ')'
    | COOK STR_FLAG ID
    | COOK FLAG ID
    | COOK dt ID
    | COOK ID
    | ID '=' VAL1
    | ID '=' VAL2
    | ID '=' VAL3
    | ID '=' '[' VAL7 ']'
    | ECHO '(' ')'
    ;


VAL2: NUM_FLAG VAL2_T
    | '0'
    ;
VAL2_T: _digit VAL2_T
    | /* empty */
    ;
VAL3:
    TRUE
    | FALSE
    ;

VAL4:
    VAL2 VAL4_T
    | /* empty */
    ;
VAL4_T:
    ',' VAL4
    | /* empty */
    ;
VAL5:
    VAL1 VAL5_T
    | /* empty */
    ;
VAL5_T:
    ',' VAL5
    | /* empty */
    ;
VAL6:
    VAL3 VAL6_T
    | /* empty */
    ;

VAL6_T:
    ',' VAL6
    | /* empty */
    ;

VAL7:
    VAL1 ',' VAL7
    | VAL2 ',' VAL7
    | VAL3 ',' VAL7
    | VAL1
    | VAL2
    | VAL3
    ;

%%

// Lexical part
_digit : [0-9];
VAL1: '\"' [^'\"'] '\"'
    ;
NUM_FLAG:   [1-9]
    ;

STR_FLAG: "str"
    ;

ID: [a-zA-Z_]+[a-zA-Z_0-9]*
    ;
