import random

from modules.brain import Brain
from modules.console import console
from modules.player import Player


class Population:
    def __init__(self, size: int):
        self.players = []
        self.generation = 0

        # population staff
        for i in range(size):
            if i == 0:
                console.print("Creating first player")
                brain = Brain(is_first=True)
                console.print(brain.rich())
                self.players.append(Player(i, brain=brain))
            else:
                self.players.append(Player(i, brain=Brain(is_first=False)))

    def update(self):
        for player in self.players:
            player.update()

    def natural_selection(self):
        next_generation = []

        console.print(f"Best player is {self.best_player}")
        console.print(self.best_player.brain.rich())
        parent = self.best_player
        child = parent.clone()
        child.brain.mutate()
        next_generation.append(child)
        while len(next_generation) < len(self.players):
            parent = self.select_player()
            child = parent.clone()
            child.brain.mutate()
            next_generation.append(child)

        self.players = next_generation
        self.generation += 1

    def select_player(self) -> Player:
        random_number = random.uniform(0, self.fitness_sum)
        running_sum = 0.0
        for player in self.players:
            running_sum += player.fitness
            if running_sum > random_number:
                return player
        return self.players[-1]

    @property
    def best_player(self) -> Player:
        return max(self.players, key=lambda x: x.fitness)

    @property
    def fitness_sum(self) -> float:
        return sum(player.fitness for player in self.players)

    @property
    def average_fitness(self) -> float:
        return round(self.fitness_sum / len(self.players), 2)

    def are_all_players_dead(self) -> bool:
        for player in self.players:
            if not player.is_dead:
                return False
        return True

    def show(self):
        print(f"Gen: {self.generation}\t\t Average Fitness: {self.average_fitness}")
