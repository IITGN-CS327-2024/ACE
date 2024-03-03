package main

import (
        "fmt"
        
)

%%{ 
    machine thermostat;
    write data;
    access lex.;
    variable p lex.p;
    variable pe lex.pe;
}%%

type lexer struct {
    data []byte
    p, pe, cs int
    ts, te, act int
}

func newLexer(data []byte) *lexer {
    lex := &lexer{ 
        data: data,
        pe: len(data),
    }
    %% write init;
    return lex
}


func (lex *lexer) Lex(out *yySymType) int {
    eof := lex.pe
    tok := 0
    %%{ 
        main := |*
            'func' => { tok = FUNC; fbreak;};
            'main' => { tok = MAIN_TOKEN; fbreak;};
            '(' => { tok = L_PAREN; fbreak;};
            ')' => { tok = R_PAREN; fbreak;};
            '{' => { tok = L_CB; fbreak;};
            '}' => { tok = R_CB; fbreak;};
            '[' => { tok = L_B; fbreak;};
            ']' => { tok = R_B; fbreak;};
            [a-zA-Z_]+[a-zA-Z_0-9]* => {tok = ID; fbreak;};
            'true' |'1' => { tok = TRUE; fbreak;};
            'false' |'0' => { tok = FALSE; fbreak;};
            'echo' => { tok = ECHO; fbreak; };
            '++' =>{tok=INC;fbreak;};
            '--' =>{tok=DEC;fbreak;};
            '&&' =>{tok=AND;fbreak;};
            '||' =>{tok=OR;fbreak;};
            [1-9][0-9]* | 0 => {tok=NUM;fbreak;};
            "\""[^"\n"]"\"" => {tok=VAL1;fbreak;};
            'floop' => { tok = FLOOP; fbreak;};
            'wloop' => { tok = WLOOP; fbreak;};
            'cook' => { tok = COOK; fbreak;};
            '>=' => { tok = GE; fbreak;};
            '<=' => { tok = LE; fbreak;};
            '>' => { tok = GT; fbreak;};
            '==' => {tok = EQ;fbreak;};    
            '<' => { tok = LT; fbreak;};
            '!=' => { tok = NEQ; fbreak;};
            'if' => { tok = IF; fbreak;};
            'else' => { tok = ELSE; fbreak;};
            'else_if' => { tok = ELSE_IF; fbreak;};

            [0-9] => {tok = _digit;fbreak;};
            'char' => {tok=CHAR;fbreak;};
            'continue' =>{tok=CONTINUE;fbreak;};
            'break' =>{tok=BREAK;fbreak;};
            'return' =>{tok=RETURN;fbreak;};
            'headof' => {tok=HEADOF;fbreak;};
            'tailof' => {tok=TAILOF;fbreak;};
            'len' => {tok=LEN;fbreak;};
            [a-zA-Z] => {tok=VAL9;fbreak;};
            [1-9] => {tok=NUM1;fbreak;};
            ':' => {tok=COLON;fbreak;};
            '+' => {tok=PLUS;fbreak;};
            '-' => {tok=MINUS;fbreak;};
            '*' => {tok=MULT;fbreak;};
            '/' => {tok = DIV;fbreak;};
            '0' => {tok = ZERO;fbreak;};
            '(' => {tok = L_PAREN;fbreak;};
            ')' => {tok=R_PAREN;fbreak;};
            '{'=> {tok=L_CB;fbreak;};
            '}'=> {tok=R_CB;fbreak;};
            '['=>{tok=L_B;fbreak;};
            ']'=>{tok=R_B;fbreak;};
            ','=>{tok=COMMA;fbreak;};
            '=' => {tok=ASSIGN_EQ;fbreak;};
            ';'=>{tok=SEMI_COL;fbreak;};

            space;
        *|;

         write exec;
    }%%

    return tok;
}

func (lex *lexer) Error(e string) {
    fmt.Println("error:", e)
}