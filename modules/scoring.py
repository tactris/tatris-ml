from typing import Optional
from typing import Tuple

import numpy as np

from .shapes import Shape
from .utils import all_ones
from .utils import all_zeros
from .utils import get_holes_amount
from .utils import get_max_consecutive_ones


REMOVED_LINES_MULTIPLIER = 1500
CONSECUTIVE_ONES_MULTIPLIER = 70
HOLES_MULTIPLIER = -600
ALMOST_HOLES_MULTIPLIER = -500


class Scoring:
    def __init__(self, grid: np.ndarray, *shapes: Shape):
        self.n = len(grid)
        self.grid = grid
        self.shapes = shapes

    def score_move(self, mask: np.ndarray) -> int:
        disjuncted = self.grid | mask
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
        return (
            REMOVED_LINES_MULTIPLIER * removed_lines
            + CONSECUTIVE_ONES_MULTIPLIER * consecutive_ones
            + HOLES_MULTIPLIER * holes
            + ALMOST_HOLES_MULTIPLIER * almost_holes
        )

    def possible_moves_generator(self, shape: Shape):
        for i in range(0, self.n - shape.height + 1):
            for j in range(0, self.n - shape.width + 1):
                mask = np.zeros((self.n, self.n), dtype=int)
                mask[i : shape.height + i, j : shape.width + j] = shape.hash
                if all_zeros(self.grid * mask):
                    yield shape, mask

    @property
    def possible_moves(self):
        for shape in self.shapes:
            yield from self.possible_moves_generator(shape)

    def choose_best_move(self) -> Tuple[Optional[Shape], Optional[np.ndarray]]:
        best_score = -1
        best_move = (None, None)
        for shape, mask in self.possible_moves:
            score = self.score_move(mask)
            if score > best_score:
                best_score = score
                best_move = (shape, mask)
        return best_move
