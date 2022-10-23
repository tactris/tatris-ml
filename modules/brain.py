import random
from typing import Dict

from rich.table import Table


EMPIRICAL_SCORES = {
    'REMOVED_LINES_MULTIPLIER': 1239.19,
    'CONSECUTIVE_ONES_MULTIPLIER': 21.85,
    'HOLES_MULTIPLIER': -319.69,
    'ALMOST_HOLES_MULTIPLIER': -77.37,
}


class Brain:
    def __init__(self, is_first: bool = False):
        self.multipliers: Dict[str, float] = {}
        if is_first:
            self.set_as_my_multipliers()
        else:
            self.randomize_multipliers()

    def set_as_my_multipliers(self):
        self.multipliers = EMPIRICAL_SCORES.copy()

    def randomize_multipliers(self):
        self.multipliers = {
            'REMOVED_LINES_MULTIPLIER': EMPIRICAL_SCORES['REMOVED_LINES_MULTIPLIER'] * random.uniform(0, 2),
            'CONSECUTIVE_ONES_MULTIPLIER': EMPIRICAL_SCORES['CONSECUTIVE_ONES_MULTIPLIER'] * random.uniform(0, 2),
            'HOLES_MULTIPLIER': EMPIRICAL_SCORES['HOLES_MULTIPLIER'] * random.uniform(0, 2),
            'ALMOST_HOLES_MULTIPLIER': EMPIRICAL_SCORES['ALMOST_HOLES_MULTIPLIER'] * random.uniform(0, 2),
        }

    def mutate(self):
        mutation_rate = 0.1
        for key in self.multipliers:
            if random.random() < mutation_rate:
                self.multipliers[key] *= random.uniform(0.95, 1.05)

    def set_multipliers(self, multipliers):
        self.multipliers = multipliers

    def clone(self) -> 'Brain':
        copy = Brain(False)
        copy.set_multipliers(self.multipliers)
        return copy

    def get_cost_of_matrix(self, removed_lines, consecutive_ones, holes, almost_holes):
        return (
            self.multipliers['REMOVED_LINES_MULTIPLIER'] * removed_lines
            + self.multipliers['CONSECUTIVE_ONES_MULTIPLIER'] * consecutive_ones
            + self.multipliers['HOLES_MULTIPLIER'] * holes
            + self.multipliers['ALMOST_HOLES_MULTIPLIER'] * almost_holes
        )

    def rich(self):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Multiplier")
        table.add_column("Value")
        for key in self.multipliers:
            table.add_row(key, f'{self.multipliers[key]:.2f}')
        return table
