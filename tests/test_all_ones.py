import numpy as np

from modules.utils import all_ones


def test_all_ones1():
    assert all_ones(np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])) is True


def test_all_ones2():
    assert all_ones(np.array([1, 1, 1, 1, 1, 0, 1, 1, 1, 1])) is False
