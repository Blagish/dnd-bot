import re
from random import randint

# pattern = '/roll\s+(?P<num>\d*)d(?P<dice>\d*)\s*\+\s*(?P<mod>\d*)'
command = 'roll\s+'
# command = '/roll\s+'
dice = '''([\+\-]?)     # check sign
        \s*             # remove whitespace
        (?:             # find either
        (?P<num>\d*)    # number of dice to roll
        |               # or
        (?P<adv>[ad])   # whether the roll is made with advantage
        )
        d               # any roll must contain a 'd' character
        (?P<dice>\d+)   # and the type of dice to roll
        '''
modifiers = '([\+\-])\s*(?P<mod>\d+)(?!d)'


# s = input()

def d(s):
    res = 0
    print("matched dice:", re.findall(dice, s, flags = re.X))
    output = ''
    output += 'Rolling\n'
    SIGN, NUM, ADV, DICE = 0, 1, 2, 3
    for roll in list(map(list, re.findall(dice, s, flags = re.VERBOSE))):
        mul = 1
        if roll[NUM] == '':
            roll[NUM] = '1'
        print(roll)
        for i in range(int(roll[NUM])):
            if roll[0] == '-':
                mul = -1
                output += "- "
            else:
                output += "+ "
            output += roll[ADV] + '['
            if roll[ADV] == '':
                r = randint(1, int(roll[DICE]))
                output += f'{r}] '
            else:
                r1 = randint(1, int(roll[DICE]))
                r2 = randint(1, int(roll[DICE]))
                output += f'{r1}|{r2}] '
                if roll[ADV] == 'a':
                    r = max(r1, r2)
                else:
                    r = min(r1, r2)
            res += r * mul

    for mod in re.findall(modifiers, s):
        output += f'{mod[0]} {mod[1]} '
        mul = 1
        if mod[0] == '-':
            mul = -1
        res += mul * int(mod[1])
    output += f'\n= {res}'
    return output
