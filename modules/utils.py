from typing import Tuple

import numpy as np


def all_zeros(arr: np.array) -> bool:
    return not np.any(arr)


def all_zeros2(arr: np.array) -> bool:
    return sum(arr) == 0


def all_ones(arr: np.array) -> bool:
    return bool(np.all(arr))


def get_max_consecutive_ones(arr: np.ndarray) -> int:
    count = 0
    result = 0
    for i in range(0, 10):
        if not arr[i]:
            count = 0
        else:
            count += 1
            result = max(result, count)
    return result


def get_holes_amount(arr: np.ndarray) -> Tuple[int, int]:
    holes = 0
    almost_holes = 0
    for i in range(0, len(arr)):
        if all_ones(arr[i]) or all_zeros(arr[i]):
            continue
        for j in range(0, len(arr)):
            if arr[i][j]:
                continue
            # дырка - когда вокруг 0 либо стены, либо единицы
            # проверяем все возможные варианты дырок
            conditions = [
                (i == 0 or arr[i - 1][j]),
                (j == 0 or arr[i][j - 1]),
                (i == 9 or arr[i + 1][j]),
                (j == 9 or arr[i][j + 1]),
            ]
            trues_amount = sum(conditions)
            if trues_amount == 4:
                holes += 1
            elif trues_amount == 3:
                almost_holes += 1

    return holes, almost_holes
