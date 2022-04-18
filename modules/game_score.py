class GameScore:
    def __init__(self):
        self.score = 0

    @staticmethod
    def calculate_score_incr(lines_removed: int):
        default_incr = 4
        lines_incr = lines_removed * 10 * lines_removed
        return default_incr + lines_incr

    def update(self, lines_removed: int) -> None:
        score_incr = self.calculate_score_incr(lines_removed=lines_removed)
        self.score += score_incr

    def rich(self) -> str:
        return f"[green]{self.score}[/green]"
