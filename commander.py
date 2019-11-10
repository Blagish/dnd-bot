from expressions import d, d_adv, d_disadv
from spells import get_spell


class ZhannaError(ValueError):
    pass


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


def detect_command(s):
    if s[0] == '[':
        i = s.index(']')
        end = s[i + 2:]
        return end
    return s


@handler('Приветствие', ['hello', 'привет', 'hewwo'])
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
    return s


@handler('Кинуть дайсы', ['roll', 'dice', 'кидай', 'кинь'])
def roll(*args):
    print(args)
    return d(args[0])[0]


@handler('Кинуть с преимуществом', ['roll_a', 'dice_a', 'кидай_пр', 'кинь_пр'])
def roll(*args):
    print(args)
    return d_adv(args[0])


@handler('Кинуть с помехой', ['roll_d', 'dice_d', 'кидай_по', 'кинь_по'])
def roll(*args):
    print(args)
    return d_disadv(args[0])


@handler('Описать заклинание', ['spell', 'spells', 'cast', 'закл', 'заклинание', 'спелл'])
def cast(*args):
    print(args)
    return get_spell(args[0])


@handler('Повторить запросы (из пересланных сообщений)', ['repeat', 'повтори', 'еще', 'ещё'])
def repeat(*args):
    print(args)
    s, fwd_msg = args
    data = []
    for msg in fwd_msg:
        print(msg)
        data += execute(msg, [])
    return data


def execute(s0, fwd_msg):
    if s0 != '':
        try:
            s = detect_command(s0)
            command1 = s.split()[0]
        except IndexError:
            raise ZhannaError('Жанна')
        function = commands.get(command1)
        parameters = ' '.join(s.split()[1:])
        if function:
            print('executing command', command1, 'with parameter strings', parameters.split(','))
            res = [function(argstring.strip(), fwd_msg) for argstring in parameters.split(',')]
            return res
        return None
    return None
