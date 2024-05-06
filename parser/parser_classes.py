from random import randint


class Operation:
    """Базовый класс операции. Сохраняет в себя данные и умеет выводить их строкой."""
    verbose = None
    sign = None
    value = None
    modifier = None
    comment = None

    def __init__(self, value, value2=None, comment=None, verbose=None):
        self.value = value
        self.value2 = value2
        self.comment = comment
        self.verbose = verbose

    def __str__(self):
        return f'{self.value}{self.sign}{self.value2}'

    def calculate(self, args=None):
        if self.value and not isinstance(self.value, Val) and not isinstance(self.value, MultipleVals):
            self.value = self.value.calculate()
        if self.value2 and not isinstance(self.value2, Val) and not isinstance(self.value2, MultipleVals):
            self.value2 = self.value2.calculate()


class Addition(Operation):
    """Математическая операция сложения"""
    sign = '+'

    def calculate(self, args=None):
        super().calculate()
        return (self.value + self.value2).calculate()


class Subtraction(Operation):
    """Математическая операция вычитания. Принимает любое число вычитаемых."""
    sign = '-'

    def calculate(self, args=None):
        super().calculate()
        return (self.value - self.value2).calculate()


class Division(Operation):
    """Математическая операция деления. Принимает любое число аргументов и делит последовательно."""
    sign = '/'

    def calculate(self, args=None):
        super().calculate()
        return (self.value / self.value2).calculate()


class Multiplication(Operation):
    """Математическая операция умножения. Принимает любое число аргументов и умножает последовательно."""
    sign = '*'

    def calculate(self, args=None):
        super().calculate()
        return (self.value * self.value2).calculate()


class DiceOperation(Operation):
    """Операция броска куба, одного или нескольких."""
    sign = 'd'
    overwrite_minimum = False
    overwrite_value = None
    pick = None

    def __init__(self, *args, overwrite=None, pick=None, **kwargs):
        super().__init__(*args, **kwargs)
        if pick:
            self.pick = pick.calculate()
        if overwrite is not None:
            self.overwrite_minimum = True
            self.overwrite_value = overwrite.calculate().value

    def calculate(self, args=None):
        super().calculate()
        results = []
        for i in range(self.value.value):
            s_, res_ = self.get_result(self.value2.value)
            results.append((s_, res_, i))
        s, res_str = self.pick_result(results)
        comment = self.value2.comment or self.comment
        return Val(s, comment=comment, verbose=(res_str[:-2] + (self.comment or '')).strip())

    def pick_result(self, results):
        s = 0
        res_str = ''
        if self.pick is not None:
            res_str = 'Выкинуто: '
            for i in results:
                res_str += i[1]
            res_str = res_str.replace(' + ', ', ').replace('*', '')
            res_str += '\n->'
            results.sort(key=lambda x: x[0], reverse=True)
            results = results[:self.pick.value]
            results.sort(key=lambda x: x[2])
        if len(results) == 0:
            res_str += '  '  # just for aesthetics
        for i, j, id_ in results:
            s += i
            res_str += j
        return s, res_str

    def get_result(self, die_size):
        roll = randint(1, die_size)
        if self.overwrite_minimum and roll < self.overwrite_value:
            return self.overwrite_value, f'[~~{roll}~~|**{self.overwrite_value}**] + '
        return roll, f'[**{roll}**] + '

    @staticmethod
    def bold_the_result(result, *rolls):
        s = '|' + '|'.join(map(str, rolls))
        return s.replace(f'|{result}', f'|**{result}**')[1:]


class ExplodingDiceOperation(DiceOperation):
    sign = 'b'

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
    sign = 'ad'

    def get_result(self, die_size):
        roll1 = randint(1, die_size)
        roll2 = randint(1, die_size)
        roll = max(roll1, roll2)
        if self.overwrite_minimum and roll < self.overwrite_value:
            return self.overwrite_value, f'a[~~{roll1}~~|~~{roll2}~~|**{self.overwrite_value}**] + '
        return roll, f'a[{self.bold_the_result(roll, roll1, roll2)}] + '


class DisadvantageDiceOperation(DiceOperation):
    """Операция броска куба с помехой."""
    sign = 'dd'

    def get_result(self, die_size):
        roll1 = randint(1, die_size)
        roll2 = randint(1, die_size)
        roll = min(roll1, roll2)
        if self.overwrite_minimum and roll < self.overwrite_value:
            return self.overwrite_value, f'd[~~{roll1}~~|~~{roll2}~~|**{self.overwrite_value}**] + '
        return roll, f'd[{self.bold_the_result(roll, roll1, roll2)}] + '


class ElfAdvantageDiceOperation(DiceOperation):
    """Операция броска куба с эльфийским преимуществом (3 куба)."""
    sign = 'ed'

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
    sign = 'kd'

    def get_result(self, die_size):
        roll1 = randint(1, die_size)
        roll2 = randint(1, die_size)
        roll3 = randint(1, die_size)
        roll4 = randint(1, die_size)
        roll = max(roll1, roll2, roll3, roll4)
        if self.overwrite_minimum and roll < self.overwrite_value:
            return self.overwrite_value, f'k[~~{roll1}~~|~~{roll2}~~|~~{roll3}~~|~~{roll4}~~|**{self.overwrite_value}**] + '
        return roll, f'k[{self.bold_the_result(roll, roll1, roll2, roll3, roll4)}] + '


class MultipleVals(Operation):
    """Несколько чисел, разделяются запятой и выводятся в скобках."""
    sign = ','
    types = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = [self.value]
        if self.value2:
            if isinstance(self.value2, MultipleVals):
                self.value += self.value2.value
                self.value2 = None
            else:
                self.value.append(self.value2)
        self.types = {}

    def simplify(self):
        pass

    @property
    def answer(self):
        return f'{self.sign} '.join(map(lambda x: x.answer, self.value))

    def calculate(self, args=None):
        vals = []
        verboses = []
        for i in self.value:
            val = i.calculate(args)
            verboses.append(val.verbose)
            vals.append(val)
            self.value = vals
        self.verbose = f'{self.sign} '.join(verboses)
        return self

    def __add__(self, other):
        if isinstance(other, MultipleVals):
            new_mult_vals = MultipleVals()
            new_mult_vals.value = self.value
            new_mult_vals.types = self.types
            for val in other.value:
                new_mult_vals += val
            return new_mult_vals
        elif isinstance(other, Val):
            if self.types.get(other.comment) is None:
                self.value.append(other)
                self.types[other.comment] = len(self.value)-1
            else:
                index = self.types.get(other.comment)
                self.value[index] += other
        return self

    def __sub__(self, other):
        if isinstance(other, MultipleVals):
            new_mult_vals = MultipleVals()
            new_mult_vals.value = self.value
            new_mult_vals.types = self.types
            for val in other.value:
                new_mult_vals -= val
            return new_mult_vals
        elif isinstance(other, Val):
            if self.types.get(other.comment) is None:
                self.value.append(other)
                self.types[other.comment] = len(self.value)-1
            else:
                index = self.types.get(other.comment)
                self.value[index] -= other
        return self

    def __mul__(self, other):
        if isinstance(other, Val):
            for i in range(len(self.value)):
                self.value[i] *= other
        return self

    def __truediv__(self, other):
        if isinstance(other, Val):
            for i in range(len(self.value)):
                self.value[i] /= other
        return self

    def __str__(self):
        return str(tuple(self.value))

    def __repr__(self):
        return self.__str__()

    def __bool__(self):
        return bool(self.value)


class FunctionOfMultipleVars(Operation):
    """Базовый класс операции применения функции к нескольким числам."""
    sign = 'func'
    func = None

    def calculate(self, args=None):
        super().calculate()
        self.value.calculate()
        res = self.func(self.value.value)
        res.verbose = f'{self.sign}({self.value.verbose})'
        return res


class MinFunction(FunctionOfMultipleVars):
    """Математическая функция минимума из нескольких чисел."""
    sign = 'min'
    func = min


class MaxFunction(FunctionOfMultipleVars):
    """Математическая функция максимума из нескольких чисел."""
    sign = 'max'
    func = max


class SumFunction(FunctionOfMultipleVars):
    """Математическая функция суммы нескольких чисел."""
    sign = 'sum'
    func = sum


class Greater(Operation):
    """Математическая функция сравнения двух чисел. Возвращает 0 или 1."""
    sign = '>'

    def calculate(self, args=None):
        super().calculate()
        return Val(self.value > self.value2).calculate()


class Lesser(Operation):
    """Математическая функция сравнения двух чисел. Возвращает 0 или 1."""
    sign = '<'

    def calculate(self, args=None):
        super().calculate()
        return Val(self.value < self.value2).calculate()


class GreaterEquals(Operation):
    """Математическая функция сравнения двух чисел. Возвращает 0 или 1."""
    sign = '>='

    def calculate(self, args=None):
        super().calculate()
        return Val(self.value >= self.value2).calculate()


class LesserEquals(Operation):
    """Математическая функция сравнения двух чисел. Возвращает 0 или 1."""
    sign = '<='

    def calculate(self, args=None):
        super().calculate()
        return Val(self.value <= self.value2).calculate()


class Equals(Operation):
    """Математическая функция сравнения двух чисел. Возвращает 0 или 1."""
    sign = '='

    def calculate(self, args=None):
        super().calculate()
        return Val(self.value == self.value2).calculate()


class NotEquals(Operation):
    """Математическая функция сравнения двух чисел. Возвращает 0 или 1."""
    sign = '≠'

    def calculate(self, args=None):
        super().calculate()
        return Val(self.value != self.value2).calculate()


class IfOperation(Operation):
    sign = ('?', ':')
    value3 = None

    def __init__(self, *args, value3=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.value3 = value3

    def calculate(self, args=None):
        # value3 - выражение для проверки
        super().calculate()
        if self.value3.calculate():
            s = f'{self.value3} - истинно, результат = '
            self.value.verbose = s + self.value.verbose
            return self.value
        s = f'{self.value3} - ложно, результат = '
        self.value2.verbose = s + self.value2.verbose
        return self.value2


class Error(Exception):
    pass


class LambdaVarsError(Error):
    def __init__(self, message):
        self.message = message


class Var(Operation):
    sign = 'it'

    def calculate(self, args=None):
        if args is None:
            raise LambdaVarsError("Calculating lambda expression with no arguments")
        return args


class Map(Operation):
    sign = 'map'

    def calculate(self, args=None):
        values = self.ops[1].calculate()[0].ops
        ress1, ress2 = [], []
        for i in range(len(values[0])):
            res1, res2 = self.ops[0].calculate((values[0][i], values[1][i]))
            ress1.append(res1)
            ress2.append(res2)
        result = MultipleVals(*ress1).calculate()
        return result[0], values[1]

    def __str__(self):
        return f'checking ({self.ops[0]} for {self.ops[1]}'


class CountFunction(Operation):
    sign = 'count'

    def calculate(self, args=None):
        pass


class Val(Operation):
    sign = 'val'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.comment is None:
            self.comment = ''

    def calculate(self, args=None):
        if self.verbose is None:
            self.verbose = self.__str__()
        return self

    def simplify(self):
        self.value = round(self.value, 5)
        if int(self.value) == self.value:
            self.value = int(self.value)

    @property
    def answer(self):
        return f'{self.value} {self.comment}'.strip()

    def __str__(self):
        if self.verbose:
            return f'{self.verbose} {self.comment}'.strip()
        return self.answer

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        verbose = f'{self} + {other}'
        if isinstance(other, int):
            return Val(other + self.value, comment=self.comment, verbose=verbose)
        if isinstance(other, MultipleVals):
            return other.__add__(self)
        if self.comment and other.comment:
            if self.comment == other.comment:
                return Val(self.value + other.value, comment=self.comment, verbose=verbose)
            return MultipleVals(value=self, value2=other)
        return Val(self.value + other.value, comment=max(self.comment, other.comment), verbose=verbose)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        verbose = f'{self} - {other}'
        if isinstance(other, int):
            return Val(other - self.value, comment=self.comment)
        if isinstance(other, MultipleVals):
            return other.__sub__(self)
        if self.comment and other.comment:
            if self.comment == other.comment:
                return Val(self.value - other.value, comment=self.comment, verbose=verbose)
            raise SyntaxError("как я тебе один тип урона из другого вычту, додик")
        return Val(self.value - other.value, comment=max(self.comment, other.comment), verbose=verbose)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        verbose = f'{self} * {other}'
        if len(set('+-,') - set(str(other))) < 3:
            verbose = f'{self} * ({other})'
        if isinstance(other, MultipleVals):
            return other.__mul__(self)
        if self.comment and other.comment:
            if self.comment == other.comment:
                return Val(self.value * other.value, comment=self.comment, verbose=verbose)
            raise SyntaxError("я не умею перемножать типы урона, додик")
        return Val(self.value * other.value, comment=max(self.comment, other.comment), verbose=verbose)

    def __truediv__(self, other):
        verbose = f'{self} / {other}'
        if len(set('+-,') - set(str(other))) < 3:
            verbose = f'{self} / ({other})'
        if isinstance(other, MultipleVals):
            return other.__truediv__(self)
        if self.comment and other.comment:
            if self.comment == other.comment:
                return Val(self.value / other.value, comment=self.comment, verbose=verbose)
            raise SyntaxError("я не умею делить типы урона, додик")
        return Val(self.value / other.value, comment=max(self.comment, other.comment), verbose=verbose)

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __bool__(self):
        return bool(self.value)
