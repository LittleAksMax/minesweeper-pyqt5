from .Game import Game
import minesweeper.visualizer as visualizer


def run(rows: int, columns: int, mines: int, window_side_size: int) -> None:
    g = Game(rows, columns, mines)
    visualizer.run(g.minefield, window_side_size, max(window_side_size // columns, 30))
