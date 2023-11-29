"""
封装各种表达式以及基础运算
"""

from dataclasses import dataclass


class Expr:
    """
    表达式基类
    """
    def __add__(self, other):
        return Add(self, other)

    def __sub__(self, other):
        return Minus(self, other)

    def __and__(self, other):
        return And(self, other)

    def __getitem__(self, item):
        return Item(self, item)


@dataclass
class Var(Expr):
    name: str


@dataclass
class Add(Expr):
    e1: Expr
    e2: Expr


@dataclass
class Minus(Expr):
    e1: Expr
    e2: Expr


@dataclass
class And(Expr):
    e1: Expr
    e2: Expr


@dataclass
class Item(Expr):
    expr: Expr
    item: int | slice
