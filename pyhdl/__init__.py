"""
使用python制作的基于verilog的硬件描述语言，将由虚拟电路、代码生成器、DSL、验证器等模块组成
"""
from .frontend import *
from .value import *
from .circuit import compile_to_circuit


del circuit
