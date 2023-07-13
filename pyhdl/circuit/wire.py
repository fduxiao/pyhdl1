"""
模拟引线状态
"""
from pyhdl.bitarray import BitArray


class Wire:
    """
    模拟引线状态
    """

    def __init__(self, n_bits: int = 1):
        self._value = BitArray(n_bits=n_bits)
        self.change_event: list[callable] = []
        """
        当导线的值发生变化的时候触发此函数，由于always块只有or操作，所以
        使用变更函数即可
        """

    def on_change(self):
        for event in self.change_event:
            event()

    @property
    def n_bits(self):
        return self._value.n_bits

    @property
    def value(self):
        """
        返回当前的导线状态

        :return:
        """
        return self._value.value

    @value.setter
    def value(self, value):
        if value != self.value:
            self._value.value = value
            self.on_change()

    def add_change_event(self, event):
        """
        增加状态变化之后的事件

        :param event:
        :return:
        """
        self.change_event.append(event)
        return self


class Reg(Wire):
    """
    由于按此python建模方式，wire和reg之间没有差别，因此我们直接使用
    Wire类即可，此处为了保证语义，单独创建一个空类
    """
