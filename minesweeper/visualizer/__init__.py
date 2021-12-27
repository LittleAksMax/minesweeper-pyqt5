from .Window import Window
from ..MineField import MineField
import sys
from PyQt5.QtWidgets import QApplication


def run(minefield: MineField, window_side_size: int, spot_size: int):
    app = QApplication(sys.argv)
    ui = Window(minefield, window_side_size, spot_size)
    ui.show()
    sys.exit(app.exec_())
