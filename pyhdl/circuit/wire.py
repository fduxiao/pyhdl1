"""
模拟引线状态
"""


class Wire:
    """
    模拟引线状态
    """

    def __init__(self, value=0):
        self._value = value
        self.change_event: list[callable] = []
        """
        当导线的值发生变化的时候触发此函数，由于always块只有or操作，所以
        使用变更函数即可
        """

    @property
    def value(self):
        """
        返回当前的导线状态

        :return:
        """
        return self._value

    @value.setter
    def value(self, value):
        if value < self._value:
            for event in self.change_event:
                event()
        if self._value < value:
            for event in self.change_event:
                event()
        self._value = value

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
