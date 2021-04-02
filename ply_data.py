from random import randint
tokens = (
    'ADD',  # +
    'SUB',  # -
    'MUL',  # *
    'DIV',  # /
    'VAL',  # 0123
    'LEFTB',  # (
    'RIGHTB',  # )
    'DIE',  # d
    'ADVDIE',  # ad
    'DISDIE',  # dd
    'ELFDIE',  # ed
    'KRISDIE',  # kd
    'ARG',  # gwf, ea, rt, st, etc.
)

precedence = (
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV'),
    ('right', 'DIE')
)

names = {}


def p_top_group(p):
    """expression : LEFTB expression RIGHTB"""
    p[0] = p[2]


def p_top_full(p):
    """expression : expression ADD expression
    | expression SUB expression
    | expression MUL expression
    | expression DIV expression"""
    left, right = p[1], p[3]
    if p[2] == '+':
        p[0] = left + right
    elif p[2] == '-':
        p[0] = left - right
    elif p[2] == '*':
        p[0] = left * right
    elif p[2] == '/':
        p[0] = left / right


def p_top_var(p):
    """expression : VAL"""
    p[0] = int(p[1])


def p_top_die(p):
    """expression : DIE expression"""
    right = p[2]
    s = 0
    s += randint(1, right)
    p[0] = s


def p_top_dice(p):
    """expression : expression DIE expression"""
    left, right = p[1], p[3]
    s = 0
    for i in range(left):
        s += randint(1, right)
    p[0] = s


def p_error(p):
    print("Syntax error at '%s'" % p.value)