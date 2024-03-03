package main

import "fmt"

//go:generate ragel -Z -G2 -o lex.go lex.rl
//go:generate  goyacc grammar.y

func main() {
	lex := newLexer([]byte(`
		func abc(){
		}
		func main(){
			a = 10;
		}
	
	`))
	e := yyParse(lex)
	fmt.Println(e)
}
