from expressions import d

commands = {}

def handler(triggers):
    def dec(f):
        def f2(s):
            return f(s)
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
def hello(s):
    return 'hewwo OwO'


@handler(['помощь', 'help', 'спаси', 'справка'])
def help(s):
    s = '''Справка:
помощь - помощь
roll - роллить кубеки'''
    return s

@handler(['roll', 'dice', 'кидай', 'кинь'])
def roll(s):
    return d(s)

def execute(s0):
    s = detect_command(s0).split()
    command1 = s[0] #ls
    if len(s) == 1:
        command2 = ''
    else:
        command2 = s[1] #conversation
    result = [commands.get(command1), commands.get(command2)]
    result.remove(None)
    return result[0](s0)
