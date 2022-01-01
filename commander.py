import json

from spells import get_spell_dungeon_su
from random import choice, randint
from parser_expr_test import d2

commands = {}
help_prompts = []
fate_die = ('[-]', '[ ]', '[+]')
with open('macros.json', 'r', encoding='utf-8') as file:
    macri = json.loads(file.read())


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
    s += '''\n\nЧтобы кидать дайсы, используйте символ d (как в d20, 4d6+1). Чтобы кидать с преимуществом, 
    супер-преимуществом (оно же эльфийское) или с помехой, используйте обозначения ad, ed или dd соответственно 
    (ad20, ed20, dd20). Доступны: основные математические операции, кубы, преимущество, помеха, эльфийский, 
    четверной. Сравнение выражений знаками больше и т.д. Проверка выражения на истинность. Например: 
    d20+10 > 20 ? d6+3 : 0, то есть выполнится первое если истина и второе если ложь. Использование скобок. Использование 
    нескольких команд разом: 5x(d20+10), скобки пока обязательны, можно использовать только число как коэффициент. 
    Использование математических функций sum, min, max, map. Разрушается делать несколько бросков за раз, перечисляя 
    команды кубов через запятую. Разрешается запускать несколько команд в одно сообщении, разделяя их точкой с 
    запятой. '''
    return s


@handler('Кинуть дайсы', ['roll', 'dice', 'кидай', 'кинь', 'r', 'р', 'к', 'k'])
def roll(*args):
    sol, ans = d2(args[0])
    s = f'Кидаю\n-> {sol}\n= **{ans}**'
    return s


@handler('Кинуть куб Фейта', ['f', 'ф', 'fate', 'фейт'])
def fate(*args):
    mod = args[0]
    if mod[0] != '+':
        return 'Ошибка: модификатор не найден'
    mod = int(mod[1:])
    s = 'Кидаю\n-> **'
    res = 0
    for i in range(4):
        d = randint(-1, 1)
        s += fate_die[d+1]
        res += d
    s += f'** + {mod}\n= **{res+mod}**'
    return s


@handler('Макрос', ['macros', 'macroll', 'mc', 'мк', 'макрос', 'макролл'])
def macros(*args):
    arg = args[0].split()
    command = arg.pop(0)
    true_command = macri.get(command)
    if true_command is not None:
        try:
            full = true_command[0].format(*arg)
            print(full)
        except IndexError:
            return 'Ошибка: не хватает значений.'
        sol, ans = d2(full)
        s = f'Кидаю\n-> {sol}\n{true_command[1].format(ans)}'
        return s
    return f'Ошибка: макрос "{command}" не найден.'


@handler('Доступные макросы', ['macroshelp', 'helpmacrost', 'макросхелп', 'хелпмакрос'])
def macros_list(*args):
    s = ''
    for m in macri:
        data = macri[m]
        s += f'{m}: {data[2]} Аналог команды {data[0]}.\n'
    return s


@handler('Описать заклинание', ['spell', 'spells', 'cast', 'закл', 'заклинание', 'спелл'])
def cast(*args):
    print(args)
    return get_spell_dungeon_su(args[0])


@handler('Выводит да или нет', ['чекай', 'чек', 'check'])
def check(*args):
    res = choice(['ага', 'нет'])
    return res


@handler('Поблагодарить за хороший рандом', ['спасибо', 'спс', 'сепс', 'thank', 'thanks', 'thx'])
def thanks(*args):
    res = choice(['Пожалуйста!', 'Рада помочь!', 'Всегда пожалуйста', 'Стараюсь :)'])
    # res = choice(['пожалуйста', 'рад помочь', 'всегда пожалуйста', 'стараюсь'])
    return res


@handler('Поинтересоваться почему все идет не так',
         ['слыш', 'слышь', 'э', 'каво', 'чево', 'всмысле', 'wut', 'слiш', 'bruh', 'брух'])
def anger(*args):
    res = choice(['Виноваты кубики', 'Оно само', 'Это не я', 'Я честно не виновата', 'Все вопросы к кубам!',
                  'Это все кубики, правда!'])
    return res


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
        print('executing command', command1, 'with parameter strings', parameters)
        res = [function(parameters.strip())]
        return res
    return None
