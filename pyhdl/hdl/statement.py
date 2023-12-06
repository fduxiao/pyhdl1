import typing
from dataclasses import dataclass, field
from .expr import Expr, Var


@dataclass(kw_only=True)
class Statement:
    extra_data: typing.Any = None


@dataclass(init=False)
class BeginBlock(Statement):
    statements: list[Statement]

    def __init__(self, *args):
        self.statements = list(args)

    def add(self, statement: Statement):
        if not isinstance(statement, Statement):
            raise TypeError(f"only Statement is accepted here, not {statement}: {type(statement)}")
        self.statements.append(statement)
        return self


@dataclass
class Assign(Statement):
    target: Var
    e: Expr


@dataclass
class Transfer(Statement):
    target: Var
    e: Expr


@dataclass
class Edge:
    wire: Expr


@dataclass
class PosEdge(Edge):
    pass


@dataclass
class NegEdge(Edge):
    pass


@dataclass
class Always(Statement):
    edges: list[Edge] = field(default_factory=list)
    body: BeginBlock = field(default_factory=BeginBlock)

    def add(self, statement):
        self.body.add(statement)
