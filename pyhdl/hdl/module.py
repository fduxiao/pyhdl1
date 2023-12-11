"""
电路的基本组成单元是module，每个module定义输入输出以及内部结构
每个module都是callable的，在触发__call__行为的时候生成一个circuit
得到真实电路，然后进行仿真
"""
from dataclasses import dataclass, field
from .statement import BeginBlock, Assign
from .expr import Var


@dataclass
class Wire:
    """
    描述一个wire所需的内容
    """
    n_bits: int = 1
    signed: bool = False
    is_input: bool = False
    is_output: bool = False
    reg: bool = False
    name: str = None


@dataclass
class Instantiate:
    module: "Module"
    args: dict[str, str]


@dataclass
class Edge:
    wire: Var


@dataclass
class PosEdge(Edge):
    pass


@dataclass
class NegEdge(Edge):
    pass


@dataclass
class Always:
    edges: list[Edge] = field(default_factory=list)
    body: BeginBlock = field(default_factory=BeginBlock)

    def add(self, statement):
        self.body.add(statement)


@dataclass
class Module:
    """
    描述模块
    """
    name: str = ""
    params: list[Wire] = field(default_factory=list)
    wires: list[Wire] = field(default_factory=list)
    instances: dict[str, Instantiate] = field(default_factory=dict)
    init: BeginBlock = field(default_factory=BeginBlock)
    combs: list[Assign] = field(default_factory=list)
    always: list[Always] = field(default_factory=list)
