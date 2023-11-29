"""
电路的基本组成单元是module，每个module定义输入输出以及内部结构
每个module都是callable的，在触发__call__行为的时候生成一个circuit
得到真实电路，然后进行仿真
"""
from dataclasses import dataclass
from enum import Enum, auto


class WireType(Enum):
    Input = auto()
    Output = auto()


@dataclass
class Wire:
    """
    描述一个wire所需的内容
    """
    name: str
    n_bits: int
    type: WireType
    reg: False



@dataclass
class Instantiate:
    module: "Module"
    args: list[str]


@dataclass
class Module:
    """
    描述模块
    """
    name: str
    wires: list[Wire]
    instances: dict[str, Instantiate]
