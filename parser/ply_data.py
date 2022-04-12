from random import randint
from .parser_classes import *

function_keywords = {'max': 'MAX', 'min': 'MIN', 'sum': 'SUM', 'map': 'MAP',
                     'x': 'FOR', 'd': 'DIE', 'ad': 'ADVDIE', 'dd': 'DISDIE',
                     'ed': 'ELFDIE', 'kd': 'QUADIE', 'it': 'VAR'}
tokens = (
    'ADD',  # +
    'SUB',  # -
    'MUL',  # *
    'DIV',  # /
    'VAL',  # 0123
    'DOT',  # .
    'MAX',  # max
    'MIN',  # min
    'SUM',  # sum
    'MAP',  # map
    'LBRACKET',  # (
    'RBRACKET',  # )
    'SLBRACKET',  # [
    'SRBRACKET',  # ]
    'COMMA',  # ,
    'SEMICOLON',  # ;
    'FOR',  # x
    'DIE',  # d
    'ADVDIE',  # ad
    'DISDIE',  # dd
    'ELFDIE',  # ed
    'QUADIE',  # kd
    'BIGGER',  # >
    'LESSER',  # <
    'EQUAL',  # =
    'NOTEQUAL1',  # ≠
    'NOTEQUAL2',  # !=
    'BIGGEREQUAL',  # >= or =>
    'LESSEREQUAL',  # <= or =<
    'IF',  # ?
    'ELSE',  # :
    'VAR',  # it
    'ARG',  # gwf, ea, rt, st, etc.
    'COMMENT'  # any letters
)

precedence = (
    ('left', 'COMMENT'),
    ('left', 'FOR'),
    ('left', 'MIN', 'MAX', 'SUM', 'MAP', 'VAR'),
    ('left', 'ADD', 'SUB', 'BIGGER', 'LESSER', 'EQUAL', 'BIGGEREQUAL', 'LESSEREQUAL'),
    ('left', 'MUL', 'DIV'),
    ('right', 'ADVDIE', 'DISDIE', 'ELFDIE', "QUADIE"),
    ('left', 'DIE')
)

classes = {'>': Greater, '>=': GreaterEquals, '=>': GreaterEquals,
           '<': Lesser, '<=': LesserEquals, '=<': LesserEquals, '=': Equals,
           '+': Addition, '-': Subtraction, '*': Multiplication, '/': Division,
           '≠': NotEquals, '!=': NotEquals,
           'min': MinFunction, 'max': MaxFunction, 'sum': SumFunction}

dices = {'d': DiceOperation, 'ad': AdvantageDiceOperation, 'dd': DisadvantageDiceOperation,
         'ed': ElfAdvantageDiceOperation, 'kd': QuadAdvantageDiceOperation}


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
    | expression BIGGEREQUAL expression
    | expression NOTEQUAL1 expression
    | expression NOTEQUAL2 expression"""
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


def p_minus_val(p):
    """expression : SUB VAL"""
    p[0] = Val(-int(p[2]))


def p_val_comment(p):
    """expression : VAL COMMENT"""
    p[0] = Val(int(p[1]), p[2])


def p_float_val(p):
    """expression : VAL DOT VAL"""
    p[0] = Val(float(f'{p[1]}.{p[3]}'))


def p_minus_float_val(p):
    """expression : SUB VAL DOT VAL"""
    p[0] = Val(-float(f'{p[2]}.{p[4]}'))


def p_float_val_comment(p):
    """expression : VAL DOT VAL COMMENT"""
    p[0] = Val(float(f'{p[1]}.{p[3]}'), p[4])


def p_die(p):
    """expression : DIE expression
    | ADVDIE expression
    | DISDIE expression
    | ELFDIE expression
    | QUADIE expression"""
    p[0] = dices[p[1]](Val(1), p[2])


def p_dice(p):
    """expression : expression DIE expression
    | expression ADVDIE expression
    | expression DISDIE expression
    | expression ELFDIE expression
    | expression QUADIE expression"""
    p[0] = dices[p[2]](p[1], p[3])


def p_die_comment(p):
    """expression : DIE expression COMMENT"""
    p[0] = DiceOperation(Val(1), p[2], p[3])


def p_dice_comment(p):
    """expression : expression DIE expression COMMENT"""
    p[0] = DiceOperation(p[1], p[3], p[4])


def p_var(p):
    """expression : VAR"""
    p[0] = Var()


def p_map(p):
    """expression : MAP LBRACKET expression ELSE expression RBRACKET"""
    p[0] = Map(p[3], p[5])


def p_error(p):
    print("Syntax error at '%s'" % p.value)
