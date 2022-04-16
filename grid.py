from typing import List
from typing import Tuple

import numpy as np

from shapes import Shape


def all_zeros(arr: np.array) -> bool:
    return not np.any(arr)


def all_ones(arr: np.array) -> bool:
    return np.all(arr)


def any_ones(arr: np.array) -> bool:
    return np.any(arr)


def get_replacers(lines: List[int]) -> Tuple[List, List]:
    closest_lines, farthest_lines = [], []
    for i in lines:
        if i < 5:
            closest_lines.append(np.zeros(10, dtype=int))
        else:
            farthest_lines.append(np.zeros(10, dtype=int))
    return closest_lines, farthest_lines


def roll_empty_lines(grid, lines: List[int]):
    closest_lines, farthest_lines = get_replacers(lines)
    new_states = closest_lines
    for i, line in enumerate(grid):
        if i not in lines:
            new_states.append(line)
    new_states += farthest_lines
    return np.array(new_states)


class Grid:
    def __init__(self):
        self.n = 10
        self.grid = np.zeros((self.n, self.n), dtype=int)

    @property
    def completed_rows(self):
        rows = []
        for i in range(0, self.n):
            if all_ones(self.grid[i]):
                rows.append(i)
        return rows

    @property
    def completed_cols(self):
        cols = []
        transposed = self.grid.T
        for i in range(0, self.n):
            if all_ones(transposed[i]):
                cols.append(i)
        return cols

    def possible_moves_generator(self, shape: Shape):
        for i in range(0, self.n - shape.height + 1):
            for j in range(0, self.n - shape.width + 1):
                mask = np.zeros((self.n, self.n), dtype=int)
                mask[i : shape.height + i, j : shape.width + j] = shape.hash
                if all_zeros(self.grid * mask):
                    yield shape, mask

    def transform(self, rows, cols):
        _block_states = roll_empty_lines(self.grid, rows)
        block_states = roll_empty_lines(_block_states.T, cols)
        self.grid = block_states.T

    def apply_mask(self, mask) -> int:
        self.grid |= mask
        completed_rows = self.completed_rows
        completed_cols = self.completed_cols
        completed_lines = len(completed_rows) + len(completed_cols)
        if completed_lines > 0:
            self.transform(completed_rows, completed_cols)
        return completed_lines

    def rich(self, mask=None) -> str:
        result = ""
        for i in range(self.n):
            for j in range(self.n):
                if mask is not None and bool(mask[i][j]):
                    result += "🟩 "
                elif self.grid[i][j]:
                    result += "🟦 "
                else:
                    result += "⬜ "
            result += "\n"
        return result
