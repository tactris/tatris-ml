from typing import Tuple

import numpy as np

from grid import all_ones
from shapes import Shape


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


REMOVED_LINES_MULTIPLIER = 1000
CONSECUTIVE_ONES_MULTIPLIER = 50


class Scoring:
    def __init__(self, grid, possible_moves: list):
        self.grid: np.ndarray = grid
        self.possible_moves = possible_moves

    def score_move(self, mask):
        removed_lines = 0
        consecutive_ones = 0
        disjuncted = self.grid | mask
        for i, row in enumerate(disjuncted):
            ## is tactris?
            if all_ones(row):
                removed_lines += 1
            ## check distance to existing shapes
            consecutive_ones += get_max_consecutive_ones(row) ** 2
        for col in disjuncted.T:
            if all_ones(col):
                removed_lines += 1
            consecutive_ones += get_max_consecutive_ones(col) ** 2
        return REMOVED_LINES_MULTIPLIER * removed_lines + consecutive_ones * CONSECUTIVE_ONES_MULTIPLIER

    def choose_best_move(self) -> Tuple[Shape, np.ndarray]:
        best_score = 0
        best_move = self.possible_moves[0]
        for shape, mask in self.possible_moves:
            score = self.score_move(mask)
            if score > best_score:
                best_score = score
                best_move = (shape, mask)
        return best_move
