import re
from random import randint


# pattern = '/roll\s+(?P<num>\d*)d(?P<dice>\d*)\s*\+\s*(?P<mod>\d*)'
command = r'roll\s+'
dice = r'''([\+\-]?)     # check sign
        (gwf)?
        (ea)?
        (rt)?
        (hl)?
        (?:          # find either
        (?P<num>\d*)    # number of dice to roll
        |             # or
        (?P<adv>[aed])   # whether the roll is made with advantage
        )
        d               # any roll must contain a 'd' character
        (?P<dice>\d+)   # and the type of dice to roll
        '''
modifiers = r'([\+\-])\s*(?P<mod>\d+)(?![dx])'
multiply = r'(\d*)x'


def roll_dice(n):
    r = randint(1, int(n))
    return r


def stat_roll():
    a = []
    for i in range(4):
        a.append(randint(1, 6))
    worst = min(a)
    used_worst = False
    output = ''
    res = 0
    for i in a:
        if i == worst and not used_worst:
            after = f'; ~~[{i}]~~'
            used_worst = True
        else:
            output += f'+ [{i}]'
            res += i
    output += after
    output += f'\n= {res}\n'
    return output


def d(s):
    s = s.replace('хл', 'hl')
    s = s.replace('х', 'x')
    s = s.replace('а', 'a')
    s = s.replace('е', 'e')
    s = s.replace('д', 'd')
    s = s.replace('гвф', 'gwf')
    s = s.replace('еа', 'ea')
    s = s.replace('рт', 'rt')
    s = s.replace('ст', 'rt')
    s = s.replace('st', 'rt')

    print("matched dice:", re.findall(dice, s.replace(' ', ''), flags=re.X))
    output = ''
    output += 'Кидаю\n'
    count = re.findall(multiply, s)
    if not count:
        count = 1
        s = '1x'+s
    elif not count[0]:
        count = 1
    else:
        count = int(count[0])
    print("count times:", count)
    print(s)
    dices = list(map(list, re.findall(dice, s.replace(' ', ''), flags=re.VERBOSE)))
    SIGN, GWF, EA, RT, HL, NUM, ADV, DICE = 0, 1, 2, 3, 4, 5, 6, 7
    for c in range(count):
        if 'aтрибут' in s:
            output += stat_roll()
            continue
        res = 0
        for roll in dices:
            s = s.replace(f'{roll[NUM]}{roll[ADV]}d{roll[DICE]}', '', 1)
            print('s:', s)
            sign = -1
            if roll[NUM] == '':
                roll[NUM] = '1'
            print(roll)
            for i in range(int(roll[NUM])):

                if roll[SIGN] != '-':
                    sign = 1
                    roll[SIGN] = '+'

                output += f'{roll[SIGN]} {roll[ADV]}'

                dice_num = roll[DICE]
                if roll[ADV] == '':
                    r = roll_dice(dice_num)
                    dice_res = '**'+str(r)+'**'
                    if roll[GWF] and (r == 1 or r == 2):
                        r_gwf = roll_dice(dice_num)
                        dice_res = f'~~{r}~~|GWF:**{r_gwf}**'
                        r = r_gwf
                    if roll[EA] and (r == 1):
                        r = 2
                        dice_res = '~~1~~|EA:**2**'
                    if roll[RT] and (r < 10):
                        dice_res = f'~~{r}~~|RT:**10**'
                        r = 10
                    if roll[HL] and (r == 1):
                        r_hl = roll_dice(dice_num)
                        dice_res = f'~~1~~|HL:**{r_hl}**'
                        r = r_hl
                else:
                    r1 = roll_dice(dice_num)
                    r2 = roll_dice(dice_num)
                    dice_res = f'**{r1}**|**{r2}**'
                    if roll[ADV] in 'aа':
                        r = max(r1, r2)
                    elif roll[ADV] in 'dд':
                        r = min(r1, r2)
                    else:
                        r3 = roll_dice(dice_num)
                        r = max(r1, r2, r3)
                        dice_res = f'**{r1}**|**{r2}**|**{r3}**'

                output += f'[{dice_res}] '
                res += sign * r
        #print('s:', s)
        for mod in re.findall(modifiers, s):
            output += f'{mod[0]} {mod[1]} '
            sign = 1
            if mod[0] == '-':
                sign = -1
            res += sign * int(mod[1])
        output += f'\n= **{res}**\n'
    return output
