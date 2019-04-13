from expressions import d

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
        return s[i+2:]
    return s

@handler('Приветствие', ['hello', 'привет', 'hewwo'])
def hello(*args):
    return 'hewwo OwO'


@handler('Это окно',['помощь', 'help', 'спаси', 'справка'])
def help(*args):
    s = ''
    for i in variants:
        s += f'{i[0]} -- '
        for j in i[1]:
            s += f'{j}, '
        s = s[:-2] + '\n'
    return s

@handler('Кинуть дайсы', ['roll', 'dice', 'кидай', 'кинь'])
def roll(*args):
    return d(args[0])

@handler('Повторить запросы (из пересланных сообщений)', ['repeat', 'повтори', 'еще', 'ещё'])
def repeat(*args):
    print(args)
    s, fwd_msg = args
    data = []
    for msg in fwd_msg:
        print(msg)
        data.append(execute(msg, []))  
    return tuple(data)
#    return d(s)

def execute(s0, fwd_msg):
    if s0 != '':
        s = detect_command(s0)
        command1 = s.split()[0]
        function = commands.get(command1)
        if function:
            return function(s, fwd_msg)
        return None
    return None
