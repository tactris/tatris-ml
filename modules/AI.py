from typing import Optional
from typing import Tuple

import numpy as np

from .brain import Brain
from .shapes import Shape
from .utils import all_ones
from .utils import all_zeros
from .utils import get_holes_amount
from .utils import get_max_consecutive_ones


class Scoring:
    @classmethod
    def score_move(cls, brain: Brain, grid: np.ndarray, mask: np.ndarray) -> int:
        disjuncted = grid | mask
        removed_lines = 0
        consecutive_ones = 0
        holes, almost_holes = get_holes_amount(disjuncted)
        for i, row in enumerate(disjuncted):
            # is tactris?
            if all_ones(row):
                removed_lines += 1
            # check distance to existing shapes
            consecutive_ones += get_max_consecutive_ones(row) ** 2
        for col in disjuncted.T:
            if all_ones(col):
                removed_lines += 1
            consecutive_ones += get_max_consecutive_ones(col) ** 2
        return brain.get_cost_of_matrix(removed_lines, consecutive_ones, holes, almost_holes)

    @classmethod
    def possible_moves_generator(cls, grid: np.ndarray, shape: Shape):
        n = len(grid)
        for i in range(0, n - shape.height + 1):
            for j in range(0, n - shape.width + 1):
                mask = np.zeros((n, n), dtype=int)
                mask[i : shape.height + i, j : shape.width + j] = shape.hash
                if all_zeros(grid * mask):
                    yield shape, mask

    @classmethod
    def get_possible_moves(cls, grid: np.ndarray, *shapes: Shape):
        for shape in shapes:
            yield from cls.possible_moves_generator(grid, shape)

    @classmethod
    def choose_best_move(cls, brain, grid: np.ndarray, *shapes: Shape) -> Tuple[Optional[Shape], Optional[np.ndarray]]:
        best_score = -1
        best_move = (None, None)
        for shape, mask in cls.get_possible_moves(grid, *shapes):
            score = cls.score_move(brain, grid, mask)
            if score > best_score:
                best_score = score
                best_move = (shape, mask)
        return best_move


AI = Scoring()
