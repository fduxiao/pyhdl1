"""
电路的基本组成单元是module，每个module定义输入输出以及内部结构
每个module都是callable的，在触发__call__行为的时候生成一个circuit
得到真实电路，然后进行仿真
"""
from dataclasses import dataclass, field
from .statement import Always, BeginBlock


@dataclass
class Wire:
    """
    描述一个wire所需的内容
    """
    n_bits: int = 1
    is_input: bool = False
    is_output: bool = False
    reg: bool = False
    name: str = None


@dataclass
class Instantiate:
    module: "Module"
    args: dict[str, str]


@dataclass
class Module:
    """
    描述模块
    """
    name: str = ""
    params: list[Wire] = field(default_factory=list)
    wires: list[Wire] = field(default_factory=list)
    instances: dict[str, Instantiate] = field(default_factory=dict)
    combs: BeginBlock = field(default_factory=BeginBlock)
    always: list[Always] = field(default_factory=list)
