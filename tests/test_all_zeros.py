import numpy as np

from modules.utils import all_zeros


def test_all_zeros1():
    assert all_zeros(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])) is True


def test_all_zeros2():
    assert all_zeros(np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0])) is False
