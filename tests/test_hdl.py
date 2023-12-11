from unittest import TestCase
import pyhdl.hdl as hdl
from pyhdl import Module, compile_to_circuit
from dataclasses import dataclass
module = dataclass


class TestHDL(TestCase):
    def test_module(self):
        class Counter(Module):

            def __init__(self, limit):
                super().__init__()
                self.limit = limit
                self.clk = self.input()
                self.rst = self.input()
                self.ovf = self.output()
                self.counter = self.reg(16)

                self.add(self.ovf.assign(self.counter.eq(self.limit)))

                with self.always(self.clk.pos()) as clk:
                    clk.add(self.counter.assign(self.counter + 1))

        counter = Counter(15)

        circuit = compile_to_circuit(counter)
        self.assertEqual(circuit.eval(counter.ovf).value, 0)

        circuit.execute(counter.counter.assign(counter.limit))
        self.assertEqual(circuit.eval(counter.ovf).value, 1)

        circuit.execute(counter.counter.assign(4))
        self.assertEqual(circuit.eval(counter.ovf).value, 0)

        circuit.execute(counter.clk.assign(1))  # 5
        circuit.execute(counter.clk.assign(0))
        circuit.execute(counter.clk.assign(1))  # 6
        circuit.execute(counter.clk.assign(0))
        self.assertEqual(circuit.eval(counter.counter).value, 6)

        def counter_test():
            yield counter.clk.assign(1)
            yield counter.clk.assign(0)
