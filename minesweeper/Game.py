from .MineField import MineField

class Game(object):
    def __init__(self, rows: int, columns: int, mines: int) -> None:
        self.rows:    int = rows
        self.columns: int = columns
        self.mines:   int = mines
        self.minefield: MineField = MineField.generate(rows, columns, mines)
