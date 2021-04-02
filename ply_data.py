from random import randint

tokens = (
    'ADD',  # +
    'SUB',  # -
    'MUL',  # *
    'DIV',  # /
    'VAL',  # 0123
    'LEFTB',  # (
    'RIGHTB',  # )
    'COMMA',  # ,
    'FOR',   # x
    'DIE',  # d
    'MAX',  # max
    'MIN',  # min
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
    """expression : LEFTB expression RIGHTB"""
    p[0] = (p[2][0], f'({p[2][1]})')


def p_top_minmax(p):
    """expression : MAX LEFTB expression RIGHTB
    | MIN LEFTB expression RIGHTB"""
    func = max if p[1] == 'max' else min
    p[0] = (func(p[3][0]), f'{p[1]}({p[3][1]})')

def p_top_for(p):
    """expression : expression FOR LEFTB expression RIGHTB"""
    times = p[1][0]
    p[0] = ((p[4][0],)*times, f'{times}x({(p[4][1],)*times})')


def p_top_comma(p):
    """expression : expression COMMA expression"""
    left, right = p[1][0], p[3][0]
    if type(left) != type(tuple()):
        left = (left,)
    if type(right) != type(tuple()):
        right = (right,)
    p[0] = ((left+right), f'{p[1][1]}, {p[3][1]}')


def p_top_full(p):
    """expression : expression ADD expression
    | expression SUB expression
    | expression MUL expression
    | expression DIV expression"""
    left, right = p[1][0], p[3][0]
    if p[2] == '+':
        res = left + right
    elif p[2] == '-':
        res = left - right
    elif p[2] == '*':
        res = left * right
    elif p[2] == '/':
        res = left / right

    p[0] = (res, f'{p[1][1]} {p[2]} {p[3][1]}')


def p_top_var(p):
    """expression : VAL"""
    p[0] = (int(p[1]), p[1])


def p_top_die(p):
    """expression : DIE expression"""
    right = p[2][0]
    s = 0
    s += randint(1, right)
    p[0] = (s, f'[**{s}**]')


def p_top_dice(p):
    """expression : expression DIE expression"""
    left, right = p[1][0], p[3][0]
    s = 0
    st = ''
    for i in range(left):
        roll = randint(1, right)
        s += roll
        st += f'[**{roll}**] + '
    st = st[:-3]
    p[0] = (s, st)


def p_error(p):
    print("Syntax error at '%s'" % p.value)
