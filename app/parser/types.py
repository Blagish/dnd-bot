class Operation:
    """Базовый класс операции между двумя величинами"""

    verbose = None
    sign = None
    value = None
    value_prev = None
    value2 = None
    value2_prev = None
    var = None
    comment = None

    def __init__(self, value, value2=None, **kwargs):
        self.value = value
        self.value2 = value2
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])

    def __str__(self):
        return f"{self.value}{self.sign}{self.value2}"

    def calculate(self, recalculate=False):
        if recalculate:
            self.restore_values()

        self.value.var = self.var
        if self.value2:
            self.value2.var = self.var

        if (
            self.value
            and not isinstance(self.value, Val)
            and not isinstance(self.value, MultipleVals)
        ):
            self.value_prev = self.value
            self.value = self.value.calculate(recalculate)
        if (
            self.value2
            and not isinstance(self.value2, Val)
            and not isinstance(self.value2, MultipleVals)
        ):
            self.value2_prev = self.value2
            self.value2 = self.value2.calculate(recalculate)

    def restore_values(self):
        self.value = self.value_prev or self.value
        self.value2 = self.value2_prev or self.value2


class Val(Operation):
    sign = "val"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self.value, bool):
            self.value = int(self.value)
        if self.comment is None:
            self.comment = ""

    def calculate(self, recalculate=False):
        if self.verbose is None:
            self.verbose = self.__str__()
        return self

    def simplify(self):
        self.value = round(self.value, 5)
        if int(self.value) == self.value:
            self.value = int(self.value)

    @property
    def answer(self):
        return f"{self.value} {self.comment}".strip()

    def __str__(self):
        if self.verbose:
            return f"{self.verbose} {self.comment}".strip()
        return self.answer

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        verbose = f"{self} + {other}"
        if isinstance(other, int):
            return Val(other + self.value, comment=self.comment, verbose=verbose)
        if isinstance(other, MultipleVals):
            return other.__add__(self)
        if self.comment and other.comment:
            if self.comment == other.comment:
                return Val(
                    self.value + other.value, comment=self.comment, verbose=verbose
                )
            return MultipleVals(value=self, value2=other)
        return Val(
            self.value + other.value,
            comment=max(self.comment, other.comment),
            verbose=verbose,
        )

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        verbose = f"{self} - {other}"
        if isinstance(other, int):
            return Val(other - self.value, comment=self.comment, verbose=verbose)
        if isinstance(other, MultipleVals):
            return other.__sub__(self)
        if self.comment and other.comment:
            if self.comment == other.comment:
                return Val(
                    self.value - other.value, comment=self.comment, verbose=verbose
                )
            raise SyntaxError("как я тебе один тип урона из другого вычту, додик")
        return Val(
            self.value - other.value,
            comment=max(self.comment, other.comment),
            verbose=verbose,
        )

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        verbose = f"{self} * {other}"
        if len(set("+-,") - set(str(other))) < 3:
            verbose = f"{self} * ({other})"
        if isinstance(other, MultipleVals):
            return other.__mul__(self)
        if self.comment and other.comment:
            if self.comment == other.comment:
                return Val(
                    self.value * other.value, comment=self.comment, verbose=verbose
                )
            raise SyntaxError("я не умею перемножать типы урона, додик")
        return Val(
            self.value * other.value,
            comment=max(self.comment, other.comment),
            verbose=verbose,
        )

    def __truediv__(self, other):
        verbose = f"{self} / {other}"
        if len(set("+-,") - set(str(other))) < 3:
            verbose = f"{self} / ({other})"
        if isinstance(other, MultipleVals):
            return other.__truediv__(self)
        if self.comment and other.comment:
            if self.comment == other.comment:
                return Val(
                    self.value / other.value, comment=self.comment, verbose=verbose
                )
            raise SyntaxError("я не умею делить типы урона, додик")
        return Val(
            self.value / other.value,
            comment=max(self.comment, other.comment),
            verbose=verbose,
        )

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


class MultipleVals(Operation):
    """Несколько чисел, разделяются запятой и выводятся в скобках."""

    sign = ","
    types = None
    value: list[Val] | Val

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        value = []
        if self.value:
            value.append(self.value)
        self.value = value
        if self.value2:
            if isinstance(self.value2, MultipleVals):
                self.value += self.value2.value
                self.value2 = None
            else:
                self.value.append(self.value2)
        self.types = {}
        self.short_verbose = kwargs.get("short_verbose", False)
        self.show_value2 = kwargs.get("show_value2", False)

    def simplify(self):
        pass

    @property
    def answer(self):
        return f"{self.sign} ".join(map(lambda x: x.answer, self.value))

    def calculate(self, recalculate=False):
        vals = []
        verboses = []
        for i in self.value:
            val = i.calculate(recalculate)
            if self.short_verbose:
                verboses.append(val.answer)
            elif self.show_value2:
                verboses.append(val.value2.verbose)
            else:
                verboses.append(val.verbose)
            vals.append(val)
            self.value = vals
        self.verbose = f"{self.sign} ".join(verboses)
        return self

    def append(self, other):
        if isinstance(other, MultipleVals):
            new_mult_vals = MultipleVals()
            new_mult_vals.value = self.value
            new_mult_vals.types = self.types
            for val in other.value:
                new_mult_vals.append(val)
            return new_mult_vals
        elif isinstance(other, Val):
            self.value.append(other)
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
            if index := self.types.get(other.comment) is None:
                self.value.append(other)
                if other.comment:
                    self.types[other.comment] = len(self.value) - 1
            else:
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
                self.types[other.comment] = len(self.value) - 1
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
