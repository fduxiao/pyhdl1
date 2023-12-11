
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


class Module:

    def __init__(self):
        self.ast = hdl.Module(type(self).__name__)
        self.block_stack = [self.ast.combs]

    def param(self, n_bits=1, is_input=False, is_output=False, reg=False, name=None):
        if name is None:
            name = get_var_name()
        wire = Wire(n_bits, is_input, is_output, reg, name)
        wire.module = self
        self.ast.params.append(wire)
        return wire.var()

    def input(self, n_bits=1, name=None):
        if name is None:
            name = get_var_name()
        return self.param(n_bits, True, False, False, name)

    def output(self, n_bits=1, name=None):
        if name is None:
            name = get_var_name()
        return self.param(n_bits, False, True, False, name)

    def wire(self, n_bits=1, reg=False, name=None):
        if name is None:
            name = get_var_name()
        wire = Wire(n_bits, reg=reg, name=name)
        wire.module = self
        self.ast.wires.append(wire)
        return wire.var()

    def reg(self, n_bits, name=None):
        if name is None:
            name = get_var_name()
        return self.wire(n_bits, True, name)

    def add(self, statement: hdl.Statement):
        self.block_stack[-1].add(statement)

    def always(self, *wires) -> Always:
        always = Always(list(wires))
        self.ast.always.append(always)
        always.extra_data = self.block_stack
        return always
