import numpy as np

from .console import print_tactris
from .game_score import GameScore
from .grid import Grid
from .scoring import Scoring
from .shapes import Shape


class GameOverException(Exception):
    pass


class Tactris:
    def __init__(self, debug=False):
        self.debug = debug
        self.n = 10
        self.board = np.zeros((self.n, self.n), dtype=int)
        self.grid = Grid()
        self.game_score = GameScore()
        self.shape1 = Shape.get_random_shape()
        self.shape2 = Shape.get_random_shape(self.shape1)

    def apply_move(self, shape: Shape, mask):
        if self.debug:
            print_tactris(self, mask)

        lines_removed = self.grid.apply_mask(mask)
        self.game_score.update(lines_removed=lines_removed)
        if shape is self.shape1:
            self.shape1 = Shape.get_random_shape(self.shape1, self.shape2)
        else:
            self.shape2 = Shape.get_random_shape(self.shape1, self.shape2)

    def move(self):
        scoring = Scoring(self.grid.grid, self.shape1, self.shape2)
        _shape, mask = scoring.choose_best_move()
        if mask is None:
            raise GameOverException("Game Over")
        self.apply_move(_shape, mask)
