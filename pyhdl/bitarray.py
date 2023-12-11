import math


class BitArray:

    @staticmethod
    def get_min_bits(value):
        if value == 0:
            min_bits = 1
        elif value == 1:
            min_bits = 1
        else:
            min_bits = math.ceil(math.log2(value))
        return min_bits

    def __init__(self, value=0, n_bits=None, signed=False):
        self.signed = signed
        min_bits = self.get_min_bits(value)
        if n_bits is None:
            n_bits = min_bits
        if min_bits > n_bits:
            raise ValueError(n_bits)
        self.n_bits = n_bits
        self.value = value

    def set_value(self, value):
        self.value = value

    def get_bit(self, index: int):
        if index >= self.n_bits:
            raise IndexError(index)
        mask = 1 << index
        value = self.value & mask
        if value > 0:
            return 1
        else:
            return 0

    def set_bit(self, key, value):
        if key >= self.n_bits:
            raise IndexError(key)
        mask = 1 << key
        value = value << key
        self.value &= ~mask
        value &= mask
        self.value |= value

    def __getitem__(self, item):
        if item.start is None and item.step is None and item.stop is None:
            return BitArray(self.value)

    def __setitem__(self, key, value):
        if isinstance(value, BitArray):
            value = value.value
        if isinstance(key, slice):
            if key.start is None and key.step is None and key.stop is None:
                self.value = value

    def __eq__(self, other):
        if isinstance(other, BitArray):
            other = other.value
        return other == self.value

    def __add__(self, other):
        if isinstance(other, BitArray):
            other = other.value
        return BitArray(self.value + other)
