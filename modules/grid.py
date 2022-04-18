from typing import List
from typing import Tuple

import numpy as np


def get_replacers(lines: np.ndarray) -> Tuple[List, List]:
    closest_lines, farthest_lines = [], []
    for i in lines:
        if i < 5:
            closest_lines.append(np.zeros(10, dtype=int))
        else:
            farthest_lines.append(np.zeros(10, dtype=int))
    return closest_lines, farthest_lines


def roll_empty_lines(grid, lines: np.ndarray) -> np.ndarray:
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
    def completed_rows(self) -> np.ndarray:
        return np.where(np.all(self.grid, axis=1))[0]

    @property
    def completed_cols(self) -> np.ndarray:
        return np.where(np.all(self.grid, axis=0))[0]

    def transform(self, rows: np.ndarray, cols: np.ndarray):
        _block_states = roll_empty_lines(self.grid, rows)
        block_states = roll_empty_lines(_block_states.T, cols)
        self.grid = block_states.T

    def apply_mask(self, mask) -> int:
        self.grid |= mask
        completed_rows: np.ndarray = self.completed_rows
        completed_cols: np.ndarray = self.completed_cols
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
