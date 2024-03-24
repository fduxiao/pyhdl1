from unittest import TestCase
from pyhdl import Shape, signed, unsigned, BitArray


class TestBitArray(TestCase):
    def test_shape(self):
        # test n_bits calculation
        for i in range(256):
            self.assertEqual(Shape.from_n(i), unsigned(len(bin(i)) - 2))
        # with negative values
        for i in range(256):
            self.assertEqual(Shape.from_n(-1, i), signed(len(bin(i)) - 2 + 1))
        # from several values
        self.assertEqual(Shape.from_n(-4), signed(3))
        self.assertTrue(-4 in signed(3))
        self.assertEqual(Shape.from_n(-4, 4), signed(4))
        self.assertEqual(Shape.from_n(-5), signed(4))
        self.assertEqual(Shape.from_n(-5, 4), signed(4))
        self.assertEqual(Shape.from_n(-8), signed(4))
        self.assertEqual(Shape.from_n(-8, 8), signed(5))

        for i in range(256):
            # 0 is meaningless
            i += 1
            shape = unsigned(i)
            self.assertEqual(shape.range.start, 0)
            self.assertEqual(shape.range.stop, 2 ** i)

            shape = signed(i)
            self.assertEqual(shape.range.start, - 2 ** (i - 1))
            self.assertEqual(shape.range.stop, 2 ** (i - 1))

    def test_get_value(self):
        reg = BitArray(0b1011)
        self.assertEqual(reg.n_bits, 4)
        self.assertEqual(reg.signed, False)
        self.assertEqual(reg[0], 1)
        self.assertEqual(reg[1], 1)
        self.assertEqual(reg[2], 0)
        self.assertEqual(reg[3], 1)

        reg = BitArray(-5)  # this should be 0b1011 as an array of length 4
        self.assertEqual(reg.n_bits, 4)
        self.assertEqual(reg.signed, True)
        self.assertEqual(reg[0], 1)
        self.assertEqual(reg[1].bin(), "1")
        self.assertEqual(reg[2], 0)
        self.assertEqual(reg[3], 1)
        self.assertEqual(reg[-5:].bin(), "1011")
        self.assertEqual(reg.rev().bin(), "1101")
        self.assertEqual(reg[2:], 0b10)
