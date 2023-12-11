"""
封装各种表达式以及基础运算
"""

from dataclasses import dataclass
from pyhdl.bitarray import BitArray


class Expr:
    """
    表达式基类
    """
    def __add__(self, other):
        if isinstance(other, int):
            other = Constant(other)
        return Add(self, other)

    def __sub__(self, other):
        if isinstance(other, int):
            other = Constant(other)
        return Minus(self, other)

    def __and__(self, other):
        if isinstance(other, int):
            other = Constant(other)
        return And(self, other)

    def __getitem__(self, item):
        return Item(self, item)

    def eq(self, other):
        if isinstance(other, int):
            other = Constant(other)
        return Eq(self, other)

    def free_variables(self) -> list["Var"]:
        return []


@dataclass
class Constant(Expr):
    value: int | BitArray

    def __post_init__(self):
        if not isinstance(self.value, BitArray):
            self.value = BitArray(self.value)

    @property
    def n_bits(self):
        return self.value.n_bits

    @n_bits.setter
    def n_bits(self, n_bits):
        self.value.set_n_bits(n_bits)


@dataclass
class Var(Expr):
    name: str

    def free_variables(self) -> list:
        return [self]


@dataclass
class Add(Expr):
    e1: Expr
    e2: Expr

    def free_variables(self) -> list:
        return self.e1.free_variables() + self.e2.free_variables()


@dataclass
class Minus(Expr):
    e1: Expr
    e2: Expr

    def free_variables(self) -> list:
        return self.e1.free_variables() + self.e2.free_variables()


@dataclass
class And(Expr):
    e1: Expr
    e2: Expr

    def free_variables(self) -> list:
        return self.e1.free_variables() + self.e2.free_variables()


@dataclass
class Item(Expr):
    expr: Expr
    item: int | slice

    def free_variables(self) -> list:
        return self.expr.free_variables()


@dataclass
class Eq(Expr):
    e1: Expr
    e2: Expr

    def free_variables(self) -> list:
        return self.e1.free_variables() + self.e2.free_variables()
