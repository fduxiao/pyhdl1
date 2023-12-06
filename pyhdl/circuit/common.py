"""
常见电路模拟器实现
"""
from .circuit import AbstractCircuit
from .wire import Wire


class AndGate(AbstractCircuit):
    """
    与门电路
    """

    def __init__(self, a: Wire, b: Wire, c: Wire, delay=1):
        super().__init__()
        self.input_a = a
        self.input_b = b
        self.output = c

        # 延时设置
        self.delay = delay
        self.step_counter = 0

    def step(self):
        if self.step_counter == self.delay:
            self.step_counter = 0
            self.output.value = self.input_a.value & self.input_b.value
        else:
            self.step_counter += 1

    def reset_counter(self):
        """
        重置计数器
        """
        self.step_counter = 0


class Xtal(AbstractCircuit):
    """
    模拟晶振行为
    """

    def __init__(self, period=10, duration=1, *, output: Wire):
        super().__init__()
        self.period = period
        self.duration = duration
        self.output = output
        self.step_counter = 0

    def step(self):
        if self.step_counter < self.duration:
            self.output.value = 1
        else:
            self.output.value = 0

        self.step_counter += 1
        if self.step_counter >= self.period:
            self.step_counter = 0

    def reset_counter(self):
        """
        重置晶振计数器
        """
        self.step_counter = 0
