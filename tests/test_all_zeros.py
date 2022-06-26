import numpy as np

from modules.utils import all_zeros
from modules.utils import all_zeros2


def test_all_zeros1(benchmark):
    benchmark(all_zeros, np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))


def test_all_zeros2(benchmark):
    benchmark(all_zeros2, np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))


# def test_all_zeros2():
#     assert all_zeros(np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0])) is False
