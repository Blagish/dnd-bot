from expressions import d

commands = {}

def handler(triggers):
    def dec(f):
        def f2(*args):
            res = f(*args)
            if type(res) == type(tuple()):
                return list(res)
            return [res]
        for i in triggers:
            commands[i] = f2
        return f2
    return dec


def detect_command(s):
    if s[0] == '[':
        i = s.index(']')
        return s[i+2:]
    return s

@handler(['hello', 'привет', 'hewwo'])
def hello(*args):
    return 'hewwo OwO'


@handler(['помощь', 'help', 'спаси', 'справка'])
def help(*args):
    s = '''Справка:
помощь - помощь
roll - роллить кубеки'''
    return s

@handler(['roll', 'dice', 'кидай', 'кинь'])
def roll(*args):
    return d(args[0])

@handler(['repeat', 'повтори', 'еще', 'ещё'])
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
