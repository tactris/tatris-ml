import random
from typing import Dict

from rich.table import Table


class Brain:
    def __init__(self, is_first: bool = False):
        self.multipliers: Dict[str, float] = {}
        if is_first:
            self.set_as_my_multipliers()
        else:
            self.randomize_multipliers()

    def set_as_my_multipliers(self):
        self.multipliers = {
            'REMOVED_LINES_MULTIPLIER': 794.07,
            'CONSECUTIVE_ONES_MULTIPLIER': 23.54,
            'HOLES_MULTIPLIER': -362.98,
            'ALMOST_HOLES_MULTIPLIER': -84.40,
        }

    def randomize_multipliers(self):
        self.multipliers = {
            'REMOVED_LINES_MULTIPLIER': 1500 * random.uniform(0, 2),
            'CONSECUTIVE_ONES_MULTIPLIER': 60 * random.uniform(0, 2),
            'HOLES_MULTIPLIER': -700 * random.uniform(0, 2),
            'ALMOST_HOLES_MULTIPLIER': -500 * random.uniform(0, 2),
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
