import time
from typing import List

import numpy as np
from rich import console
from rich.columns import Columns


console = console.Console()


def print_tactris(tactris, mask=None):
    console.clear()
    console.print(
        Columns(
            [tactris.grid.rich(mask=mask), tactris.shape1.rich(), tactris.shape2.rich(), tactris.game_score.rich()],
            padding=(0, 3),
            title="            Grid               Shape1    Shape2    Score",
        )
    )
    time.sleep(0.5)


def print_results(total_scores: List[int]):
    console.log(
        Columns(
            [
                f"{np.mean(total_scores):.2f}",
                f"{np.median(total_scores):.2f}",
                f"{np.max(total_scores):.2f}",
                f"{np.min(total_scores):.2f}",
            ],
            padding=(1, 3),
            title="Mean    Median      Max      Min",
        )
    )
