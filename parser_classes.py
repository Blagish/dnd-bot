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


class Val(Operation):
    def calculate(self, args=None):
        if args is None:
            args = []
        return int(self.ops[0])

    def __str__(self):
        return str(self.ops[0])

    def __gt__(self, other):
        return self.ops[0] > other.ops[0]


#class BasicMathOperation(Operation):
#    def calculate(self):
#        s = self.ops[0].calculate(args)
#        for i in range(1, len(self.ops)):
#           next = self.ops[i].calculate(args)
#            if self.value == '+':
#                s += next
#            if self.value == '-':
#                s -= next
#            if self.value == '*':
#                s *= next
#            if self.value == '/':
#                s /= next
#        return s


class Addition(Operation):
    value = '+'
    
    def calculate(self, args=None):
        res = self.ops[0].calculate(args)
        for i in range(1, len(self.ops)):
            res += self.ops[i].calculate(args)
        return res


class Subtraction(Operation):
    value = '-'
    
    def calculate(self, args=None):
        res = self.ops[0].calculate(args)
        for i in range(1, len(self.ops)):
            res -= self.ops[i].calculate(args)
        return res


class Division(Operation):
    value = '/'
    
    def calculate(self, args=None):
        res = self.ops[0].calculate(args)
        for i in range(1, len(self.ops)):
            res /= self.ops[i].calculate(args)
        return res


class Multiplication(Operation):
    value = '*'
    
    def calculate(self, args=None):
        res = self.ops[0].calculate(args)
        for i in range(1, len(self.ops)):
            res *= self.ops[i].calculate(args)
        return res


class DiceOperation(Operation):
    value = 'd'

    def calculate(self, args=None):
        rolls = self.ops[0].calculate(args)
        die_size = self.ops[1].calculate(args)
        s = 0
        for i in range(rolls):
            s += randint(1, die_size)
        return s


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
        return tuple(map(lambda x: x.calculate(args), self.ops))


class MinOperation(Operation):
    value = 'min'

    def calculate(self, args=None):
        return min(self.ops[0].calculate(args))

    def __str__(self):
        str_ = f'{self.value}('
        for i in self.ops:
            str_ += f'{i}, '
        return str_[:-2]+')'


class MaxOperation(Operation):
    value = 'max'

    def calculate(self, args=None):
        return max(self.ops[0].calculate(args))

    def __str__(self):
        str_ = f'{self.value}('
        for i in self.ops:
            str_ += f'{i}, '
        return str_[:-2] + ')'


class Greater(Operation):
    value = '>'

    def calculate(self, args=None):
        return int(self.ops[0].calculate(args) > self.ops[1].calculate(args))


class Lesser(Operation):
    value = '<'

    def calculate(self, args=None):
        return int(self.ops[0].calculate(args) < self.ops[1].calculate(args))


class GreaterEquals(Operation):
    value = '>='

    def calculate(self, args=None):
        return int(self.ops[0].calculate(args) >= self.ops[1].calculate(args))


class LesserEquals(Operation):
    value = '<='

    def calculate(self, args=None):
        return int(self.ops[0].calculate(args) < self.ops[1].calculate(args))


class Equals(Operation):
    value = '=='

    def calculate(self, args=None):
        return int(self.ops[0].calculate(args) == self.ops[1].calculate(args))


class NotEquals(Operation):
    value = '!='

    def calculate(self, args=None):
        return int(self.ops[0].calculate(args) != self.ops[1].calculate(args))


class IfOperation(Operation):
    value = ('?', ':')

    def calculate(self, args=None):
        condition = self.ops[0].calculate(args)
        if condition:
            return self.ops[1].calculate(args)
        return self.ops[2].calculate(args)

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
        return tuple([self.ops[0].calculate(i) for i in self.ops[1].calculate()])

    def __str__(self):
        return f'({self.ops[0]} mapped to {self.ops[1]}'


class Sum(Operation):
    value = 'sum'

    def calculate(self, args=None):
        return sum(self.ops[0].calculate(args))

    def __str__(self):
        return f'(sum of {self.ops[0]})'


class Tuple(Operation):
    value = ''

    def calculate(self, args=None):
        return self.ops[0].calculate(args),

    def __str__(self):
        return '{' + f'{self.ops[0]}' + '}'
