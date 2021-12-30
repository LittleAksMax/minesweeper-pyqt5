from .Game import Game


def run(rows: int, columns: int, mines: int, window_side_size: int) -> None:
    g = Game(rows, columns, mines)
