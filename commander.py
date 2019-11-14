from expressions import d
from spells import get_spell
from random import choice

commands = {}
variants = []


def list_(res):
    if type(res) == type(tuple()):
        return list(res)
    return [res]


def handler(name, triggers):
    def dec(f):
        def f2(*args):
            res = f(*args)
            return list_(res)

        for i in triggers:
            commands[i] = f2
        variants.append((name, triggers))
        return f2

    return dec


@handler('Приветствие', ['hello', 'привет', 'hewwo', 'owo'])
def hello(*args):
    return 'hewwo OwO'


@handler('Это окно', ['помощь', 'help', 'спаси', 'справка'])
def help_list(*args):
    s = ''
    for i in variants:
        s += f'{i[0]} -- '
        for j in i[1]:
            s += f'{j}, '
        s = s[:-2] + '\n'
    s += '\nЧтобы кидать дайсы, используйте символ d(d20, 4d6+1). Чтобы кидать с преимуществом или с помехой, ' \
         'используйте обозначения ad или dd соответственно (ad20, dd20). Разрещается делать несколько бросков за раз,' \
         ' перечисляя кубы через запятую. Разрешается запускать несколько команд в одном сообщении, разделяя их точкой' \
         ' с запятой. '
    return s


@handler('Кинуть дайсы', ['roll', 'dice', 'кидай', 'кинь'])
def roll(*args):
    return d(args[0])


@handler('Описать заклинание', ['spell', 'spells', 'cast', 'закл', 'заклинание', 'спелл'])
def cast(*args):
    print(args)
    return get_spell(args[0])


@handler('Выводит да или нет', ['чекай', 'чек', 'check'])
def check(*args):
    res = choice(['ага', 'нет'])
    return res


# scrapped command
# @handler('Повторить запросы (из пересланных сообщений)', ['repeat', 'повтори', 'еще', 'ещё'])
# def repeat(*args):
#     print(args)
#     s, fwd_msg = args
#     data = []
#     for msg in fwd_msg:
#         print(msg)
#         data += execute(msg, [])
#     return data


def execute(s, fwd_msg):
    command1 = s.split()[0]
    function = commands.get(command1)
    parameters = ' '.join(s.split()[1:])
    if function:
        print('executing command', command1, 'with parameter strings', parameters.split(','))
        res = [function(argstring.strip(), fwd_msg) for argstring in parameters.split(',')]
        return res
    return None
