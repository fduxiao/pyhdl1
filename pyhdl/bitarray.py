"""
This module ensures binary operation.
"""
from dataclasses import dataclass
import math


@dataclass
class Shape:
    """
    This class defines the shape of a bit array
    """
    signed: bool = False
    n_bits: int = 1

    def __post_init__(self):
        # make sure n_bits is positive
        if self.n_bits < 0:
            raise ValueError("n_bits can only be positive.")
        if self.n_bits == 0:
            self.range = None
            self.min = None
            self.max = None
        # then calculate the possible range of this value
        if not self.signed:
            self.min = 0
            self.max = 0b01 << self.n_bits
            self.range = range(self.max)
            self.max -= 1
        else:
            max_value = 0b1 << (self.n_bits - 1)
            self.min = -max_value
            self.max = max_value - 1
            self.range = range(-max_value, max_value)

    def contains(self, item: int) -> bool:
        return item in self

    def __contains__(self, item: int):
        return item in self.range

    def __repr__(self):
        if self.signed:
            return f"signed({self.n_bits})"
        else:
            return f"unsigned({self.n_bits})"

    @classmethod
    def from_range(cls, iterable):
        """
        Calculate the shape from many possibilities.
        """
        minimal = math.inf
        maximal = -math.inf
        for k in iterable:
            minimal = min(minimal, k)
            maximal = max(maximal, k)
        if minimal >= 0:
            # all positive
            if maximal == 0 or maximal == 1:
                return unsigned(1)
            n_bits = math.floor(math.log2(maximal)) + 1
            return unsigned(n_bits)
        if minimal < 0:
            if minimal == -1:
                if maximal == 0 or maximal == 1:
                    return signed(2)
                return signed(math.ceil(math.log2(maximal + 1) + 1))

            n_bits_neg = math.ceil(math.log2(-minimal)) + 1
            if maximal <= 1:
                return signed(n_bits_neg)
            n_bits_pos = math.ceil(math.log2(maximal + 1) + 1)
            return signed(max(n_bits_neg, n_bits_pos))

    @classmethod
    def from_enum(cls, enum):
        return cls.from_range(map(lambda x: x.value, enum))

    @classmethod
    def from_n(cls, *args):
        return cls.from_range(args)


def signed(n: int):
    return Shape(True, n)


def unsigned(n: int):
    return Shape(False, n)


class BitArray:

    def __init__(self, value=0, shape=None):
        if shape is None:
            shape = Shape.from_n(value)
        self.shape: Shape = shape
        self.value = 0
        self.set_value(value)

    @property
    def signed(self):
        return self.shape.signed

    @property
    def n_bits(self):
        return self.shape.n_bits

    def set_value(self, value):
        if value not in self.shape:
            raise ValueError(f"invalid value {value} for shape {self.shape}")
        self.value = value
        return self

    def bin(self):
        value = self.value
        result = ""
        for i in range(self.n_bits):
            result += str(value & 0b1)
            value >>= 1
        return result[::-1]

    def __repr__(self):
        return f"BitArray({self.value}, shape={self.shape})"

    def get_bit(self, index: int):
        if index < 0:
            index += self.n_bits
        if index < 0 or index >= self.n_bits:
            raise IndexError(index)
        mask = 1 << index
        value = self.value & mask
        if value > 0:
            return 1
        else:
            return 0

    def set_bit(self, key, value):
        if key < 0:
            key += self.n_bits
        if key < 0 or key >= self.n_bits:
            raise IndexError(key)
        mask = 1 << key
        value = value << key
        self.value &= ~mask
        value &= mask
        self.value |= value

    def parse_slice(self, item):
        if isinstance(item, int):
            item = slice(item, self.n_bits, self.n_bits)

        if not isinstance(item, slice):
            raise TypeError(f"{type(item)} is not of type slice")

        start = item.start
        step = item.step
        stop = item.stop

        # :, :stop, start:stop, start:stop:step, ::
        # For a slice, if step is missing, then it is 1
        step = step or 1
        if step < 0:
            raise ValueError("negative step is not supported")
        # if start is missing, then it is 0
        start = start or 0
        if start < 0:
            start += self.n_bits
        if start < 0:
            start = 0
        # if stop is missing, then it is the maximal
        stop = stop or self.n_bits
        if stop < 0:
            stop += self.n_bits
        if stop < 0:
            return 0, 0, 0

        if step * (stop - start) < 0:
            return 0, 0, 0

        return start, stop, step

    def __getitem__(self, item):
        start, stop, step = self.parse_slice(item)
        if start is None and step is None and stop is None:
            return BitArray(self.value)  # create a new object

        if start == stop == 0:
            return BitArray(shape=unsigned(0))

        result_value = 0
        value = self.value >> start
        last_bit = 0b1
        mask = 0b1
        # use shifting and masking to calculate result_value
        for i in range(start, stop, step):
            if i >= self.n_bits:
                break
            result_value |= (value & last_bit) * mask
            mask <<= 1
            value >>= step
        return BitArray(result_value)  # always unsigned

    def rev(self):
        value = self.value
        result = 0
        for i in range(self.n_bits):
            result <<= 1
            result |= value & 0b1
            value >>= 1
        return BitArray(result)  # always unsigned

    def __setitem__(self, key, value):
        if isinstance(value, BitArray):
            shape = value.shape
            value = value.value
        else:
            shape = Shape.from_n(value)

        start, stop, step = self.parse_slice(key)
        if start == stop == 0:
            return

    def __eq__(self, other):
        if isinstance(other, BitArray):
            other = other.value
        return other == self.value

    def __add__(self, other):
        if isinstance(other, BitArray):
            other = other.value
        return BitArray(self.value + other)
