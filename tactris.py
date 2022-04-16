import time

import numpy as np
import typer
from rich import console
from rich.columns import Columns
from rich.progress import track

from game_score import GameScore
from grid import Grid
from scoring import Scoring
from shapes import Shape
from shapes import get_random_shape


console = console.Console()


class GameOverException(Exception):
    pass


class Tactris:
    def __init__(self, debug=False):
        self.debug = debug
        self.n = 10
        self.board = np.zeros((self.n, self.n), dtype=int)
        self.grid = Grid()
        self.game_score = GameScore()
        self.shape1 = get_random_shape()
        self.shape2 = get_random_shape(self.shape1)

    def apply_move(self, shape: Shape, mask):
        if self.debug:
            console.clear()
            self.draw(mask)
            time.sleep(0.5)

        lines_removed = self.grid.apply_mask(mask)
        self.game_score.update(lines_removed=lines_removed)
        if shape is self.shape1:
            self.shape1 = get_random_shape(self.shape1, self.shape2)
        else:
            self.shape2 = get_random_shape(self.shape1, self.shape2)

    def move(self):
        possible_moves = []
        for shape in [self.shape1, self.shape2]:
            for move in self.grid.possible_moves_generator(shape):
                possible_moves.append(move)
        if not possible_moves:
            raise GameOverException("Game Over")
        scoring = Scoring(self.grid.grid, possible_moves)
        _shape, mask = scoring.choose_best_move()
        self.apply_move(_shape, mask)

    def draw(self, mask=None):
        console.print(
            Columns(
                [self.grid.rich(mask=mask), self.shape1.rich(), self.shape2.rich(), self.game_score.rich()],
                padding=(0, 3),
                # equal=True,
                title="            Grid               Shape1    Shape2    Score",
            )
        )


def main(repeat: int = 100, debug: bool = False):
    scores = []
    for i in track(range(repeat), description="Generation"):
        tactris = Tactris(debug=debug)
        while True:
            try:
                tactris.move()
            except GameOverException:
                break
        scores.append(tactris.game_score.score)

    print(
        f"Average score: {np.mean(scores)}, median: {np.median(scores)}, max: {np.max(scores)}, min: {np.min(scores)}"
    )


if __name__ == "__main__":
    typer.run(main)
