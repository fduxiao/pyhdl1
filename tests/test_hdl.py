from unittest import TestCase
import pyhdl.hdl as hdl
from pyhdl import *
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

                with self.always(self.clk.pos()):
                    self.add(self.counter.assign(self.counter + 1))

        counter = Counter(15)

        def counter_test():
            yield counter.clk.assign(1)
