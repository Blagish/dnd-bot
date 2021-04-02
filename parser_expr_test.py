from ply_data import *
import ply.lex as lex
import ply.yacc as yacc

t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'\/'
t_VAL = r'[0-9]+'
t_LEFTB = r'\('
t_RIGHTB = r'\)'
t_DIE = r'd'
t_ADVDIE = r'ad'
t_DISDIE = r'dd'
t_ELFDIE = r'ed'
t_KRISDIE = r'kd'
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


print(parse('2*(d4+10)'))
