
import ast
from dataclasses import dataclass, field
import inspect

import pyhdl.hdl as hdl
from .wire import Wire


def get_var_name(offset=1, base=1) -> str:
    depth = offset + base
    current_frame = inspect.currentframe()
    caller = inspect.getouterframes(current_frame)
    caller = caller[depth]
    context = caller.code_context[0]
    parsed = ast.parse(context.strip())
    assign = parsed.body[0]
    if not isinstance(assign, ast.Assign):
        raise TypeError("expect assignment statement")
    target = assign.targets[-1]
    if isinstance(target, ast.Attribute):
        return target.attr
    if isinstance(target, ast.Name):
        return target.id
    raise TypeError("unknown assignment")


@dataclass
class Always(hdl.Always):
    extra_data: list = field(default_factory=list)

    def __enter__(self):
        self.extra_data.append(self.body)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.extra_data.pop()

    def transfer(self, target, expr):
        self.body.statements.append(hdl.Transfer(target, expr))
        return self


class CombHelper:
    def __init__(self, combs: list[hdl.Assign]):
        self.combs = combs

    def add(self, assign: hdl.Assign):
        self.combs.append(assign)
        return self

    def __iadd__(self, other):
        self.add(other)
        return self


class Module:

    def __init__(self):
        self.ast = hdl.Module(type(self).__name__)
        self.block_stack = [self.ast.init]

    @property
    def combs(self):
        return CombHelper(self.ast.combs)

    @combs.setter
    def combs(self, value: CombHelper):
        self.ast.combs = value.combs

    @staticmethod
    def const(value):
        return hdl.Constant(value)

    def param(self, n_bits=1, signed=False, is_input=False, is_output=False, reg=False, name=None, init=None):
        if name is None:
            name = get_var_name()
        wire = Wire(n_bits, signed, is_input, is_output, reg, name)
        wire.module = self
        self.ast.params.append(wire)
        var = wire.var()
        if init is not None:
            self.add(var.assign(init))
        return var

    def input(self, n_bits=1, signed=False, name=None, reg=False, init=None):
        if name is None:
            name = get_var_name()
        return self.param(n_bits, signed, True, False, reg, name, init)

    def output(self, signed=False, n_bits=1, name=None, reg=False, init=None):
        if name is None:
            name = get_var_name()
        return self.param(n_bits, signed, False, True, reg, name, init)

    def wire(self, n_bits=1, signed=False, reg=False, name=None, init=None):
        if name is None:
            name = get_var_name()
        wire = Wire(n_bits, signed, reg=reg, name=name)
        wire.module = self
        self.ast.wires.append(wire)
        var = wire.var()
        if init is not None:
            self.add(var.assign(init))
        return var

    def reg(self, n_bits, signed=False, name=None, init=None):
        if name is None:
            name = get_var_name()
        return self.wire(n_bits, signed, True, name, init)

    def add(self, statement: hdl.Statement):
        self.block_stack[-1].add(statement)

    def always(self, *wires) -> Always:
        always = Always(list(wires))
        self.ast.always.append(always)
        always.extra_data = self.block_stack
        return always
