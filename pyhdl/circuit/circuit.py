from typing import Optional
import weakref

from pyhdl import hdl, Value
from .wire import BaseWire


class Wire(BaseWire):
    def __init__(self, n_bit: int = 1, signed=False, name=None):
        super().__init__(n_bit, signed)
        self._parent: weakref.ref["Circuit"] = None
        self.name = name

    @property
    def parent(self) -> Optional["Circuit"]:
        if self._parent is None:
            return None
        return self._parent()

    @parent.setter
    def parent(self, x: "Circuit"):
        self._parent = weakref.ref(x)

    def relative_to(self, circuit: "Circuit"):
        parent = self.parent
        path = [self.name]
        while parent is not None:
            if parent is circuit:
                return path
            path = [parent.name] + path
        return None


class Circuit:
    def __init__(self, name=None):
        self._parent = None
        self.name = name
        self.wire_pool: dict[str, Wire] = dict()
        self.sub_circuits: dict[str, Circuit] = dict()

    @property
    def parent(self) -> Optional["Circuit"]:
        if self._parent is None:
            return None
        return self._parent()

    @parent.setter
    def parent(self, x):
        self._parent = weakref.ref(x)

    def add_wire(self, name, wire):
        wire.name = name
        self.wire_pool[name] = wire

    def find_wire(self, *path):
        if len(path) == 0:
            raise ValueError("empty path")
        if len(path) == 1:
            return self.wire_pool[path[0]]
        return self.sub_circuits[path[0]].find_wire(path[1:])

    def execute(self, statement: hdl.Statement) -> "Circuit":
        if isinstance(statement, hdl.BeginBlock):
            for s in statement.statements:
                self.execute(s)
        if isinstance(statement, hdl.Assign):
            target = statement.target
            expr = statement.expr
            if isinstance(target, hdl.Var):
                wire = self.find_wire(target.name)
                item = slice(None, None, None)
            elif isinstance(target, hdl.Item):
                item = target.item
                target = target.expr
                if not isinstance(target, hdl.Var):
                    raise ValueError("we can only assign to wires")
                wire = self.find_wire(target.name)
            else:
                raise TypeError("we can only assign to wires")
            wire.set_value(self.eval(expr), item)
        return self

    def eval(self, expr: hdl.Expr) -> Value:
        if isinstance(expr, int):
            return Value(expr)

        if isinstance(expr, hdl.Constant):
            return expr.value

        if isinstance(expr, hdl.Var):
            return self.wire_pool[expr.name].value

        if isinstance(expr, hdl.Eq):
            v1 = self.eval(expr.e1)
            v2 = self.eval(expr.e2)
            return Value(1 if v1 == v2 else 0)

        if isinstance(expr, hdl.Add):
            v1 = self.eval(expr.e1)
            v2 = self.eval(expr.e2)
            return v1 + v2
        raise NotImplementedError(f"not implemented: {expr}")
