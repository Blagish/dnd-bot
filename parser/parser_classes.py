from parser.types import Operation, Val, MultipleVals
from parser.custom_random import rangen


class Addition(Operation):
    """Математическая операция сложения"""
    sign = '+'

    def calculate(self, recalculate=False) -> Val | MultipleVals:
        super().calculate(recalculate)
        return (self.value + self.value2).calculate(recalculate)


class Subtraction(Operation):
    """Математическая операция вычитания."""
    sign = '-'

    def calculate(self, recalculate=False) -> Val | MultipleVals:
        super().calculate(recalculate)
        return (self.value - self.value2).calculate(recalculate)


class Division(Operation):
    """Математическая операция деления."""
    sign = '/'

    def calculate(self, recalculate=False) -> Val | MultipleVals:
        super().calculate(recalculate)
        return (self.value / self.value2).calculate(recalculate)


class Multiplication(Operation):
    """Математическая операция умножения."""
    sign = '*'

    def calculate(self, recalculate=False) -> Val | MultipleVals:
        super().calculate(recalculate)
        return (self.value * self.value2).calculate(recalculate)


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

    def calculate(self, recalculate=False) -> Val | MultipleVals:
        super().calculate(recalculate)
        results = []
        for i in range(self.value.value):
            s_, res_ = self.get_result(self.value2.value)
            results.append((s_, res_, i))
        s, res_str = self.pick_result(results)
        comment = self.value2.comment or self.comment
        verbose = (res_str[:-2] + (self.comment or '')).strip()
        return Val(s, comment=comment, verbose=verbose)

    def pick_result(self, results) -> (int, str):
        s = 0
        res_str = ''
        if self.pick is not None:
            res_str = '\nВыкинуто: '
            for i in results:
                res_str += i[1]
            res_str = res_str.replace(' + ', ', ').replace('*', '')
            res_str += '\n'
            results.sort(key=lambda x: x[0], reverse=True)
            results = results[:self.pick.value]
            results.sort(key=lambda x: x[2])
        if len(results) == 0:
            res_str += '  '  # just for aesthetics
        for i, j, id_ in results:
            s += i
            res_str += j
        return s, res_str

    def get_result(self, die_size) -> (int, str):
        roll = rangen.roll(die_size)
        if self.overwrite_minimum and roll < self.overwrite_value:
            return self.overwrite_value, f'[~~{roll}~~|**{self.overwrite_value}**] + '
        return roll, f'[**{roll}**] + '

    @staticmethod
    def bold_the_result(result, *rolls) -> str:
        s = '|' + '|'.join(map(str, rolls))
        return s.replace(f'|{result}', f'|**{result}**')[1:]


class ExplodingDiceOperation(DiceOperation):
    sign = 'b'

    def get_result(self, die_size) -> (int, str):
        rolls_total = []
        rolls_sum = 0
        times_to_roll = 1
        rollings = 0
        while rollings < times_to_roll:
            rollings += 1
            roll = rangen(die_size)
            rolls_sum += roll
            rolls_total.append(str(roll))
            if roll == die_size and die_size > 1:
                times_to_roll += 1
        return rolls_sum, f'[**{"**+**".join(rolls_total)}**] + '


class AdvantageDiceOperation(DiceOperation):
    """Операция броска куба с преимуществом."""
    sign = 'ad'

    def get_result(self, die_size) -> (int, str):
        rolls = rangen.roll(die_size, times=2)
        roll = max(rolls)
        if self.overwrite_minimum and roll < self.overwrite_value:
            return self.overwrite_value, f'a[~~{rolls[0]}~~|~~{rolls[1]}~~|**{self.overwrite_value}**] + '
        return roll, f'a[{self.bold_the_result(roll, *rolls)}] + '


class DisadvantageDiceOperation(DiceOperation):
    """Операция броска куба с помехой."""
    sign = 'dd'

    def get_result(self, die_size) -> (int, str):
        rolls = rangen.roll(die_size, times=2)
        roll = min(rolls)
        if self.overwrite_minimum and roll < self.overwrite_value:
            s = '|'.join(map(lambda x: f'~~{x}~~', rolls))
            return self.overwrite_value, f'd[{s}|**{self.overwrite_value}**] + '
        return roll, f'd[{self.bold_the_result(roll, *rolls)}] + '


class ElfAdvantageDiceOperation(DiceOperation):
    """Операция броска куба с эльфийским преимуществом (3 куба)."""
    sign = 'ed'

    def get_result(self, die_size) -> (int, str):
        rolls = rangen.roll(die_size, times=3)
        roll = max(rolls)
        if self.overwrite_minimum and roll < self.overwrite_value:
            s = '|'.join(map(lambda x: f'~~{x}~~', rolls))
            return self.overwrite_value, f'e[{s}|**{self.overwrite_value}**] + '
        return roll, f'e[{self.bold_the_result(roll, *rolls)}] + '


class QuadAdvantageDiceOperation(DiceOperation):
    """Операция броска куба с четверным преимуществом (4 куба)."""
    sign = 'kd'

    def get_result(self, die_size) -> (int, str):
        rolls = rangen.roll(die_size, times=4)
        roll = max(rolls)
        if self.overwrite_minimum and roll < self.overwrite_value:
            s = '|'.join(map(lambda x: f'~~{x}~~', rolls))
            return self.overwrite_value, f'k[{s}|**{self.overwrite_value}**] + '
        return roll, f'k[{self.bold_the_result(roll, *rolls)}] + '


class FunctionOfMultipleVars(Operation):
    """Базовый класс операции применения функции к нескольким числам."""
    sign = 'func'
    func = None

    def calculate(self, recalculate=False) -> MultipleVals:
        super().calculate(recalculate)
        self.value.calculate(recalculate)
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

    def calculate(self, recalculate=False) -> Val:
        super().calculate(recalculate)
        return Val(self.value > self.value2).calculate(recalculate)


class Lesser(Operation):
    """Математическая функция сравнения двух чисел. Возвращает 0 или 1."""
    sign = '<'

    def calculate(self, recalculate=False) -> Val:
        super().calculate(recalculate)
        return Val(self.value < self.value2).calculate(recalculate)


class GreaterEquals(Operation):
    """Математическая функция сравнения двух чисел. Возвращает 0 или 1."""
    sign = '>='

    def calculate(self, recalculate=False) -> Val:
        super().calculate(recalculate)
        return Val(self.value >= self.value2).calculate(recalculate)


class LesserEquals(Operation):
    """Математическая функция сравнения двух чисел. Возвращает 0 или 1."""
    sign = '<='

    def calculate(self, recalculate=False) -> Val:
        super().calculate(recalculate)
        return Val(self.value <= self.value2).calculate(recalculate)


class Equals(Operation):
    """Математическая функция сравнения двух чисел. Возвращает 0 или 1."""
    sign = '='

    def calculate(self, recalculate=False) -> Val:
        super().calculate(recalculate)
        return Val(self.value == self.value2).calculate(recalculate)


class NotEquals(Operation):
    """Математическая функция сравнения двух чисел. Возвращает 0 или 1."""
    sign = '≠'

    def calculate(self, recalculate=False) -> Val:
        super().calculate(recalculate)
        return Val(self.value != self.value2).calculate(recalculate)


class IfOperation(Operation):
    sign = ('?', ':')
    value3 = None

    def __init__(self, *args, value3=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.value3 = value3

    def calculate(self, recalculate=False) -> Val | MultipleVals:
        # value3 - выражение для проверки
        super().calculate(recalculate)
        if self.value3.calculate(recalculate):
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

    def __init__(self):
        super().__init__(None)

    def calculate(self, recalculate=False) -> Val | MultipleVals:
        return self.var


class Map(Operation):
    sign = 'map'

    def calculate(self, recalculate=False) -> Val | MultipleVals:
        result = MultipleVals(None, show_value2=True)
        if not isinstance(self.value2, MultipleVals):
            return Val(0)

        for i in self.value2.value:
            val = i.calculate(recalculate=True)
            self.value.var = val
            calc = self.value.calculate(recalculate=True)
            calc.value2 = val
            result.append(calc)

        return result


class CountFunction(Operation):
    sign = 'count'

    def calculate(self, recalculate=False) -> Val:
        pass
