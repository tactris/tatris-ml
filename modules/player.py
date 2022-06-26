from .AI import AI
from .brain import Brain
from .tactris import Tactris


class Player:
    def __init__(self, _id: int, brain: Brain):
        self._id = _id
        self.brain = brain
        self.current_game = Tactris()
        self.is_dead = False

    @property
    def tetris_rate(self) -> float:
        return self.current_game.tetris_rate

    @property
    def fitness(self) -> float:
        # return self.score * (1 + self.tetris_rate)
        return self.score

    @property
    def score(self) -> int:
        return self.current_game.game_score.score

    def clone(self):
        return Player(self._id, self.brain.clone())

    def update(self):
        if self.is_dead:
            return

        shape, mask = AI.choose_best_move(
            self.brain, self.current_game.grid.grid, self.current_game.shape1, self.current_game.shape2
        )
        if mask is None:
            self.is_dead = True
        else:
            self.current_game.apply_move(shape, mask)

    def __str__(self):
        return f"Player {self._id} with score {self.score} and fitness {self.fitness}"
