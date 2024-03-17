import sys
from typing import List, Optional
from dataclasses import dataclass
import lark.tree
from lark import Lark, ast_utils, Transformer, v_args
from lark.tree import Meta


def flatten(lst):
    flat_list = []
    for sublist in lst:
        if isinstance(sublist, list):
            flat_list.extend(flatten(sublist))
        else:
            flat_list.append(sublist)
    return flat_list
    return lst
this_module = sys.modules[__name__]

#
#   Define AST
#

grammar = '''
start: program
program: function_decl 
function_decl: main_function -> func_to_main
            | (FUNC datatype IDENTIFIER LPAREN params RPAREN LBR stmts RBR function_decl)
main_function: FUNC NUM MAIN LPAREN RPAREN LBR stmts RBR 

LPAREN: "("
RPAREN: ")"
LBR: "{"
RBR: "}"

params: (param ("," param)*)? 
param: datatype IDENTIFIER  | datatype "(" ")" IDENTIFIER  | datatype "[" "]" IDENTIFIER  | datatype "{" "}" IDENTIFIER 
datatype: NUM | FLAG | STR | VOID | CHAR
stmts: (stmt ";" | function_decl | floop  |  wloop  |  if_cond  |  try  |  catch | iter COLON )*
stmt: CONTINUE | BREAK | RETURN | RETURN IDENTIFIER | RETURN CONST |(IDENTIFIER "[" IDENTIFIER "]" ASSIGN exp ) | l1 | RETURN IDENTIFIER "[" (VAL2)? ":" (VAL2)? "]"

try : TRY  "{"  stmts  "}" 
catch :  CATCH  "{"  stmts  "}" 
throw : THROW  "("  VAL1  ")" 
floop : FLOOP  LPAREN  assign  COLON  cond  COLON  iter  RPAREN  LBR  stmts  RBR
wloop : WHOOP  LPAREN  cond  RPAREN  LBR  stmts  RBR 
assign : COOK datatype IDENTIFIER ASSIGN exp -> a1
        | IDENTIFIER ASSIGN exp -> a2
        | IDENTIFIER INC -> a3
        | IDENTIFIER DEC
cond : UNARY_NOT c | c


COLON: ";"

c : "(" c ")" | (exp | LEN "(" IDENTIFIER ")" | HEADOF "(" IDENTIFIER ")" | TAILOF "(" IDENTIFIER ")" | VAL2 | VAL1) comp (exp | LEN "(" IDENTIFIER ")" | HEADOF "(" IDENTIFIER ")" | TAILOF "(" IDENTIFIER ")" | VAL2 | VAL1) | TRUE | FALSE | c "||" c | c "&&" c | exp 
comp : GTE | LTE | NEQL | LT | GT | EQL  
exp : (IDENTIFIER | IDENTIFIER "[" (VAL2 | IDENTIFIER) "]" | "(" exp ")" | (exp | int_exp) op (exp| int_exp))? | exp1
exp1: "(" exp1 ")" | CONST 
e1: ((datatype IDENTIFIER  | datatype "(" ")" IDENTIFIER  | datatype "[" "]" IDENTIFIER  | datatype "{" "}" IDENTIFIER ) e2*)*
e2: ("," e1)
op: PLUS | MINUS | MUL | DIV | POW | BWAND | BWOR | XOR | MODULO

binary_exp: binary_exp binary_op binary_exp
          | "(" binary_exp ")" | UNARY_NOT binary_exp
          | TRUE
          |FALSE
          | exp

binary_op: OR | AND | EQL | NEQL 

IF : "if"
ELSE_IF : "else_if"
ELSE : "else"
if_cond : IF "(" cond ")" "{" stmts "}" (else_if_cond | else_cond)?
else_if_cond : ELSE_IF "(" cond ")" "{" stmts "}" (else_if_cond | else_cond)?
else_cond : ELSE "{" stmts "}"
int_exp : VAL2 | LEN "(" IDENTIFIER ")" | HEADOF "(" IDENTIFIER ")" | TAILOF "(" IDENTIFIER ")" | "(" int_exp ")"
iter: stmt | IDENTIFIER INC | IDENTIFIER DEC
print : ((IDENTIFIER | CONST) ("," print)?  |  ("," print)? | (IDENTIFIER | CONST) "[" (exp | VAL2) "]" ("," print)? )? 

l1:  COOK datatype IDENTIFIER ASSIGN VAL2 ":" ":" IDENTIFIER
    | IDENTIFIER ASSIGN VAL2 ":" ":" IDENTIFIER
    | l

l:COOK datatype IDENTIFIER ASSIGN "{" val11 "}" 
    | COOK IDENTIFIER ASSIGN "[" val7 "]"
    | COOK IDENTIFIER ASSIGN "(" val7 ")"
    | COOK datatype IDENTIFIER
    | COOK datatype IDENTIFIER "[" IDENTIFIER "]"
    | COOK datatype IDENTIFIER "[" int_exp "]"
    | IDENTIFIER ASSIGN "[" val7 "]"
    | IDENTIFIER ASSIGN ( binary_exp)
    | IDENTIFIER ASSIGN IDENTIFIER "[" int_exp "]"
    | IDENTIFIER ASSIGN IDENTIFIER "(" val7 ")"
    | COOK datatype IDENTIFIER ASSIGN ( binary_exp | VAL1 | VAL9 )
    | COOK datatype IDENTIFIER ASSIGN "[" val7 "]"
    | COOK datatype IDENTIFIER ASSIGN IDENTIFIER "[" int_exp "]"
    | COOK datatype IDENTIFIER ASSIGN IDENTIFIER "(" val7 ")"
    | COOK datatype IDENTIFIER ASSIGN IDENTIFIER "("  ")"
    | COOK datatype IDENTIFIER ASSIGN IDENTIFIER "[" exp? ":" exp? "]"
    | COOK datatype IDENTIFIER ASSIGN VAL1 "[" exp? ":" exp? "]"
    | ECHO "(" print ")"
    | throw 

slicing: IDENTIFIER "[" exp? ":" exp? "]"
       | VAL1 "[" exp? ":" exp? "]"

CONST : VAL2 | VAL1 | VAL9

VAL1: /"[^"]*"/
NUM1 : /[1-9]/
NUM2 : /[0-9]*/
VAL2T: /[1-9][0-9]*/ 
VAL2 : ("-")?VAL2T |"0"

VAL3 : TRUE | FALSE

val4 : ((VAL2 ) ( "," (VAL2) )*)?
val11: ((VAL1 | VAL3 | VAL2 | VAL9) ( "," (VAL1 | VAL3 | VAL2 | VAL9) )*)?
val5 : (VAL1 ( "," VAL1 )*)?

val6 : (VAL3 ( "," VAL3 )*)?

val7 : ((VAL1 | VAL2 | VAL3 |  IDENTIFIER | VAL9 |  IDENTIFIER "[" exp "]" | LEN "(" IDENTIFIER ")" | HEADOF "(" IDENTIFIER ")" | TAILOF "(" IDENTIFIER ")" | slicing ) ( "," (VAL1 | VAL2 | VAL3 | IDENTIFIER | VAL9 |  IDENTIFIER "[" exp "]" | LEN "(" IDENTIFIER ")" | HEADOF "(" IDENTIFIER ")" | TAILOF "(" IDENTIFIER ")" | slicing) )*)?
VAL9 : /'([A-Za-z])'/
val10 : (VAL9 ( "," VAL9 )*)?
NUM : "num"
FLAG : "flag"
STR : "str"
VOID : "void" 
CHAR : "char"
FUNC :"func"
TRY : "try"
CATCH : "catch"
THROW : "throw"
COOK : "cook"
MAIN : "main"
RETURN : "return"
CONTINUE : "continue"
BREAK : "break"
FLOOP : "floop"
WHOOP : "whoop"
INC : "++"
DEC : "--"
UNARY_NOT : "!"
LEN : "len"
HEADOF : "headof"
TAILOF : "tailof"
TRUE : "true"
FALSE : "false"
ECHO : "echo"
PLUS : "+"
MINUS : "-"
MUL : "*"
DIV : "/"
POW : "^"
BWAND : "&"
BWOR : "|"
XOR : "^"
OR : "||"
AND : "&&"
EQL : "=="
NEQL : "!="
GTE : ">="
LTE : "<="
LT : "<"
GT : ">"
MODULO : "%"
ASSIGN : "="

IDENTIFIER: /[a-zA-Z_][a-zA-Z0-9_]*/
%import common.WS
%ignore WS
%import common.WS_INLINE
%ignore WS_INLINE
'''

class ASTNodeMeta(type):
    def __new__(cls, name, bases, dct):
        if name != 'BaseASTNode':
            def repr_func(self):
                return name
            dct['__repr__'] = repr_func
        return super().__new__(cls, name, bases, dct)

class ASTNode(metaclass=ASTNodeMeta):
    """Abstract b"""
    pass

class BaseASTNode(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            # print(self)
            # print(f'{i} {value}')
            setattr(self, f'{i}', value)


# class Program(BaseASTNode):
#     functions : List[FunctionDecl]




class Statement(BaseASTNode):
    pass

class Program(BaseASTNode):
    def __init__(self, functions : List['Function_Decl']):
        self.functions = functions

class Function_Decl(BaseASTNode):
    def __init__(self,datatype : str, identifier : str, params : List['Params'], stmts : List['Statement']):
        self.datatype = datatype
        self.identifier = identifier
        self.params = params
        self.stmts = stmts

class Params(BaseASTNode):
    def __init__(self,datatype : str, identifier : str):
        self.datatype = datatype
        self.identifier = identifier

class Main_Function(BaseASTNode):
    def __init__(self, stmts):
        self.stmts = stmts

class Floop(BaseASTNode):
    def __init__(self, assign, cond, iter, stmts):
        self.assign = assign
        self.cond = cond
        self.iter = iter
        self.stmts = stmts

class Wloop(BaseASTNode):
    def __init__(self, cond, stmts):
        self.cond = cond
        self.stmts = stmts

class Try(BaseASTNode):
    def __init__(self, stmts):
        self.stmts = stmts
        
class Catch(BaseASTNode):
    def __init__(self, stmts):
        self.stmts = stmts

class Throw(BaseASTNode):
    def __init__(self, val1):
        self.val1 = val1

class SetValue(BaseASTNode):
    def __init__(self, name,value):
        self.name = name
        self.value = value

class Assign(BaseASTNode):
    def __init__(self, name,value):
        self.identifier = name
        self.value = value

class assign(BaseASTNode):
    pass

class If_cond(BaseASTNode):
    def __init__(self,cond,then):
        self.cond = cond
        self.then = then

class Else_If_cond(BaseASTNode):
    def __init__(self,cond,then):
        self.cond = cond
        self.then = then

class Else_Cond(BaseASTNode):
    def __init__(self,then):
        self.then = then

class iter(BaseASTNode):
    pass

# class IDENTIFIER(BaseASTNode):
#     pass

class start(BaseASTNode):
    pass

class LPAREN(BaseASTNode):
    pass


class RPAREN(BaseASTNode):
    pass
class program(BaseASTNode):
    pass
class LBR(BaseASTNode):
    pass
class RBR(BaseASTNode):
    pass
class COLON(BaseASTNode):
    pass
class binary_exp(BaseASTNode):
    pass


class binary_op(BaseASTNode):
    pass
class slicing(BaseASTNode):
    pass


class ToAst(Transformer):
    # Define transformation functions for each rule that corresponds to an AST class.
    def start(self, items):
        # print("s")
        # print(items)
        flatten_list=(flatten(items))
        
        return start(items)
    
    def main_function(self, items):
        # print("main_function")
        # print(items)
        flatten_list=(flatten(items))
        # print(flatten_list)
        return Main_Function(items)
    
    def function_decl(self, items):
        # print("fd")
        # print(items)
        flatten_list=(flatten(items))
        if(len(flatten_list)==1):
            return Main_Function(flatten_list)
        else:
            return Function_Decl(flatten_list[1],flatten_list[2],flatten_list[4],flatten_list[8])
            
    def param(self, items):
        flatten_list=(flatten(items))
        return Params(flatten_list[0],flatten_list[1])
    
    def datatype(self, items):
        return items[0]
        
    def stmt(self, items):
        return Statement(items)
    
    def Try(self, items):
        flatten_list=(flatten(items))
        return Try(flatten_list[2])
    
    def catch(self, items):
        flatten_list=(flatten(items))
        return Catch(flatten_list[2])
    
    def throw(self, items):
        flatten_list=(flatten(items))
        return Throw(flatten_list[2])
    
    def floop(self, items):
        flatten_list=(flatten(items))
        return Floop(flatten_list[2],flatten_list[4],flatten_list[6],flatten_list[9])
    
    def wloop(self, items):
        flatten_list=(flatten(items))
        return Wloop(flatten_list[2],flatten_list[5])
    
    def assign(self, items):
        flatten_list=(flatten(items))
        return assign(flatten_list)
    
    def if_cond(self, items):
        flatten_list=(flatten(items))
        return If_cond(flatten_list[1],flatten_list[2])
    
    def else_if_cond(self, items):
        flatten_list=(flatten(items))
        return Else_If_cond(flatten_list[1],flatten_list[2])
    
    def else_cond(self, items):
        flatten_list=(flatten(items))
        print(flatten_list)
        return Else_Cond(flatten_list[1])
     
    def iter(self, items):
        flatten_list=(flatten(items))
        return iter(flatten_list)
    
    # def l1(self, items):
    #     # print("l1")
    #     # print(items)
    #     flatten_list=(flatten(items))
    #     return l1(flatten_list)
    
    def l(self, items):
        flatten_list=(flatten(items))
        # print(flatten_list)
        return SetValue(flatten_list[2],flatten_list[4])
    
    # def CONST(self, items):
    #     # print("cnst")
    #     # print(items)
    #     flatten_list=(flatten(items))
    #     return CONST(flatten_list)
    
    # def VAL1(self, items):
    #     flatten_list=(flatten(items))
    #     return VAL1(flatten_list)
    
    # def VALX(self, items):
    #     flatten_list=(flatten(items))
    #     return VALX(flatten_list)
    
    # def NUM1(self, items):
    #     flatten_list=(flatten(items))
    #     return NUM1(flatten_list)
    
    # def NUM2(self, items):
    #     flatten_list=(flatten(items))
    #     return NUM2(flatten_list)
    
    # def VAL2(self, items):
    #     # print("v2")
    #     # print(items)
    #     flatten_list=(flatten(items))
    #     return VAL2(flatten_list)
    
    # def VAL3(self, items):
    #     flatten_list=(flatten(items))
    #     return VAL3(flatten_list)
    
    # def val4(self, items):
    #     flatten_list=(flatten(items))
    #     return val4(flatten_list)
    
    # def val11(self, items):
    #     flatten_list=(flatten(items))
    #     return val11(flatten_list)
    
    # def val5(self, items):
    #     flatten_list=(flatten(items))
    #     return val5(flatten_list)
    
    # def val6(self, items):
    #     flatten_list=(flatten(items))
    #     return val6(flatten_list)
    
    # def val7(self, items):
    #     flatten_list=(flatten(items))
    #     return val7(flatten_list)
    
    # def VAL9(self, items):
    #     flatten_list=(flatten(items))
    #     return VAL9(flatten_list)
    
    # def val10(self, items):
    #     flatten_list=(flatten(items))
    #     return val10(flatten_list)
    
    # def IDENTIFIER(self, items):
    #     # print("id")
    #     # print(items)
    #     flatten_list=(flatten(items))
    #     return IDENTIFIER(flatten_list)
    
    def program(self, items):
        # print("pgrm")
        # print(items)
        flatten_list=(flatten(items))
        # print(flatten_list)
        return Program(list(flatten_list))
    
    # def LPAREN(self, items):
    #     # print("lppppp")
    #     # print(items)
    #     flatten_list=(flatten(items))
    #     return LPAREN(flatten_list)
    # def RPAREN(self, items):
    #     # print("rpppppp")
    #     # print(items)
    #     flatten_list=(flatten(items))
    #     return RPAREN(flatten_list)
    # def LBR(self, items):
    #     # print("lbrrr")
    #     # print(items)
    #     flatten_list=(flatten(items))
    #     return LBR(flatten_list)
    # def RBR(self, items):
    #     # print("rbbbr")
    #     # print(items)
    #     flatten_list=(flatten(items))
    #     return RBR(flatten_list)
    # def COLON(self, items):
    #     flatten_list=(flatten(items))
    #     return COLON(flatten_list)
    def binary_exp(self, items):
        # print("beeee")
        # print(items)
        flatten_list=(flatten(items))
        return binary_exp(flatten_list)
    def binary_op(self, items):
        # print("booooo")
        # print(items)
        flatten_list=(flatten(items))
        return binary_op(flatten_list)
    def slicing(self, items):
        flatten_list=(flatten(items))
        return slicing(flatten_list)
    # def VAL2T(self, items):
    #     flatten_list=(flatten(items))
    #     return VAL2T(flatten_list)
        
    
transformer = ast_utils.create_transformer(this_module, ToAst())

def parse(text):
    parser = Lark(grammar, parser="lalr")
    tree = parser.parse(text)
    # print(tree.pretty())
    p = transformer.transform(tree)
    #print(f"as {repr(p)}")
    return p

def print_ast(node, indent=0):
    print(' ' * indent + repr(node))
    # print(node, type(node))
    if(type(node)!=lark.tree.Tree):
        print(node)
    if isinstance(node, BaseASTNode):
        for child_name, child_node in node.__dict__.items():

            if isinstance(child_node, list):
                for child in child_node:
                    print_ast(child, indent + 4)
            else:
                print_ast(child_node, indent + 4)
    
    elif(isinstance(node, lark.tree.Tree)):
        for child in node.children:
            print_ast(child, indent + 4)
    

def draw_ast(node, indent=0):
    print(' ' * indent + repr(node))
    for child in node.__dict__.values():
        print(type(child))
        if isinstance(child, list):
            for item in child:
                if isinstance(item, ASTNode):
                    draw_ast(item, indent=indent + 2)
        if isinstance(child, ASTNode):
            draw_ast(child, indent=indent + 2)
# Assuming `ast_root` is the root node of your AST


if __name__ == '__main__':
    test_program = """
        func num main(){

            if(a>5){
                cook num b = 5;
            }
            else{
                cook num b=6;
            }
        }
    """
    # print((parse(test_program)))
    # traverse_ast(parse(test_program))
    ast_root = parse(test_program)
    # print(ast_root)
    print_ast(ast_root)
