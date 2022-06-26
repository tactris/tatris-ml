class GameScore:
    def __init__(self):
        self.score = 0
        self.total_lines_removed = 0
        self.total_moves = 0

    @staticmethod
    def calculate_score_incr(lines_removed: int):
        default_incr = 4
        lines_incr = lines_removed * 10 * lines_removed
        return default_incr + lines_incr

    def update(self, lines_removed: int) -> None:
        score_incr = self.calculate_score_incr(lines_removed=lines_removed)
        self.score += score_incr
        self.total_lines_removed += lines_removed
        self.total_moves += 1

    def get_tetris_rate(self) -> float:
        return self.total_moves / max(1, self.total_lines_removed)

    def rich(self) -> str:
        return f"[green]{self.score}[/green]"
