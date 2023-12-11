"""
模拟引线状态
"""
from pyhdl.bitarray import BitArray


class BaseWire:
    """
    模拟引线状态
    """

    def __init__(self, n_bits: int = 1, signed=False):
        self._value: BitArray = BitArray(n_bits=n_bits, signed=signed)
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
    def value(self) -> BitArray:
        """
        返回当前的导线状态

        :return:
        """
        return self._value

    @value.setter
    def value(self, value: BitArray):
        if value != self.value:
            self._value.set_value(value.value)
            self.on_change()

    def set_value(self, value, item=slice(None, None, None)):
        if isinstance(value, BitArray):
            value = value.value
        if value != self.value[item]:
            self.value[item] = value
            self.on_change()

    def add_change_event(self, event):
        """
        增加状态变化之后的事件

        :param event:
        :return:
        """
        self.change_event.append(event)
        return self

    def make_pos_event(self, event):
        def new_event():
            if self.value.value != 0:
                event()
        return new_event

    def make_neg_event(self, event):
        def new_event():
            if self.value.value == 0:
                event()
        return new_event
