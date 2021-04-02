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
    def calculate(self):
        return int(self.ops[0])

    def __str__(self):
        return str(self.ops[0])

    def __gt__(self, other):
        return self.ops[0] > other.ops[0]


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


class CommaOperation(Operation):
    def __init__(self, *ops, value=','):
        super().__init__(*ops, value=value)
        self.ops = []
        for op in ops:
            if op.value == ',':
                self.ops += list(op.ops)
            else:
                self.ops.append(op)
        self.ops = tuple(self.ops)
        self.value = value

    def calculate(self):
        return tuple(map(lambda x: x.calculate(), self.ops))


class MinMaxOperation(Operation):
    def calculate(self):
        if self.value == 'max':
            return max(self.ops[0].calculate())
        elif self.value == 'min':
            return min(self.ops[0].calculate())

    def __str__(self):
        str_ = f'{self.value}('
        for i in self.ops:
            str_ += f'{i}, '
        return str_[:-2]+')'

