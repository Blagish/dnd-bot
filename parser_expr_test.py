from ply_data import *
import ply.lex as lex
import ply.yacc as yacc

t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'\/'
t_VAL = r'[0-9]+'
t_DOT = r'\.'
t_VAR = r'it'
t_LBRACKET = r'\('
t_RBRACKET = r'\)'
t_SLBRACKET = r'\['
t_SRBRACKET = r'\]'
t_COMMA = r'\,'
t_SEMICOLON = r'\;'
t_FOR = r'x'
t_DIE = r'd'
t_ADVDIE = r'ad'
t_DISDIE = r'dd'
t_ELFDIE = r'ed'
t_QUADIE = r'kd'
t_MAX = r'max'
t_MIN = r'min'
t_MAP = r'map'
t_SUM = r'sum'
t_BIGGER = r'\>'
t_LESSER = r'\<'
t_EQUAL = r'\='
t_NOTEQUAL1 = r'≠'
t_NOTEQUAL2 = r'\!\='
t_BIGGEREQUAL = r'\>\=|\=\>'
t_LESSEREQUAL = r'\<\=|\=\<'
t_IF = '\?'
t_ELSE = '\:'
t_ARG = r'gwf|ea|rt|st'
t_ignore = ' \n\t'


def t_COMMENT(t):
    r"""[a-zA-Zа-яА-ЯёЁ]+"""
    if t.value in function_keywords:  # is this a keyword
        t.type = function_keywords[t.value]
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
parser = yacc.yacc()


def parse(expression):
    result = parser.parse(expression)
    return result


def test(expression):
    lexer.input(expression)
    for tok in lexer:
        print(tok)


def d2(expression):
    expression = expression.replace('х', 'x')
    expression = expression.replace('а', 'a')
    expression = expression.replace('е', 'e')
    expression = expression.replace('д', 'd')
    expression = expression.replace('к', 'k')
    res = parse(expression)
    ans, sol = res.calculate()
    if type(sol) == list:
        sol = '('+', '.join(sol)+')'
    return sol, ans