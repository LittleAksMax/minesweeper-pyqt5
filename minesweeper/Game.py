from PyQt5.QtWidgets import QApplication
from .MineField import MineField
import sys


class Game(object):
    def __init__(self, rows: int, columns: int, mines: int) -> None:
        app = QApplication(sys.argv)
        ui = MineField.generate(rows, columns, mines)
        ui.show()
        self.minefield: MineField = MineField.generate(rows, columns, mines)
        sys.exit(app.exec_())
