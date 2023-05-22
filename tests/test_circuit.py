import unittest
from pyhdl import AndGate, Xtal, Circuit, Wire


class TestSimpleLogic(unittest.TestCase):
    def test_xtal(self):
        class SomeCircuit(Circuit):
            def __init__(self):
                super().__init__()
                self.wire_a = Wire()
                self.wire_b = Wire()
                self.wire_c = Wire()
                self.xtal1 = self.add_circuit(Xtal(period=2, output=self.wire_a))
                self.xtal2 = self.add_circuit(Xtal(period=4, output=self.wire_b))
                self.and_gate = self.add_circuit(AndGate(self.wire_a, self.wire_b, self.wire_c))

        circuit = SomeCircuit()
        output = []
        for i in range(20):
            circuit.step()
            output.append(circuit.wire_c.value)
        print(output)


if __name__ == '__main__':
    unittest.main()
