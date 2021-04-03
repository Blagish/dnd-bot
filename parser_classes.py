from random import randint


class Operation:
    verbose = True
    ops = None
    value = None

    def __init__(self, *ops):
        self.ops = ops

    def __str__(self):
        str_ = '('
        for i in self.ops:
            str_ += f'{i} {self.value} '
        return str_[:-(2+len(self.value))]+')'

    def calculate(self, args=None):
        pass


class Addition(Operation):
    value = '+'

    def calculate(self, args=None):
        res_tuple = self.ops[0].calculate(args)
        res = res_tuple[0]
        res_str = str(res_tuple[1])+' '
        for i in range(1, len(self.ops)):
            next_part = self.ops[i].calculate(args)
            res += next_part[0]
            res_str += f'{self.value} '+str(next_part[1])
        return res, res_str


class Subtraction(Operation):
    value = '-'

    def calculate(self, args=None):
        res_tuple = self.ops[0].calculate(args)
        res = res_tuple[0]
        res_str = str(res_tuple[1])+' '
        for i in range(1, len(self.ops)):
            next_part = self.ops[i].calculate(args)
            res -= next_part[0]
            res_str += f'{self.value} '+str(next_part[1])
        return res, res_str


class Division(Operation):
    value = '/'

    def calculate(self, args=None):
        res_tuple = self.ops[0].calculate(args)
        res = res_tuple[0]
        res_str = str(res_tuple[1])+' '
        for i in range(1, len(self.ops)):
            next_part = self.ops[i].calculate(args)
            res /= next_part[0]
            res_str += f'{self.value} '+str(next_part[1])
        return res, res_str


class Multiplication(Operation):
    value = '*'

    def calculate(self, args=None):
        res_tuple = self.ops[0].calculate(args)
        res = res_tuple[0]
        res_str = str(res_tuple[1])+' '
        for i in range(1, len(self.ops)):
            next_part = self.ops[i].calculate(args)
            res *= next_part[0]
            res_str += f'{self.value} '+str(next_part[1])
        return res, res_str


class DiceOperation(Operation):
    value = 'd'

    def calculate(self, args=None):
        rolls = self.ops[0].calculate(args)[0].ops[0]
        die = self.ops[1].calculate(args)[0]
        die_size = die.ops[0]
        type = die.ops[1]
        res_str = ''
        s = 0
        for i in range(rolls):
            roll = randint(1, die_size)
            s += roll
            res_str += f'[{roll}] + '
        return Val(s, type), res_str[:-3]


class CommaOperation(Operation):
    value = ','

    def __init__(self, *ops):
        super().__init__(*ops)
        self.ops = []
        for op in ops:
            if op.value == ',':
                self.ops += list(op.ops)
            else:
                self.ops.append(op)
        self.ops = tuple(self.ops)

    def calculate(self, args=None):
        calced = tuple(map(lambda x: x.calculate(args), self.ops))
        return tuple(zip(*calced))

    def __repr__(self):
        return self.__str__()


class MinFunction(Operation):
    value = 'min'

    def calculate(self, args=None):
        calced = self.ops[0].calculate(args)
        return min(calced[0]), f'{self.value}({", ".join(calced[1])})'

    def __str__(self):
        str_ = f'{self.value}('
        for i in self.ops:
            str_ += f'{i}, '
        return str_[:-2]+')'


class MaxFunction(Operation):
    value = 'max'

    def calculate(self, args=None):
        calced = self.ops[0].calculate(args)
        return max(calced[0]), f'{self.value}({", ".join(calced[1])})'

    def __str__(self):
        str_ = f'{self.value}('
        for i in self.ops:
            str_ += f'{i}, '
        return str_[:-2] + ')'


class Greater(Operation):
    value = '>'

    def calculate(self, args=None):
        first, second = self.ops[0].calculate(args), self.ops[1].calculate(args)
        return Val(first[0] > second[0]), f'{first[1]} {self.value} {second[1]}'


class Lesser(Operation):
    value = '<'

    def calculate(self, args=None):
        first, second = self.ops[0].calculate(args), self.ops[1].calculate(args)
        return Val(first[0] < second[0]), f'{first[1]} {self.value} {second[1]}'


class GreaterEquals(Operation):
    value = '>='

    def calculate(self, args=None):
        first, second = self.ops[0].calculate(args), self.ops[1].calculate(args)
        return Val(first[0] >= second[0]), f'{first[1]} {self.value} {second[1]}'


class LesserEquals(Operation):
    value = '<='

    def calculate(self, args=None):
        first, second = self.ops[0].calculate(args), self.ops[1].calculate(args)
        return Val(first[0] <= second[0]), f'{first[1]} {self.value} {second[1]}'


class Equals(Operation):
    value = '='

    def calculate(self, args=None):
        first, second = self.ops[0].calculate(args), self.ops[1].calculate(args)
        return Val(first[0] == second[0]), f'{first[1]} {self.value} {second[1]}'


class NotEquals(Operation):
    value = '!='

    def calculate(self, args=None):
        first, second = self.ops[0].calculate(args), self.ops[1].calculate(args)
        return Val(first[0] != second[0]), f'{first[1]} {self.value} {second[1]}'


class IfOperation(Operation):
    value = ('?', ':')

    def calculate(self, args=None):
        condition = self.ops[0].calculate(args)
        s = condition[1]
        if condition[0]:
            s += ' - истинно, результат = '
            calced = self.ops[1].calculate(args)
            return calced[0], s+calced[1]
        s += ' - ложно, результат = '
        calced = self.ops[2].calculate(args)
        return calced[0], s + calced[1]

    def __str__(self):
        return f'({self.ops[0]} {self.value[0]} {self.ops[1]} {self.value[1]} {self.ops[2]})'


class Error(Exception):
    pass


class LambdaVarsError(Error):
    def __init__(self, message):
        self.message = message


class Var(Operation):
    value = 'it'

    def calculate(self, args=None):
        if args is None:
            raise LambdaVarsError("Calculating lambda expression with no arguments")
        return args


class Map(Operation):  # todo output
    value = 'map'

    def calculate(self, args=None):
        return tuple([self.ops[0].calculate(i) for i in self.ops[1].calculate()])

    def __str__(self):
        return f'({self.ops[0]} mapped to {self.ops[1]}'


class SumFunction(Operation):
    value = 'sum'

    def calculate(self, args=None):
        calced = self.ops[0].calculate(args)
        return sum(calced[0]), f'{self.value}({", ".join(calced[1])})'

    def __str__(self):
        return f'(sum of {self.ops[0]})'


class Tuple(Operation):  # todo output
    value = ''

    def calculate(self, args=None):
        return self.ops[0].calculate(args),

    def __str__(self):
        return '{' + f'{self.ops[0]}' + '}'


class Val(Operation):
    def __init__(self, *ops):
        super().__init__(*ops)
        if len(self.ops) == 1:
            self.ops = self.ops + ('',)

    def calculate(self, args=None):
        if args is None:
            args = []
        if self.ops[1]:
            return self, f'{self.ops[0]} {self.ops[1]}'
        return self, f'{self.ops[0]}'

    def __str__(self):
        return str(self.ops[0])

    def __repr__(self):
        return str(self.ops[0])

    def __add__(self, other):
        num1, type1 = self.ops
        num2, type2 = other.ops
        if type1 and type2:
            return CommaOperation(self, other)
        return Val(num1 + num2, max(type1, type2))

    def __sub__(self, other):
        num1, type1 = self.ops
        num2, type2 = other.ops
        if type1 and type2:
            raise SyntaxError("как я тебе один тип урона из другого вычту, додик")
        return Val(num1 - num2, max(type1, type2))

    def __mul__(self, other):
        num1, type1 = self.ops
        num2, type2 = other.ops
        if type1 and type2:
            raise SyntaxError("я не умею перемножать типы урона, додик")
        return Val(num1 * num2, max(type1, type2))

    def __truediv__(self, other):
        num1, type1 = self.ops
        num2, type2 = other.ops
        if type1 and type2:
            raise SyntaxError("я не умею делить типы урона, додик")
        return Val(num1 / num2, max(type1, type2))

    def __lt__(self, other):
        if self.ops[0] < other.ops[0]:
            return 1
        return 0

    def __le__(self, other):
        if self.ops[0] <= other.ops[0]:
            return 1
        return 0

    def __eq__(self, other):
        if self.ops[0] == other.ops[0]:
            return 1
        return 0

    def __ne__(self, other):
        if self.ops[0] != other.ops[0]:
            return 1
        return 0

    def __gt__(self, other):
        if self.ops[0] > other.ops[0]:
            return 1
        return 0

    def __ge__(self, other):
        if self.ops[0] >= other.ops[0]:
            return 1
        return 0

