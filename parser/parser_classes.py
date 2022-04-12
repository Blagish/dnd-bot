from random import randint


def strfy(x):
    if type(x) == list:
        res_str = '(' + ', '.join(x) + ')'
    else:
        res_str = str(x)
    return res_str


class Operation:
    verbose = True
    ops = None
    value = None

    def __init__(self, *ops):
        self.ops = ops

    def __str__(self):
        str_ = '('
        for i in self.ops:
            str_ += f'{i} {self.value}'
        return str_[:-(2+len(self.value))]+')'

    def calculate(self, args=None):
        pass


class Addition(Operation):
    value = '+'

    def calculate(self, args=None):
        res_tuple = self.ops[0].calculate(args)
        res = res_tuple[0]
        res_str = strfy(res_tuple[1])
        for i in range(1, len(self.ops)):
            next_part = self.ops[i].calculate(args)
            res += next_part[0]
            res_str += f' {self.value} '+strfy(next_part[1])
        return res, res_str


class Subtraction(Operation):
    value = '-'

    def calculate(self, args=None):
        res_tuple = self.ops[0].calculate(args)
        res = res_tuple[0]
        res_str = strfy(res_tuple[1])
        for i in range(1, len(self.ops)):
            next_part = self.ops[i].calculate(args)
            res -= next_part[0]
            res_str += f' {self.value} '+strfy(next_part[1])
        return res, res_str


class Division(Operation):
    value = '/'

    def calculate(self, args=None):
        res_tuple = self.ops[0].calculate(args)
        res = res_tuple[0]
        res_str = strfy(res_tuple[1])
        for i in range(1, len(self.ops)):
            next_part = self.ops[i].calculate(args)
            res /= next_part[0]
            res_str += f' {self.value} '+strfy(next_part[1])
        res.simplify()
        return res, res_str


class Multiplication(Operation):
    value = '*'

    def calculate(self, args=None):
        res_tuple = self.ops[0].calculate(args)
        res = res_tuple[0]
        res_str = strfy(res_tuple[1])
        for i in range(1, len(self.ops)):
            next_part = self.ops[i].calculate(args)
            res *= next_part[0]
            res_str += f' {self.value} '+strfy(next_part[1])
        res.simplify()
        return res, res_str


class DiceOperation(Operation):
    value = 'd'

    def calculate(self, args=None):
        rolls = self.ops[0].calculate(args)[0].ops[0]
        die = self.ops[1].calculate(args)[0]
        die_size = die.ops[0]
        type = die.ops[1]
        if len(self.ops) > 2:
            type = self.ops[2]
        res_str = ''
        s = 0
        for i in range(rolls):
            roll, ress = self.get_result(die_size)
            s += roll
            res_str += ress
        return Val(s, type), (res_str[:-2]+type).strip()

    @staticmethod
    def get_result(die_size):
        roll = randint(1, die_size)
        return roll, f'[**{roll}**] + '


class AdvantageDiceOperation(DiceOperation):
    value = 'ad'

    @staticmethod
    def get_result(die_size):
        roll1 = randint(1, die_size)
        roll2 = randint(1, die_size)
        roll = max(roll1, roll2)
        return roll, f'a[{roll1}|{roll2}] + '


class DisadvantageDiceOperation(DiceOperation):
    value = 'dd'

    @staticmethod
    def get_result(die_size):
        roll1 = randint(1, die_size)
        roll2 = randint(1, die_size)
        roll = min(roll1, roll2)
        return roll, f'd[{roll1}|{roll2}] + '


class ElfAdvantageDiceOperation(DiceOperation):
    value = 'ed'

    @staticmethod
    def get_result(die_size):
        roll1 = randint(1, die_size)
        roll2 = randint(1, die_size)
        roll3 = randint(1, die_size)
        roll = max(roll1, roll2, roll3)
        return roll, f'e[{roll1}|{roll2}|{roll3}] + '


class QuadAdvantageDiceOperation(DiceOperation):
    value = 'kd'

    @staticmethod
    def get_result(die_size):
        roll1 = randint(1, die_size)
        roll2 = randint(1, die_size)
        roll3 = randint(1, die_size)
        roll4 = randint(1, die_size)
        roll = max(roll1, roll2, roll3, roll4)
        return roll, f'k[{roll1}|{roll2}|{roll3}|{roll4}] + '


class CommaOperation(Operation):  # на данный момент есть два разных типа коммаоперейшн. один - посчитанный, второй -
    # нет. в первом опс это слагаемые, во втором - уже сам ответ. надо это исправить
    value = ','
    types = dict()

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
        elems1 = []
        elems2 = []
        for i in range(len(self.ops)):
            val, text = self.ops[i].calculate(args)
            elems1.append(val)
            elems2.append(text)
            self.types.setdefault(val.ops[1], []).append(i)
        self.ops = [elems1, elems2]
        return self, self.ops[1]

    def simplify(self):
        pass

    def __str__(self):
        return str(tuple(self.ops[0]))

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        if other.value == 'val':
            num, type1 = other.ops
            if self.types.get(type1) is None:
                self.ops[0].append(other)
                self.ops[1].append(str(other))
                self.types[type1] = [len(self.ops[0])-1]
            else:
                index = self.types.get(type1)[0]
                self.ops[0][index] += other
                self.ops[1][index] += f' + {other}'
        return self

    def __sub__(self, other):
        if other.value == 'val':
            num, type1 = other.ops
            if self.types.get(type1) is None:
                new_num = Val(-num, type1)
                self.ops[0].append(new_num)
                self.ops[1].append(str(new_num))
                self.types[type1] = [len(self.ops[0])-1]
            else:
                index = self.types.get(type1)[0]
                self.ops[0][index] -= other
                self.ops[1][index] += f' - {other}'
        return self

    def __mul__(self, other):
        if other.value == 'val':
            for i in range(len(self.ops[0])):
                self.ops[0][i] *= other
        return self

    def __truediv__(self, other):
        if other.value == 'val':
            for i in range(len(self.ops[0])):
                self.ops[0][i] /= other
        return self


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
        print(first)
        print(second)
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
    value = '≠'

    def calculate(self, args=None):
        first, second = self.ops[0].calculate(args), self.ops[1].calculate(args)
        return Val(first[0] != second[0]), f'{first[1]} {self.value} {second[1]}'


class IfOperation(Operation):
    value = ('?', ':')

    def calculate(self, args=None):
        condition = self.ops[0].calculate(args)
        s = condition[1]
        if condition[0].ops[0]:
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
        values = self.ops[1].calculate()[0].ops
        print(values)
        ress1, ress2 = [], []
        for i in range(len(values[0])):
            res1, res2 = self.ops[0].calculate((values[0][i], values[1][i]))
            ress1.append(res1)
            ress2.append(res2)
        return tuple(ress1), values[1]

    def __str__(self):
        return f'checking ({self.ops[0]} for {self.ops[1]}'


class SumFunction(Operation):
    value = 'sum'

    def calculate(self, args=None):
        calced = self.ops[0].calculate(args)
        return sum(calced[0]), f'{self.value}({", ".join(calced[1])})'

    def __str__(self):
        return f'(sum of {self.ops[0]})'


class CountFunction(Operation):
    value = 'count'

    def calculate(self, args=None):
        pass


class Tuple(Operation):  # todo output
    value = ''

    def calculate(self, args=None):
        return self.ops[0].calculate(args),

    def __str__(self):
        return '{' + f'{self.ops[0]}' + '}'


class Val(Operation):
    value = 'val'

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

    def simplify(self):
        num = self.ops[0]
        if int(num) == num:
            self.ops = (int(num), self.ops[1])
        else:
            self.ops = (round(num, 5), self.ops[1])

    def __str__(self):
        return f'{self.ops[0]} {self.ops[1]}'.strip()

    def __repr__(self):
        return f'{self.ops[0]} {self.ops[1]}'.strip()

    def __add__(self, other):
        if other.value == ',':
            return other.__add__(self)
        num1, type1 = self.ops
        num2, type2 = other.ops
        if type1 and type2:
            if type1 == type2:
                return Val(num1 + num2, type1)
            return CommaOperation(self, other).calculate()[0]
        return Val(num1 + num2, max(type1, type2))

    def __radd__(self, other):
        num1, type1 = self.ops
        if type(other) == int:
            return Val(other + num1, type1)
        if other.value == ',':
            return other.__add__(self)
        num2, type2 = other.ops
        return Val(num1 + num2, type1)

    def __sub__(self, other):
        if other.value == '-':
            return other.__sub__(self)
        num1, type1 = self.ops
        num2, type2 = other.ops
        if type1 and type2:
            if type1 == type2:
                return Val(num1 - num2, type1)
            raise SyntaxError("как я тебе один тип урона из другого вычту, додик")
        return Val(num1 - num2, max(type1, type2))

    def __rsub__(self, other):
        num1, type1 = self.ops
        if type(other) == int:
            return Val(other - num1, type1)
        if other.value == '-':
            return other.__sub__(self)
        num2, type2 = other.ops
        if type1 and type2:
            if type1 == type2:
                return Val(num1 - num2, type1)
            raise SyntaxError("как я тебе один тип урона из другого вычту, додик")
        return Val(num1 - num2, max(type1, type2))

    def __mul__(self, other):
        if other.value == ',':
            return other.__mul__(self)
        num1, type1 = self.ops
        num2, type2 = other.ops
        if type1 and type2:
            if type1 == type2:
                return Val(num1 * num2, type1)
            raise SyntaxError("я не умею перемножать типы урона, додик")
        return Val(num1 * num2, max(type1, type2))

    def __truediv__(self, other):
        if other.value == ',':
            return other.__truediv__(self)
        num1, type1 = self.ops
        num2, type2 = other.ops
        if type1 and type2:
            if type1 == type2:
                return Val(num1 / num2, type1)
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


class Bool(Operation):
    def __init__(self, *ops):
        super().__init__(*ops)
        if self.ops[0]:
            self.ops = (1, 'True')
        else:
            self.ops = (0, 'False')

    def calculate(self, args=None):
        if args is None:
            args = []
        return self, self.ops[1]

    def __str__(self):
        return self.ops[1]

    def __repr__(self):
        return self.ops[1]

#    def __add__(self, other):
#        num1, type1 = self.ops
#        num2, type2 = other.ops
#        if type1 and type2:
#            return CommaOperation(self, other)
#        return Val(num1 + num2, max(type1, type2))
#
#    def __radd__(self, other):  # for sum function only
#        num1, type1 = self.ops
#        num2 = other
#        return Val(num1 + num2, type1)
#
#    def __sub__(self, other):
#        num1, type1 = self.ops
#        num2, type2 = other.ops
#        if type1 and type2:
 #           raise SyntaxError("как я тебе один тип урона из другого вычту, додик")
#        return Val(num1 - num2, max(type1, type2))
#
#    def __mul__(self, other):
#        num1, type1 = self.ops
#        num2, type2 = other.ops
#        if type1 and type2:
#            raise SyntaxError("я не умею перемножать типы урона, додик")
#        return Val(num1 * num2, max(type1, type2))
#
#    def __truediv__(self, other):
#        num1, type1 = self.ops
#        num2, type2 = other.ops
#        if type1 and type2:
#            raise SyntaxError("я не умею делить типы урона, додик")
#        return Val(num1 / num2, max(type1, type2))
#
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