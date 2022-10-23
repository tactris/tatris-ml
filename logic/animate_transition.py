from enum import Enum
from pprint import pprint

import numpy as np


class TransitionState(Enum):
    HOLD = 0
    MOVE = 1
    DESTROY = 2


class BlockTransition:
    def __init__(self, block, state: TransitionState):
        self.block = block
        self.state = state
        self.diff = (0, 0)

    def move_up(self, transposed=False):
        if not self.block.is_filled or self.state == TransitionState.DESTROY:
            return

        self.state = TransitionState.MOVE
        if transposed:
            self.diff = (self.diff[0], self.diff[1] - 1)
        else:
            self.diff = (self.diff[0] - 1, self.diff[1])

    def move_down(self, transposed=False):
        if not self.block.is_filled or self.state == TransitionState.DESTROY:
            return

        self.state = TransitionState.MOVE
        if transposed:
            self.diff = (self.diff[0], self.diff[1] + 1)
        else:
            self.diff = (self.diff[0] + 1, self.diff[1])

    def destroy(self):
        self.state = TransitionState.DESTROY

    @property
    def is_filled(self) -> bool:
        return self.block.is_filled

    def __repr__(self) -> str:
        if self.state == TransitionState.HOLD:
            if self.block.is_filled:
                return "🟪"
            else:
                return "🟧"
        elif self.state == TransitionState.MOVE:
            return "🟨"
        else:
            return "🟥"


class Block:
    def __init__(self, is_filled):
        self.is_filled = is_filled

    def fill(self):
        self.is_filled = True

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return "🟦 " if self.is_filled else "⬜ "


class GameField:
    def __init__(self, n):
        self.n = n
        self.grid = []
        for i in range(n):
            row = []
            for j in range(n):
                row.append(Block(False))
            self.grid.append(row)

    def proceed_transition(self, transition_grid: np.ndarray, transposed=False):
        if transposed:
            transition_grid = transition_grid.T

        completed_lines = []
        for i, row in enumerate(transition_grid):
            if all([block.is_filled for block in row]):
                completed_lines.append(i)

        for row_idx in completed_lines:
            # mark row as destroy
            for transition_block in transition_grid[row_idx]:
                transition_block.destroy()

            if row_idx < 5:
                # we need to move down all the lines above
                for i in range(0, row_idx):
                    for transition_block in transition_grid[i]:
                        transition_block.move_down(transposed=transposed)
            else:
                # we need to move up all the lines below
                for i in range(row_idx + 1, self.n):
                    for transition_block in transition_grid[i]:
                        transition_block.move_up(transposed=transposed)

    def tactris(self):
        print("\nCREATE TRANSITION MATRIX\n")
        transition_grid = np.zeros((self.n, self.n), dtype=BlockTransition)
        for i, row in enumerate(self.grid):
            transition_grid[i] = [BlockTransition(block, TransitionState.HOLD) for block in row]

        print(transition_grid)

        print("\nPROCEED TRANSITION FOR MATRIX\n")
        self.proceed_transition(transition_grid)

        print(transition_grid)

        print("\nPROCEED TRANSITION FOR TRANSPOSED MATRIX\n")
        self.proceed_transition(transition_grid, transposed=True)

        print(transition_grid)

    def __getitem__(self, item):
        return self.grid[item]

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return '\n'.join(''.join(str(block) for block in row) for row in self.grid)


def main():
    n = 10
    grid = GameField(n)

    grid[4][6].fill()
    grid[4][7].fill()
    grid[4][8].fill()
    grid[4][9].fill()
    for i in range(n):
        grid[5][i].fill()
    grid[6][0].fill()
    grid[6][1].fill()
    grid[6][2].fill()
    grid[6][3].fill()

    for i in range(n):
        grid[7][i].fill()

    for j in range(n):
        grid[j][2].fill()

    grid[8][6].fill()
    grid[8][7].fill()
    grid[8][8].fill()
    grid[8][9].fill()

    print("INITIAL GRID\n")
    pprint(grid)

    grid.tactris()


if __name__ == "__main__":
    main()
