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
    'COMMA',  # ,
    'FOR',   # x
    'DIE',  # d
    'MAX',  # max
    'MIN',  # min
    'BIGGER',  # >
    'LESSER',  # <
    'EQUAL',   # =
    'BIGGEREQUAL',  # >=
    'LESSEREQUAL',  # <=
    'ARG',  # gwf, ea, rt, st, etc.
)

precedence = (
    ('left', 'FOR'),
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV'),
    ('right', 'DIE')
)

names = {}


def p_top_group(p):
    """expression : LBRACKET expression RBRACKET"""
#    p[0] = (p[2][0], f'({p[2][1]})')
    p[0] = p[2]


def p_top_compare(p):
    """expression : expression BIGGER expression
    | expression LESSER expression
    | expression EQUAL expression
    | expression LESSEREQUAL expression
    | expression BIGGEREQUAL expression"""
    p[0] = CompareOperation(p[1], p[3], value=p[2])


def p_top_minmax(p):
    """expression : MAX LBRACKET expression RBRACKET
    | MIN LBRACKET expression RBRACKET"""
    p[0] = MinMaxOperation(p[3], value=p[1])


def p_top_for(p):
    """expression : expression FOR LBRACKET expression RBRACKET"""
    p[0] = CommaOperation(*[p[4]]*p[1].ops[0])


def p_top_comma(p):
    """expression : expression COMMA expression"""
    left, right = p[1], p[3]
    p[0] = CommaOperation(left, right)


def p_top_full(p):
    """expression : expression ADD expression
    | expression SUB expression
    | expression MUL expression
    | expression DIV expression"""
    left, right = p[1], p[3]
    p[0] = BasicMathOperation(left, right, value=p[2])


def p_top_var(p):
    """expression : VAL"""
    p[0] = Var(int(p[1]))


def p_top_die(p):
    """expression : DIE expression"""
    right = p[2]
    p[0] = DiceOperation(Var(1), right, value=p[1])


def p_top_dice(p):
    """expression : expression DIE expression"""
    left, right = p[1], p[3]
    p[0] = DiceOperation(left, right, value=p[2])


def p_error(p):
    print("Syntax error at '%s'" % p.value)
