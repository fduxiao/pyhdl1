"""
模拟引线状态
"""
from dataclasses import dataclass
from typing import Any, Optional
import weakref
from pyhdl import hdl


def get_name(x):
    if isinstance(x, str):
        return x

    name = getattr(x, "name", None)
    if name is None:
        raise TypeError(f"unable to find name of {x}: {type(x)}")
    return name


@dataclass
class Var(hdl.Var):
    target: str = ""
    _wire: weakref.ref["Wire"] = None

    @property
    def wire(self) -> Optional["Wire"]:
        if self._wire is None:
            return None
        return self._wire()

    @wire.setter
    def wire(self, x):
        self._wire = weakref.ref(x)

    def __call__(self, another):
        self.target = get_name(another)
        w = self.wire
        if w is None:
            return None
        return w.module

    def pos(self):
        return hdl.PosEdge(self)

    def neg(self):
        return hdl.NegEdge(self)

    def assign(self, expr: hdl.Expr) -> hdl.Assign:
        return hdl.Assign(self, expr)

    def transfer_from(self, expr: hdl.Expr) -> hdl.Transfer:
        return hdl.Transfer(self, expr)


@dataclass
class Wire(hdl.Wire):
    _var: Var = None
    _module: Any = None

    def __post_init__(self):
        self._var = Var(self.name)
        self._var.wire = self

    def var(self):
        if self._var.name is None:
            self._var.name = self.name
        return self._var

    @property
    def module(self):
        if self._module is None:
            return None
        return self._module()

    @module.setter
    def module(self, x):
        self._module = weakref.ref(x)


def wire(n_bits=1, is_input=False, is_output=False, reg=False):
    return Wire(n_bits, is_input, is_output, reg)


def input_wire(n_bits=1):
    return wire(n_bits, is_input=True)


def output_wire(n_bits=1):
    return wire(n_bits, is_output=True)
