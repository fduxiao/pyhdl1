import typing
from dataclasses import dataclass
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
    target: Expr
    expr: Expr


@dataclass
class Transfer(Statement):
    target: Expr
    expr: Expr
