from random import randint


def strfy(x):
    if type(x) == list:
        res_str = '(' + ', '.join(x) + ')'
    else:
        res_str = str(x)
    return res_str


class Operation:
    """Базовый класс операции. Сохраняет в себя данные и умеет выводить их строкой."""
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
    """Математическая операция сложения. Принимает любое число слагаемых."""
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
    """Математическая операция вычитания. Принимает любое число вычитаемых."""
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
    """Математическая операция деления. Принимает любое число аргументов и делит последовательно."""
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
    """Математическая операция умножения. Принимает любое число аргументов и умножает последовательно."""
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
    """Операция броска куба, одного или нескольких."""
    value = 'd'
    overwrite_minimum = False
    overwrite_value = None

    def __init__(self, *ops, overwrite=None):
        super().__init__(*ops)
        if overwrite is not None:
            self.overwrite_minimum = True
            self.overwrite_value = overwrite.calculate()[0].ops[0]

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

    def get_result(self, die_size):
        roll = randint(1, die_size)
        if self.overwrite_minimum and roll < self.overwrite_value:
            return self.overwrite_value, f'[~~{roll}~~|**{self.overwrite_value}**] + '
        return roll, f'[**{roll}**] + '

    @staticmethod
    def bold_the_result(result, *rolls):
        s = '|'+'|'.join(map(str, rolls))
        return s.replace(f'|{result}', f'|**{result}**')[1:]


class ExplodingDiceOperation(DiceOperation):
    value = 'b'

    def get_result(self, die_size):
        rolls_total = []
        rolls_sum = 0
        times_to_roll = 1
        rollings = 0
        while rollings < times_to_roll:
            rollings += 1
            roll = randint(1, die_size)
            rolls_sum += roll
            rolls_total.append(str(roll))
            if roll == die_size and die_size > 1:
                times_to_roll += 1
        return rolls_sum, f'[**{"**+**".join(rolls_total)}**] + '


class AdvantageDiceOperation(DiceOperation):
    """Операция броска куба с преимуществом."""
    value = 'ad'

    def get_result(self, die_size):
        roll1 = randint(1, die_size)
        roll2 = randint(1, die_size)
        roll = max(roll1, roll2)
        if self.overwrite_minimum and roll < self.overwrite_value:
            return self.overwrite_value, f'a[~~{roll1}~~|~~{roll2}~~|**{self.overwrite_value}**] + '
        return roll, f'a[{self.bold_the_result(roll, roll1, roll2)}] + '


class DisadvantageDiceOperation(DiceOperation):
    """Операция броска куба с помехой."""
    value = 'dd'

    def get_result(self, die_size):
        roll1 = randint(1, die_size)
        roll2 = randint(1, die_size)
        roll = min(roll1, roll2)
        if self.overwrite_minimum and roll < self.overwrite_value:
            return self.overwrite_value, f'd[~~{roll1}~~|~~{roll2}~~|**{self.overwrite_value}**] + '
        return roll, f'd[{self.bold_the_result(roll, roll1, roll2)}] + '


class ElfAdvantageDiceOperation(DiceOperation):
    """Операция броска куба с эльфийским преимуществом (3 куба)."""
    value = 'ed'

    def get_result(self, die_size):
        roll1 = randint(1, die_size)
        roll2 = randint(1, die_size)
        roll3 = randint(1, die_size)
        roll = max(roll1, roll2, roll3)
        if self.overwrite_minimum and roll < self.overwrite_value:
            return self.overwrite_value, f'e[~~{roll1}~~|~~{roll2}~~|~~{roll3}~~|**{self.overwrite_value}**] + '
        return roll, f'e[{self.bold_the_result(roll, roll1, roll2, roll3)}] + '


class QuadAdvantageDiceOperation(DiceOperation):
    """Операция броска куба с четверным преимуществом (4 куба)."""
    value = 'kd'

    def get_result(self, die_size):
        roll1 = randint(1, die_size)
        roll2 = randint(1, die_size)
        roll3 = randint(1, die_size)
        roll4 = randint(1, die_size)
        roll = max(roll1, roll2, roll3, roll4)
        if self.overwrite_minimum and roll < self.overwrite_value:
            return self.overwrite_value, f'k[~~{roll1}~~|~~{roll2}~~|~~{roll3}~~|~~{roll4}~~|**{self.overwrite_value}**] + '
        return roll, f'k[{self.bold_the_result(roll, roll1, roll2, roll3, roll4)}] + '


class CommaOperation(Operation):
    """Конвертор нескольких чисел в объект MultipleVals."""
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
        result = MultipleVals()
        for i in range(len(self.ops)):
            val, text = self.ops[i].calculate(args)
            elems1.append(val)
            elems2.append(text)
            result.types.setdefault(val.ops[1], []).append(i)
        result.ops = [elems1, elems2]
        return result, result.ops[1]

    def simplify(self):
        pass

    def __str__(self):
        return str(tuple(self.ops))

    def __repr__(self):
        return self.__str__()


class MultipleVals(Operation):
    """Несколько чисел, разделяются запятой и выводятся в скобках."""
    value = ';'
    types = dict()

    def calculate(self, args=None):
        return self.ops[0], self.ops[1]

    def simplify(self):
        pass

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
        elif other.value == ';':
            self.ops[0] += other.ops[0]
            self.ops[1] += other.ops[1]
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

    def __str__(self):
        return str(tuple(self.ops[0]))

    def __repr__(self):
        return self.__str__()


class FunctionOfMultipleVars(Operation):
    """Базовый класс операции применения функции к нескольким числам."""
    value = 'func'
    func = None

    def calculate(self, args=None):
        calced = self.ops[0].calculate(args)
        sol = calced[1]
        if isinstance(sol, str):
            sol = [sol]
        to_sum = calced[0].ops[0]
        if isinstance(calced[0], Val):
            to_sum = [calced[0]]
        return self.func(to_sum), f'{self.value}({", ".join(sol)})'

    def __str__(self):
        str_ = f'{self.value}('
        for i in self.ops:
            str_ += f'{i}, '
        return str_[:-2]+')'


class MinFunction(FunctionOfMultipleVars):
    """Математическая функция минимума из нескольких чисел."""
    value = 'min'
    func = min


class MaxFunction(FunctionOfMultipleVars):
    """Математическая функция максимума из нескольких чисел."""
    value = 'max'
    func = max


class SumFunction(FunctionOfMultipleVars):
    """Математическая функция суммы нескольких чисел."""
    value = 'sum'
    func = sum


class Greater(Operation):
    """Математическая функция сравнения двух чисел. Возвращает 0 или 1."""
    value = '>'

    def calculate(self, args=None):
        first, second = self.ops[0].calculate(args), self.ops[1].calculate(args)
        return Val(first[0] > second[0]), f'{first[1]} {self.value} {second[1]}'


class Lesser(Operation):
    """Математическая функция сравнения двух чисел. Возвращает 0 или 1."""
    value = '<'

    def calculate(self, args=None):
        first, second = self.ops[0].calculate(args), self.ops[1].calculate(args)
        return Val(first[0] < second[0]), f'{first[1]} {self.value} {second[1]}'


class GreaterEquals(Operation):
    """Математическая функция сравнения двух чисел. Возвращает 0 или 1."""
    value = '>='

    def calculate(self, args=None):
        first, second = self.ops[0].calculate(args), self.ops[1].calculate(args)
        return Val(first[0] >= second[0]), f'{first[1]} {self.value} {second[1]}'


class LesserEquals(Operation):
    """Математическая функция сравнения двух чисел. Возвращает 0 или 1."""
    value = '<='

    def calculate(self, args=None):
        first, second = self.ops[0].calculate(args), self.ops[1].calculate(args)
        return Val(first[0] <= second[0]), f'{first[1]} {self.value} {second[1]}'


class Equals(Operation):
    """Математическая функция сравнения двух чисел. Возвращает 0 или 1."""
    value = '='

    def calculate(self, args=None):
        first, second = self.ops[0].calculate(args), self.ops[1].calculate(args)
        return Val(first[0] == second[0]), f'{first[1]} {self.value} {second[1]}'


class NotEquals(Operation):
    """Математическая функция сравнения двух чисел. Возвращает 0 или 1."""
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


class Map(Operation):
    value = 'map'

    def calculate(self, args=None):
        values = self.ops[1].calculate()[0].ops
        print(values)
        ress1, ress2 = [], []
        for i in range(len(values[0])):
            res1, res2 = self.ops[0].calculate((values[0][i], values[1][i]))
            ress1.append(res1)
            ress2.append(res2)
        result = CommaOperation(*ress1).calculate()
        return result[0], values[1]

    def __str__(self):
        return f'checking ({self.ops[0]} for {self.ops[1]}'


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
            self.ops = (self.ops[0], '')

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
        if other.value == ';':
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
        if other.value == ';':
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
        if other.value == ';':
            return other.__mul__(self)
        num1, type1 = self.ops
        num2, type2 = other.ops
        if type1 and type2:
            if type1 == type2:
                return Val(num1 * num2, type1)
            raise SyntaxError("я не умею перемножать типы урона, додик")
        return Val(num1 * num2, max(type1, type2))

    def __truediv__(self, other):
        if other.value == ';':
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