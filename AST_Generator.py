import sys
from typing import List, Optional
from dataclasses import dataclass
import lark
from lark.lexer import Token, Lexer
import lark.tree as tree
from lark import Lark, LarkError, ast_utils, Transformer, v_args
from lark.tree import Meta
import networkx as nx
import matplotlib.pyplot as plt
from graphviz import Digraph

this_module = sys.modules[__name__]

#
#   Define AST
#

grammar = '''
start: program
program: function_decl_list 
function_decl_list:  main_function |  ( function_decl )* 
main_function: "func" "num" "main" "(" ")" "{" stmts "}"
function_decl:  "func" dt_identifier "(" params ")" "{" stmts "}" 



params: (param ("," param)*)? 
param: dt_identifier  | datatype "(" ")" IDENTIFIER  | datatype "[" "]" IDENTIFIER  | datatype "{" "}" IDENTIFIER 
datatype: NUM | STR | VOID | CHAR | FLAG
stmts: (stmt ";" | function_decl | floop  |  wloop  |  if_else_block  |  trycatchblock | iter ";" )*
trycatchblock: try_ catch?
stmt: CONTINUE | BREAK | RETURN | RETURN IDENTIFIER | RETURN CONST |(IDENTIFIER "[" IDENTIFIER "]" "=" exp ) | l1 | RETURN IDENTIFIER "[" (VAL2)? ":" (VAL2)? "]"
if_else_block: if_cond else_if_cond* else_cond?
try_ : "try"  "{"  stmts  "}" 
catch :  "catch"  "{"  stmts  "}" 
throw : "throw"  "("  VAL1  ")" 
floop : "floop"  "("  assign  ";"  cond  ";"  iter  ")"  "{"  stmts  "}"
wloop : "wloop"  "("  cond  ")"  "{"  stmts  "}" 
assign : "cook" dt_identifier "=" exp 
        | IDENTIFIER "=" exp -> a2
        | IDENTIFIER INC -> a3
        | IDENTIFIER DEC
cond : UNARY_NOT c | c


c : "(" c ")" | (exp | LEN "(" IDENTIFIER ")" | HEADOF "(" IDENTIFIER ")" | TAILOF "(" IDENTIFIER ")" | VAL2 | VAL1) comp (exp | LEN "(" IDENTIFIER ")" | HEADOF "(" IDENTIFIER ")" | TAILOF "(" IDENTIFIER ")" | VAL2 | VAL1) | TRUE | FALSE | c "||" c | c "&&" c | exp 
comp : GTE | LTE | NEQL | LT | GT | EQL  
exp : ( IDENTIFIER | IDENTIFIER "[" (VAL2 | IDENTIFIER) "]" | "(" exp ")" | (exp | int_exp) op (exp| int_exp))? | exp1
exp1: "(" exp1 ")" | CONST 
e1: ((dt_identifier  | datatype "(" ")" IDENTIFIER  | datatype "[" "]" IDENTIFIER  | datatype "{" "}" IDENTIFIER ) e2*)*
e2: ("," e1)
op: PLUS | MINUS | MUL | DIV | POW | BWAND | BWOR | XOR | MODULO

binary_exp: binary_exp (OR | AND | EQL | NEQL) binary_exp
          | "(" binary_exp ")" | UNARY_NOT binary_exp
          | TRUE
          |FALSE
          | exp


if_cond : "if" "(" cond ")" "{" stmts "}" 
else_if_cond : "else_if" "(" cond ")" "{" stmts "}" 
else_cond : "else" "{" stmts "}"
int_exp : VAL2 | LEN "(" IDENTIFIER ")" | HEADOF "(" IDENTIFIER ")" | TAILOF "(" IDENTIFIER ")" | "(" int_exp ")"
iter: stmt | IDENTIFIER INC | IDENTIFIER DEC
print : ((IDENTIFIER | CONST) ("," print)?  |  ("," print)? | (IDENTIFIER | CONST) "[" (exp | VAL2) "]" ("," print)? )? 

to_print: "echo" "(" print ")"

l1:  "cook" dt_identifier "=" VAL2 ":" ":" IDENTIFIER
    | IDENTIFIER "=" VAL2 ":" ":" IDENTIFIER
    | l

l:"cook" dt_identifier "=" "{" val11 "}" 
    | "cook" LIST_TUPLE_ID "=" "[" val7 "]"
    | "cook" LIST_TUPLE_ID "=" "(" val7 ")"
    | "cook" dt_identifier
    | "cook" dt_identifier "[" IDENTIFIER "]"
    | "cook" dt_identifier "[" int_exp "]"
    | IDENTIFIER "=" "[" val7 "]"
    | IDENTIFIER "=" ( binary_exp)
    | IDENTIFIER "=" IDENTIFIER "[" int_exp "]"
    | IDENTIFIER "=" IDENTIFIER "(" val7 ")"
    | "cook" dt_identifier "=" ( binary_exp | VAL1 | VAL9 )
    | "cook" dt_identifier "=" "[" val7 "]"
    | "cook" dt_identifier "=" IDENTIFIER "[" int_exp "]"
    | "cook" dt_identifier "=" FUNC_IDENTIFIER "(" val7 ")"
    | "cook" dt_identifier "=" IDENTIFIER "("  ")"
    | "cook" dt_identifier "=" IDENTIFIER "[" exp? ":" exp? "]"
    | "cook" dt_identifier "=" VAL1 "[" exp? ":" exp? "]"
    | to_print
    | throw 

LIST_TUPLE_ID: /(?<!(main)\b)[a-zA-Z_][a-zA-Z0-9_]*/
FUNC_IDENTIFIER: /(?<!(main)\b)[a-zA-Z_][a-zA-Z0-9_]*/
FUNC_DECL_IDENTIFIER : /(?<!(main)\b)[a-zA-Z_][a-zA-Z0-9_]*/

dt_identifier : datatype IDENTIFIER

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
TRY : "try"
CATCH : "catch"
THROW : "throw"
MAIN : "main"
RETURN : "return"
CONTINUE : "continue"
BREAK : "break"
INC : "++"
DEC : "--"
UNARY_NOT : "!"
LEN : "len"
HEADOF : "headof"
TAILOF : "tailof"
TRUE : "true"
FALSE : "false"
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



IDENTIFIER: /(?<!(main)\b)[a-zA-Z_][a-zA-Z0-9_]*/
%import common.WS
%ignore WS
%import common.WS_INLINE
%ignore WS_INLINE
'''



class ASTNodeMeta(type):
    def __new__(cls, name, bases, dct):
        if name != 'ASTNode':
            def repr_func(self):
                return name
            dct['__repr__'] = repr_func
        return super().__new__(cls, name, bases, dct)
    

class ASTNode(metaclass=ASTNodeMeta):
    """Abstract b"""
    pass

class Start(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class Program(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)
            
class FunctionDeclList(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)
            

class Statement(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)
            
class FunctionDeclaration(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)
            
class Param(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)
            
class Params(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)
            
class MainFunction(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)
            
class DataType(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)
            
class Assign(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class   IfElseBlock(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class IfCond(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)
            
class ElseIfCond(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)
            
class ElseCond(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)
            
class Expression(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)
            

class Try(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)
            
class Catch(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)
            
class Throw(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class Floop(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)
            
class Wloop(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class Print(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class TryCatchBlock(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)

class LoopAssign(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)
            
class ConditionalStatement(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)
            
class PrintParams(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)
            
class Slice(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)
            
class IntTerminal(ASTNode):
    def __init__(self, value):
        self.value = value
        
class StringTerminal(ASTNode):
    def __init__(self, value):
        str=""
        for i in value:
            str+=i
        self.value = str
class BoolTerminal(ASTNode):
    def __init__(self, value):
        self.value = value
        
class CharTerminal(ASTNode):
    def __init__(self, value):
        self.value = value
        
class ListItems(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            setattr(self, f'{i}', value)
            # print(type(value))
            
class DT_IDENTIFIER(ASTNode):
    def __init__(self, values):
        for i, value in enumerate(values):
            if(type(value)!=str):
                setattr(self, f'{i}', value)
            else:
                setattr(self, f'{i}', IDENTIFIER(value))

class ListTupleIdentifier(ASTNode):
    def __init__(self, value):
        str=""
        for i in value:
            str+=i
        self.value = str
                     
class IDENTIFIER(ASTNode):
    def __init__(self, value):
        str=""
        for i in value:
            str+=i
        self.value = str                        
                        
class FUNC_IDENTIFIER(ASTNode):
    def __init__(self, value):
        str=""
        for i in value:
            str+=i
        self.value = str
            
class FUNC_DECL_IDENTIFIER(ASTNode):
    def __init__(self, value):
        str=""
        for i in value:
            str+=i
        self.value = str

def single_list(_list):
    combined_list = []
    for entry in _list:
        if isinstance(entry, list):
            combined_list.extend(single_list(entry))
        else:
            combined_list.append(entry)
    return combined_list


def to_list(our_tree):

    ls=[]
    if isinstance(our_tree, lark.tree.Tree):
        for child in our_tree.children:
            ls1= to_list(child)
            ls += ls1
            
    elif(isinstance(our_tree, lark.lexer.Token)):
        ls.append(our_tree.value)
    
    elif(isinstance(our_tree, list)):
        for child in our_tree:
            ls1= to_list(child)
            ls+=ls1
    else:
        ls= [our_tree]
    return ls
         


class ToAst(Transformer):
    
    def create_node(self, items, node_class):
        items = single_list(items)
        if len(items) == 1:
            return items
        return node_class(items)
    
    def start(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return Start(items)
    
    def program(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return Program(items)
    
    def function_decl_list(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        
        return FunctionDeclList(items)
    
    def function_decl(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        
        return FunctionDeclaration(items)
    
    def main_function(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return MainFunction(items)
    
    def params(self, items):
        items = single_list(items)
        return Params(items)
    
    def param(self, items):
        items = single_list(items)
        return Param(items)
    
    def datatype(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return DataType(items)
    
    def stmts(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return Statement(items)
    
    def stmt(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return Statement(items)
    
    def assign(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return LoopAssign(items)
    
    def try_(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return Try(items)
    
    def catch(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst 
        return Catch(items)
        
    def throw(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return Throw(items)
    
    def floop(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return Floop(items)
    
    def wloop(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return Wloop(items)
    
    def if_cond(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return IfCond(items)
    
    def else_if_cond(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return ElseIfCond(items)
    
    def else_cond(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return ElseCond(items)
    
    def cond(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return ConditionalStatement(items)
    
    def c(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return ConditionalStatement(items)
    
    def exp(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return Expression(items)
    
    def ex1(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return Expression(items)
    
    def e1(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return Expression(items)
    
    def e2(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return Expression(items)
    
    def exp1(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return Expression(items)
    
    def binary_exp(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return Expression(items)
    
    def int_exp(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return Expression(items)
    
    def iter(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return Statement(items)
    
    def print(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return PrintParams(items)
    
    def to_print(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return Print(items)
    
    def l1(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return Assign(items)
    
    def comp(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return Expression(items)
    
    def l(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        # print(items)
        return Assign(items)
    
    def dt_identifier(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return DT_IDENTIFIER(items)
    
    def slicing(self, items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return Slice(items)
    
    def VAL1(self,items):
        return self.create_node(items, StringTerminal)
    
    def NUM1(self,items):
        return self.create_node(items, IntTerminal)
    
    def NUM2(self,items):
        return self.create_node(items, IntTerminal)
    
    def VAL2T(self,items):
        return self.create_node(items, IntTerminal)
    
    def VAL2(self,items):
        return self.create_node(items, IntTerminal)
    
    def VAL3(self,items):
        return self.create_node(items, BoolTerminal)
    
    def val11(self,items):
        return self.create_node(items, ListItems)
    
    def val4(self,items):
        return self.create_node(items, ListItems)
    
    def val5(self,items):
        return self.create_node(items, ListItems)
    
    def val6(self,items):
        return self.create_node(items, ListItems)
    
    def val7(self,items):
        return self.create_node(items, ListItems)
    
    def val10(self,items):
        return self.create_node(items, ListItems)
    
    def val9(self,items):
        return self.create_node(items, CharTerminal)
    
    def num(self,items):
        return self.create_node(items, DataType)
    
    def flag(self,items):
        return self.create_node(items, DataType)
    
    def str(self,items):
        return self.create_node(items, DataType)
    
    def void(self,items):
        return self.create_node(items, DataType)
    
    def char(self,items):
        return self.create_node(items, DataType)
    
    def binary_op(self,items):
        return self.create_node(items, Expression)
    
    def op(self,items):
        return self.create_node(items, Expression)
    
    def if_else_block(self,items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return IfElseBlock(items)
    
    def IDENTIFIER(self,items):
        return self.create_node(items, IDENTIFIER)
    
    def trycatchblock(self,items):
        lst=[]
        for i in items:
            lst+=to_list(i)
        items=lst
        return TryCatchBlock(items)
    def LIST_TUPLE_ID(self,items):
        return self.create_node(items, ListTupleIdentifier)
    def FUNC_IDENTIFIER(self,items):
        return self.create_node(items, FUNC_IDENTIFIER)
    def FUNC_DECL_IDENTIFIER(self,items):
        return self.create_node(items, FUNC_DECL_IDENTIFIER)
    
transformer = ast_utils.create_transformer(this_module, ToAst())

def parse(text):
    parser = Lark(grammar, parser="lalr")
    tree = parser.parse(text)
    p = transformer.transform(tree)
    return p



def create_ast(tree, edge_list,graph=None,parent=None):
    if isinstance(tree, ASTNode)==False:
        graph.node(str(id(tree)), label=str(tree), shape='box', filled='true')
        if str(id(parent)) in edge_list.keys():
            edge_list[str(id(parent))].append((str(id(tree)),str(tree)))
        else:
            edge_list[str(id(parent))]=[]
            edge_list[str(id(parent))].append((str(id(tree)),str(tree)))
        graph.edge(str(id(parent)), str(id(tree)))
    else:
        children = vars(tree).items()
        child_count = sum(isinstance(child, ASTNode) for _, child in children)
        if graph is None:
            graph = Digraph()
        if parent is None:
            parent = tree
            graph.node(str(id(parent)), label=str(parent), filled='true')
            for _, child in children:
                create_ast(child,edge_list,graph,tree)
        else:
            if (type(tree)==ElseCond or type(tree)==FunctionDeclaration or type(tree)==MainFunction or type(tree)==Try or type(tree)==Catch or type(tree)==Throw or type(tree)==ListTupleIdentifier):
                graph.node(str(id(tree)), label=str(tree), filled='true')
                graph.edge(str(id(parent)), str(id(tree)))
                if str(id(parent)) in edge_list.keys():
                    edge_list[str(id(parent))].append((str(id(tree)),str(tree)))
                else:
                    edge_list[str(id(parent))]=[]
                    edge_list[str(id(parent))].append((str(id(tree)),str(tree)))
                for _, child in children:
                    create_ast(child,edge_list,graph,tree)
            elif child_count==1:
                for _, child in children:
                    if isinstance(child, ASTNode):
                        create_ast(child,edge_list,graph,parent)
            else:
                graph.node(str(id(tree)), label=str(tree), filled='true')
                graph.edge(str(id(parent)), str(id(tree)))
                if str(id(parent)) in edge_list.keys():
                    edge_list[str(id(parent))].append((str(id(tree)),str(tree)))
                else:
                    edge_list[str(id(parent))]=[]
                    edge_list[str(id(parent))].append((str(id(tree)),str(tree)))
                for _, child in children:
                    create_ast(child,edge_list,graph,tree)
                
    return graph
                

class scopecheck:
    def __init__(self,tree):
        self.tree=tree
        self.scopes = []
        self.func_list = []
    
    def enter_scope(self):
        self.scope = {}
        self.scopes.append(self.scope)
    
    def exit_scope(self):
        self.scopes.pop()
        if self.scopes:
            self.scope = self.scopes[-1]
    
    def add_symbol(self, symbol):
        self.scope[symbol] = True
    
    def check_symbol(self, symbol):
        for scope in reversed(self.scopes):
            if symbol in scope:
                return True
        return False
    
    def check_scope(self, symbol):
        return symbol in self.scope
    
    def dfs_traverse(self,edge_list,node, visited=None):
        if visited is None:
            visited = set()
        if node in visited:
            return
        if node not in edge_list.keys():
            return
        children = edge_list[node]
        for child in children:
            # print(child[1])
            if (child[1]=="FunctionDeclaration" or child[1]=="MainFunction" or child[1]=="Floop" or child[1]=="Wloop" or child[1]=="IfCond"or child[1]=="ElseIfCond"or child[1]=="ElseCond"):
                self.enter_scope()
                self.dfs_traverse(edge_list,child[0], visited)
                self.exit_scope()
            elif(child[1]=="DT_IDENTIFIER"):
                identifier=edge_list[child[0]][1]
                identifier_id=identifier[0]
                idd=edge_list[identifier_id][0][1]
                check=self.check_scope(idd)
                if not check:
                    self.add_symbol(idd)
                else:
                    print(f"Error: {idd} already declared in the same scope")
            elif(child[1]=="IDENTIFIER"):

                check=self.check_symbol(edge_list[child[0]][0][1])
                idd = edge_list[child[0]][0][1]
                if not check:
                    print(f"Error: {idd} not declared in the scope")
            elif(child[1]=="ListTupleIdentifier"):
                identifier=edge_list[child[0]][0]
                identifier_id=identifier[1]
                # idd=edge_list[identifier_id][0][0]
                check=self.check_scope(identifier_id)
                # print(identifier_id)
                if not check:
                    self.add_symbol(identifier_id)
                else:
                    print(f"Error: {identifier_id} already declared in the same scope")
            else:
                self.dfs_traverse(edge_list, child[0], visited)

if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        print("Usage: python parser.py <input_file>")
        sys.exit(1)

    file = sys.argv[1]

    try:
        with open(file, 'r', encoding="utf8") as f:
            sentence = f.read()
            test_program = sentence
        parser = Lark(grammar, start='program', parser='lalr')
        tree = parser.parse(sentence)
        edge_list={}
        print("Parsing succesfull. The input is syntactically correct. AST Generation Succesfull. The AST file has been created.\n")
        graph =create_ast(parse(test_program),edge_list)
        graph.render('AST.gv', view=True)
        scopecheck1=scopecheck(edge_list)
        startId=list(edge_list.keys())[0]
        scopecheck1.dfs_traverse(edge_list,startId)
        
        
    except FileNotFoundError:
        print(f"Error: File '{file}' not found.")
        
    except LarkError as e:
        if hasattr(e, 'line') and hasattr(e, 'column'):
            error_line = e.line
            error_column = e.column
            print(f"Syntax error at line {error_line}, column {error_column}: \n\n{e}")
        else:
            print(f"Syntax error: {e}")
            
    except Exception as e:
        print("123")
        print(f"Error: {e}")