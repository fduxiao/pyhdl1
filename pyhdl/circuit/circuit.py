"""
电路的实现
"""


class AbstractCircuit:
    """
    电路抽象类，用于维护电路状态、变化，记录总资源等，以及允许自定义行为模拟一些特殊电路等

    每个电路模块是一个黑盒，使用功能只能通过外部导线连接来使用。在此python类的实现里，涉及输入
    输出的导线均通过类构造函数传入

    电路可以互相组合形成新的电路，连接通过指定明确的input和output来设置，这里我们约定input
    作为引用传递，进行output的结果被所在类持有内存。

    电路以离散时间为单位进行状态变化，总以1为单位变化时间，程序的核心就是设置时序变化时电路状态
    的变化
    """

    def step(self):
        """
        单步执行
        """

    def step_n(self, n_steps):
        """
        连续执行多步

        :param n_steps: 步数
        :return:
        """
        for _ in range(n_steps):
            self.step()

    def reset(self):
        """
        设置电路的初始化状态

        :return:
        """


class Circuit(AbstractCircuit):
    """
    默认情况下我们只需要负责连接电路即可，计算过程相当于
    每一个电路都执行step
    """
    def __init__(self):
        self.sub_circuits = []

    def add_circuit(self, circuit: AbstractCircuit):
        """
        添加子电路

        :param circuit:
        :return: 输入的circuit，方便链式写法
        """
        self.sub_circuits.append(circuit)
        return circuit

    def step(self):
        # 按顺序计算子电路
        for circuit in self.sub_circuits:
            circuit.step()

    def reset(self):
        """
        默认将所有字电路进行重置
        """
        for circuit in self.sub_circuits:
            circuit.reset()
