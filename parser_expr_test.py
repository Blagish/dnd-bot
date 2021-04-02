from ply_data import *
import ply.lex as lex
import ply.yacc as yacc

t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'\/'
t_VAL = r'[0-9]+'
t_LBRACKET = r'\('
t_RBRACKET = r'\)'
t_COMMA = r'\,'
t_FOR = r'x'
t_DIE = r'd'
t_MAX = r'max'
t_MIN = r'min'
t_BIGGER = r'\>'
t_LESSER = r'\<'
t_EQUAL = r'\='
t_BIGGEREQUAL = r'\>\='
t_LESSEREQUAL = r'\<\='
t_ARG = r'gwf|ea|rt|st'
t_ignore = ' \n\t'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def parse(expression):
    lex.lex()
    parser = yacc.yacc()
    result = parser.parse(expression)
    return result


a = parse('10 > 8')
print(a)
print(a.calculate())
