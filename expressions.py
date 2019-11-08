import re
from random import randint

# pattern = '/roll\s+(?P<num>\d*)d(?P<dice>\d*)\s*\+\s*(?P<mod>\d*)'
command = 'roll\s+'
# command = '/roll\s+'
dice = '([\+\-]?)\s*(?P<num>\d*)d(?P<dice>\d*)'
modifiers = '([\+\-])\s*(?P<mod>\d+)(?!d)'


# s = input()

def d(s):
    res = 0
    print(re.findall(dice, s))
    output = ''
    output += 'Rolling\n'
    for roll in re.findall(dice, s):
        mul = 1
        if roll[1] == '':
            roll = (roll[0], '1', roll[2])
        for i in range(int(roll[1])):
            if roll[0] == '-':
                mul = -1
                output += "- ["
            else:
                output += "+ ["
            r = randint(1, int(roll[2]))
            output += f'{r}] '
            res += r * mul

    for mod in re.findall(modifiers, s):
        output += f'{mod[0]} {mod[1]} '
        mul = 1
        if mod[0] == '-':
            mul = -1
        res += mul * int(mod[1])
    output += f'\n= {res}'
    return output, res


def d_adv(s):
    a1 = d(s)
    a2 = d(s)
    output = a1[0] + '\n' + a2[0]
    output += '\nAdvantage: {max(a1[1], a2[1])}'
    return output


def d_disadv(s):
    a1 = d(s)
    a2 = d(s)
    output = a1[0] + '\n' + a2[0]
    output += '\nDisadvantage: {min(a1[1], a2[1])}'
    return output
