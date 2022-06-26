#!/usr/bin/env python3
import typer
from rich.progress import track

from modules import AI
from modules import Brain
from modules import Tactris
from modules import print_results
from modules.population import Population


app = typer.Typer()


def main(gen, repeat: int = 10, _debug: bool = False):
    scores = []
    brain = Brain(is_first=True)
    for _ in range(repeat) if _debug else track(range(repeat), description=f"Generation {gen}"):
        tactris = Tactris(debug=_debug)
        while True:
            shape, mask = AI.choose_best_move(brain, tactris.grid.grid, tactris.shape1, tactris.shape2)
            if mask is None:
                break
            else:
                tactris.apply_move(shape, mask)  # type: ignore
        scores.append(tactris.game_score.score)

    return scores


@app.command()
def run(repeat: int = 100):
    import multiprocessing

    MULTIPROCESSING_CORES = 5

    with multiprocessing.Pool(processes=MULTIPROCESSING_CORES) as pool:
        subset = repeat // MULTIPROCESSING_CORES
        results = pool.starmap(main, [(i, subset, False) for i in range(0, MULTIPROCESSING_CORES)])

    total_scores: list[int] = sum(results, [])
    print_results(total_scores)


@app.command()
def ai(population_size: int = 16):
    population = Population(population_size)
    while True:
        if not population.are_all_players_dead():
            # population.show()
            population.update()
        else:
            population.natural_selection()
            # population.show()
            population.update()

    # tactris = Tactris(debug=True)
    # while True:
    #     try:
    #         tactris.move()
    #     except GameOverException:
    #         break
    # print_results(tactris.game_score.score)


@app.command()
def debug():
    main(1, repeat=1, _debug=True)


@app.command()
def profile():
    from pyinstrument import Profiler

    with Profiler() as prof:
        main(0, repeat=10, _debug=False)
    prof.print()


if __name__ == "__main__":
    app()
    # ai()
