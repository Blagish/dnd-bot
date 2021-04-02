from random import randint


class Operation:
    ops = None
    value = None

    def __init__(self, *ops, value=None):
        self.ops = ops
        self.value = value

    def __str__(self):
        str_ = '('
        for i in self.ops:
            str_ += f'{i} {self.value} '
        return str_[:-3]+')'

    def calculate(self):
        pass


class Var(Operation):
    def __str__(self):
        return str(self.ops[0])

    def calculate(self):
        return int(self.ops[0])


class BasicMathOperation(Operation):
    def calculate(self):
        s = self.ops[0].calculate()
        for i in range(1, len(self.ops)):
            next = self.ops[i].calculate()
            if self.value == '+':
                s += next
            if self.value == '-':
                s -= next
            if self.value == '*':
                s *= next
            if self.value == '/':
                s /= next
        return s


class DiceOperation(Operation):
    def calculate(self):
        rolls = self.ops[0].calculate()
        die_size = self.ops[1].calculate()
        s = 0
        for i in range(rolls):
            s += randint(1, die_size)
        return s


class MultipleOperations:
    ops = []

    def __init__(self, *ops):
        self.ops = [*ops]

    def __str__(self):
        s = '('
        for i in self.ops:
            s += f'{i}, '
        return s[:-2]+')'