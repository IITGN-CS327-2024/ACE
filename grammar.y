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
    | dt ID e1
    | ',' e1
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
    | ID
    | FLAG
    | NUM
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
    | exp f1
    | '(' exp ')'
    ;

f1:
    op exp f1
    | /* empty */
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
    | wloop
    | floop
    | if_cond
    | /* empty */
    ;

l:
    COOK STR_FLAG ID '=' VAL1
    | COOK NUM_FLAG ID '=' VAL1
    | COOK FLAG ID '=' VAL1
    | COOK NUM_FLAG ID '=' '{' VAL1 '}'
    | COOK STR_FLAG ID '=' '{' VAL1 '}'
    | COOK FLAG ID '=' '{' VAL1 '}'
    | COOK dt ID '=' '[' VAL1 ']'
    | COOK ID '=' '(' VAL1 ')'
    | COOK STR_FLAG ID
    | COOK NUM_FLAG ID
    | COOK FLAG ID
    | COOK NUM_FLAG ID
    | COOK STR_FLAG ID
    | COOK FLAG ID
    | COOK dt ID
    | COOK ID
    | ID '=' VAL1
    | ID '=' VAL1
    | ID '=' VAL1
    | ID '=' '{' VAL1 '}'
    | ID '=' '{' VAL1 '}'
    | ID '=' '{' VAL1 '}'
    | dt ID '=' '[' VAL1 ']'
    | ID '=' '(' VAL1 ')'
    | ECHO '('  ')'
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
    VAL1 ',' VAL4
    | VAL2 ',' VAL4
    | VAL3 ',' VAL4
    | VAL1
    | VAL2
    | VAL3
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
VAL1: '\"' [^'\"] '\"'
    ;
NUM_FLAG:   [1-9]
    ;
