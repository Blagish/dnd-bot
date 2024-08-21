from app.parser.ply_data import *
import ply.lex as lex
import ply.yacc as yacc
import re

t_ADD = r"\+"
t_SUB = r"-"
t_MUL = r"\*"
t_DIV = r"\/"
t_VAL = r"[0-9]+"
t_DOT = r"\."
t_VAR = r"it"
t_LBRACKET = r"\("
t_RBRACKET = r"\)"
t_SLBRACKET = r"\["
t_SRBRACKET = r"\]"
t_COMMA = r"\,"
t_SEMICOLON = r"\;"
t_FOR = r"x"
t_DIE = r"d"
t_PICK = r"p"
t_BOOMDIE = r"b"
t_ADVDIE = r"ad"
t_DISDIE = r"dd"
t_ELFDIE = r"ed"
t_QUADIE = r"kd"
t_DIEMOD = r"\%"
t_MAX = r"max"
t_MIN = r"min"
t_MAP = r"map"
t_SUM = r"sum"
t_BIGGER = r"\>"
t_LESSER = r"\<"
t_EQUAL = r"\="
t_NOTEQUAL1 = r"≠"
t_NOTEQUAL2 = r"\!\="
t_BIGGEREQUAL = r"\>\=|\=\>"
t_LESSEREQUAL = r"\<\=|\=\<"
t_IF = "\?"
t_ELSE = "\:"
t_ARG = r"gwf|ea|rt|st"
t_ignore = " \n\t"


def t_COMMENT(t):
    r"""[a-zA-Zа-яА-ЯёЁ_]+"""
    if t.value in function_keywords:  # is this a keyword
        t.type = function_keywords[t.value]
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
parser = yacc.yacc()


def parse(expression):
    result = parser.parse(expression.lower())
    return result


def test(expression):
    lexer.input(expression)
    for tok in lexer:
        print(tok)


def d2(expression):
    expression = re.sub(" {2,}", " ", expression)
    expression = re.sub("(?<=[a-zA-Zа-яА-ЯёЁ]) (?=[a-zA-Zа-яА-ЯёЁ])", "_", expression)
    res = parse(expression)
    ans = res.calculate()
    ans.simplify()
    sol = ans.verbose.replace("_", " ")
    ans = ans.answer.replace("_", " ")
    return sol, ans


if __name__ == "__main__":
    expr = "d20+10, d20+8"
    # expr = 'sum(map(((it=2)+(it=4)+2*(it=6)):9x(d6)))'
    # expr = 'sum(map(((it=2)+(it=4)+(it=6)):5x(d6)))'
    # expr = '10x(1=d2)'
    # expr = '(it=2) + (it=4) + 2*(it=6)'.replace('it', '3')
    # expr = '10x(ad20+1)'
    sol, ans = d2(expr)
    s = f"Кидаю\n{sol}\n**{ans}**"
    s = s.replace("\n", "\n-> ")
    # s = s.replace('\n', '= ')
    # print(s)
    print(f"{sol=}, {ans=}")
