from expressions import d
from spells import get_spell
from random import choice

commands = {}
help_prompts = []


def construct_prompt(tupl):
    if 'hidden' in tupl[1]:
        return ''
    s = f'{tupl[0]} -- ' + ', '.join(tupl[1]) + ';'
    return s


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
        help_prompts.append((name, triggers))
        return f2

    return dec


@handler('Приветствие', ['hello', 'привет', 'hewwo', 'owo'])
def hello(*args):
    return 'hewwo OwO'


@handler('Это окошко', ['помощь', 'help', 'спаси', 'справка', 'хелп'])
def help_list(*args):
    s = '\n'.join([construct_prompt(i) for i in help_prompts])
    s += '\n\nЧтобы кидать дайсы, используйте символ d(d20, 4d6+1). Чтобы кидать с преимуществом, супер-преимуществом (оно же эльфийское) или с помехой, ' \
         'используйте обозначения ad, ed или dd соответственно (ad20, ed20, dd20). Можно использовать Great Weapon Fighting, Elemental Adept, Reliable Talent или Halfling Lucky указывая параметр перед кубом (gwf d4+1, ea 2d6, rt, hl). Разрешается делать несколько бросков за раз,' \
         ' перечисляя кубы через запятую. Разрешается запускать несколько команд в одном сообщении, разделяя их точкой' \
         ' с запятой. '
    return s


@handler('Кинуть дайсы', ['roll', 'dice', 'кидай', 'кинь', 'r', 'р', 'к', 'k'])
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


@handler('Поблагодарить за хороший рандом', ['спасибо', 'спс', 'сепс', 'thank', 'thanks', 'thx'])
def thanks(*args):
    res = choice(['Пожалуйста!', 'Рада помочь!', 'Всегда пожалуйста', 'Стараюсь :)'])
    # res = choice(['пожалуйста', 'рад помочь', 'всегда пожалуйста', 'стараюсь'])
    return res


@handler('Поинтересоваться почему все идет не так', ['слыш', 'слышь', 'э', 'каво', 'чево', 'всмысле', 'wut', 'слiш', 'bruh', 'брух'])
def anger(*args):
    res = choice(['Виноваты кубики', 'Оно само', 'Это не я', 'Я честно не виновата', 'Все вопросы к кубам!',
                  'Это все кубики, правда!'])
    return res


#@handler('Consider donating?', ['donate', 'донат'])
#def donate(*args):
#    return 'Consider donating? Разрабам надо кушать. Ну хотя бы на чашечку кофе.'


# scrapped command
# @handler('Повторить запросы (из пересланных сообщений)', ['repeat', 'повтори', 'еще', 'ещё'])
# def repeat(*args):
#     print(args)
#     s, fwd_msg = args
#     data = []
#     for msg in fwd_msg:
#         print(msg)
#         data += execute(msg, [])
#     return dat


@handler('Портент', ['портент', 'portent', 'hidden'])
def portent(*args):
    data = ['no']
    if args[0]:
        data = args[0].split()
    mode = 'r'
    if data[0] == 'new':
        mode = 'w'
    with open('portent.txt', mode=mode) as file:
        if mode == 'r':
            s = file.readline()
        else:
            file.write(' '.join(data[1:]))
            s = 'Портент записан'
    return s


@handler('Куку', ['куку', 'hidden'])
def kuku(*args):
    return 'быбы'


def execute(s):
    command1 = s.split()[0]
    function = commands.get(command1)
    parameters = ' '.join(s.split()[1:])
    if function:
        print('executing command', command1, 'with parameter strings', parameters.split(','))
        res = [function(argstring.strip()) for argstring in parameters.split(',')]
        return res
    return None
