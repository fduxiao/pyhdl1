import math


class BitArray:
    def __init__(self, value=0, n_bits=None):
        if value == 0:
            min_bits = 1
        else:
            min_bits = math.ceil(math.log2(value))
        if n_bits is None:
            n_bits = min_bits
        if min_bits > n_bits:
            raise ValueError(n_bits)
        self.n_bits = n_bits
        self.value = value

    def __getitem__(self, index: int):
        if index >= self.n_bits:
            raise IndexError(index)
        mask = 1 << index
        value = self.value & mask
        if value > 0:
            return 1
        else:
            return 0

    def __setitem__(self, key, value):
        if key >= self.n_bits:
            raise IndexError(key)
        mask = 1 << key
        value = value << key
        self.value &= ~mask
        value &= mask
        self.value |= value
