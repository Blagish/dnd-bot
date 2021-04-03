from random import randint
from parser_classes import *

tokens = (
    'ADD',  # +
    'SUB',  # -
    'MUL',  # *
    'DIV',  # /
    'VAL',  # 0123
    'LBRACKET',  # (
    'RBRACKET',  # )
    'SLBRACKET',  # [
    'SRBRACKET',  # ]
    'COMMA',  # ,
    'FOR',   # x
    'DIE',  # d
    'MAX',  # max
    'MIN',  # min
    'SUM',  # sum
    'BIGGER',  # >
    'LESSER',  # <
    'EQUAL',   # =
    'BIGGEREQUAL',  # >=
    'LESSEREQUAL',  # <=
    'IF',  # ?
    'ELSE',  # :
    'VAR',  # it
    'MAP',  # map
    'ARG',  # gwf, ea, rt, st, etc.
)

precedence = (
    ('left', 'FOR'),
    ('left', 'ADD', 'SUB', 'BIGGER', 'LESSER', 'EQUAL', 'BIGGEREQUAL', 'LESSEREQUAL'),
    ('left', 'MUL', 'DIV'),
    ('right', 'DIE')
)

names = {}


def p_top_group(p):
    """expression : LBRACKET expression RBRACKET"""
#    p[0] = (p[2][0], f'({p[2][1]})')
    p[0] = p[2]


def p_top_if(p):
    """expression : expression IF expression ELSE expression"""
    p[0] = IfOperation(p[1], p[3], p[5])


#def p_top_compare(p):
#    """expression : expression BIGGER expression
#    | expression LESSER expression
#    | expression EQUAL expression
#    | expression LESSEREQUAL expression
#    | expression BIGGEREQUAL expression"""
#    p[0] = CompareOperation(p[1], p[3], value=p[2])


def p_top_greater(p):
    """expression : expression BIGGER expression"""
    p[0] = Greater(p[1], p[3])


def p_top_lesser(p):
    """expression : expression LESSER expression"""
    p[0] = Lesser(p[1], p[3])


def p_top_greaterequals(p):
    """expression : expression BIGGEREQUAL expression"""
    p[0] = GreaterEquals(p[1], p[3])


def p_top_lesserequals(p):
    """expression : expression LESSEREQUAL expression"""
    p[0] = LesserEquals(p[1], p[3])


def p_top_equals(p):
    """expression : expression EQUAL expression"""
    p[0] = Equals(p[1], p[3])


def p_top_min(p):
    """expression : MIN LBRACKET expression RBRACKET"""
    p[0] = MinOperation(p[3])


def p_top_max(p):
    """expression : MAX LBRACKET expression RBRACKET"""
    p[0] = MaxOperation(p[3])


def p_top_for(p):
    """expression : expression FOR LBRACKET expression RBRACKET"""
    p[0] = CommaOperation(*[p[4]]*p[1].ops[0])


def p_top_comma(p):
    """expression : expression COMMA expression"""
    left, right = p[1], p[3]
    p[0] = CommaOperation(left, right)


#def p_top_full(p):
#    """expression : expression ADD expression
#    | expression SUB expression
#    | expression MUL expression
#    | expression DIV expression"""
#    left, right = p[1], p[3]
#    p[0] = BasicMathOperation(left, right, value=p[2])


def p_top_add(p):
    """expression : expression ADD expression"""
    left, right = p[1], p[3]
    p[0] = Addition(left, right)


def p_top_sub(p):
    """expression : expression SUB expression"""
    left, right = p[1], p[3]
    p[0] = Subtraction(left, right)


def p_top_mul(p):
    """expression : expression MUL expression"""
    left, right = p[1], p[3]
    p[0] = Multiplication(left, right)


def p_top_div(p):
    """expression : expression DIV expression"""
    left, right = p[1], p[3]
    p[0] = Division(left, right)


def p_top_val(p):
    """expression : VAL"""
    p[0] = Val(int(p[1]))


def p_top_die(p):
    """expression : DIE expression"""
    right = p[2]
    p[0] = DiceOperation(Val(1), right)


def p_top_dice(p):
    """expression : expression DIE expression"""
    left, right = p[1], p[3]
    p[0] = DiceOperation(left, right)


def p_top_var(p):
    """expression : VAR"""
    p[0] = Var()


def p_top_map(p):
    """expression : MAP LBRACKET expression ELSE expression RBRACKET"""
    p[0] = Map(p[3], p[5])


def p_top_sum(p):
    """expression : SUM LBRACKET expression RBRACKET"""
    p[0] = Sum(p[3])


def p_block(p):
    """expression : SLBRACKET expression SRBRACKET"""
    p[0] = Tuple(p[2])


def p_error(p):
    print("Syntax error at '%s'" % p.value)
