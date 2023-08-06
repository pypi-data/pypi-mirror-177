from __future__ import annotations
from typing import Tuple
from .customint import customint


# noinspection PyPep8Naming
class int64(customint):
    """Represents an int64."""
    _num_bits = 64
    _minvalue = int((2**_num_bits // -2))
    _maxvalue = int((2**_num_bits // 2) - 1)

    def __init__(self, value):
        super(int64, self).__init__(
            value=value,
            num_bits=self._num_bits,
            minvalue=self._minvalue,
            maxvalue=self._maxvalue
        )

    def __add__(self, other) -> int64:
        if isinstance(other, customint):
            return int64(self.value + other.value)
        if isinstance(other, int):
            return int64(self.value + other)
        raise NotImplementedError(f'Addition between {type(self)} and {type(other)} not supported.')

    def __iadd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __radd__(self, other) -> int64:
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __sub__(self, other) -> int64:
        if isinstance(other, customint):
            return int64(self.value - other.value)
        if isinstance(other, int):
            return int64(self.value - other)
        raise NotImplementedError(f'Subtraction between {type(self)} and {type(other)} not supported.')

    def __isub__(self, other):
        if other == 0:
            return self
        else:
            return self.__sub__(other)

    def __rsub__(self, other) -> int64:
        if other == 0:
            return self
        else:
            return self.__sub__(other)

    def __mul__(self, other) -> int64:
        if isinstance(other, customint):
            return int64(self.value * other.value)
        if isinstance(other, int):
            return int64(self.value * other)
        raise NotImplementedError(f'Multiplication between {type(self)} and {type(other)} not supported.')

    def __imul__(self, other) -> int64:
        if other == 0:
            return int64(0)
        else:
            return self.__mul__(other)

    def __rmul__(self, other) -> int64:
        if other == 0:
            return int64(0)
        else:
            return self.__mul__(other)

    def __divmod__(self, other) -> Tuple[int64, int64]:
        if isinstance(other, customint):
            if other.value == 0:
                raise ZeroDivisionError('Cannot divide by zero.')
            new_quot, new_mod = self.value // other.value, self.value % other.value
            return int64(new_quot), int64(new_mod)
        if isinstance(other, int):
            if other == 0:
                raise ZeroDivisionError('Cannot divide by zero.')
            new_quot, new_mod = self.value // other, self.value % other
            return int64(new_quot), int64(new_mod)
        raise NotImplementedError(f'Division between {type(self)} and {type(other)} not supported.')

    def __rdivmod__(self, other) -> Tuple[int64, int64]:
        return self.__divmod__(other)

    def __floordiv__(self, other) -> int64:
        if isinstance(other, customint):
            if other.value == 0:
                raise ZeroDivisionError('Cannot divide by zero.')
            return int64(self.value // other.value)
        if isinstance(other, int):
            if other == 0:
                raise ZeroDivisionError('Cannot divide by zero.')
            return int64(self.value // other)
        raise NotImplementedError(f'Division between {type(self)} and {type(other)} not supported.')

    def __rfloordiv__(self, other):
        return self.__floordiv__(other)

    def __pow__(self, power, modulo=None) -> int64:
        if isinstance(power, int):
            return int64(self.value ** power)
        raise NotImplementedError(f'Exponentiation between {type(self)} and {type(power)} not supported.')

    def __str__(self) -> str:
        return str(self.value)
