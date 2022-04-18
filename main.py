#!/usr/bin/env python3
import typer
from rich.progress import track

from modules import GameOverException
from modules import Tactris
from modules import print_results


app = typer.Typer()


def main(gen, repeat: int = 10, _debug: bool = False):
    scores = []
    for _ in range(repeat) if _debug else track(range(repeat), description=f"Generation {gen}"):
        tactris = Tactris(debug=_debug)
        while True:
            try:
                tactris.move()
            except GameOverException:
                break
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
