from random import randint
from parser_classes import *

tokens = (
    'ADD',  # +
    'SUB',  # -
    'MUL',  # *
    'DIV',  # /
    'VAL',  # 0123
    'COMMENT',  # any letters
    'LBRACKET',  # (
    'RBRACKET',  # )
    'SLBRACKET',  # [
    'SRBRACKET',  # ]
    'COMMA',  # ,
    'FOR',  # x
    'DIE',  # d
    'MAX',  # max
    'MIN',  # min
    'SUM',  # sum
    'BIGGER',  # >
    'LESSER',  # <
    'EQUAL',  # =
    'BIGGEREQUAL',  # >= or =>
    'LESSEREQUAL',  # <= or =<
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
    ('right', 'DIE'),
)

classes = {'>': Greater, '>=': GreaterEquals, '=>': GreaterEquals,
           '<': Lesser, '<=': LesserEquals, '=<': LesserEquals, '=': Equals,
           '+': Addition, '-': Subtraction, '*': Multiplication, '/': Division,
           'min': MinFunction, 'max': MaxFunction, 'sum': SumFunction}


def p_group(p):
    """expression : LBRACKET expression RBRACKET"""
    #    p[0] = (p[2][0], f'({p[2][1]})')
    p[0] = p[2]


def p_block(p):
    """expression : SLBRACKET expression SRBRACKET"""
    p[0] = Tuple(p[2])


def p_if(p):
    """expression : expression IF expression ELSE expression"""
    p[0] = IfOperation(p[1], p[3], p[5])


def p_compare(p):
    """expression : expression BIGGER expression
    | expression LESSER expression
    | expression EQUAL expression
    | expression LESSEREQUAL expression
    | expression BIGGEREQUAL expression"""
    p[0] = classes[p[2]](p[1], p[3])


def p_functions(p):
    """expression : MIN LBRACKET expression RBRACKET
    | MAX LBRACKET expression RBRACKET
    | SUM LBRACKET expression RBRACKET"""
    p[0] = classes[p[1]](p[3])


def p_for(p):
    """expression : expression FOR LBRACKET expression RBRACKET"""
    p[0] = CommaOperation(*[p[4]] * p[1].ops[0])


def p_comma(p):
    """expression : expression COMMA expression"""
    p[0] = CommaOperation(p[1], p[3])


def p_math(p):
    """expression : expression ADD expression
    | expression SUB expression
    | expression MUL expression
    | expression DIV expression"""
    p[0] = classes[p[2]](p[1], p[3])


def p_val(p):
    """expression : VAL"""
    p[0] = Val(int(p[1]))


def p_val_comment(p):
    """expression : VAL COMMENT"""
    p[0] = Val(int(p[1]), p[2])


def p_die(p):
    """expression : DIE expression"""
    p[0] = DiceOperation(Val(1), p[2])


def p_dice(p):
    """expression : expression DIE expression"""
    p[0] = DiceOperation(p[1], p[3])


def p_var(p):
    """expression : VAR"""
    p[0] = Var()


def p_map(p):
    """expression : MAP LBRACKET expression ELSE expression RBRACKET"""
    p[0] = Map(p[3], p[5])


def p_error(p):
    print("Syntax error at '%s'" % p.value)
