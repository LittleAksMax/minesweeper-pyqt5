from PyQt5.QtWidgets import QPushButton, QSizePolicy, QWidget, QLabel, QLabel, QScrollArea, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QRect, QCoreApplication, QSize
from ..MineField import MineField
from typing import List, Tuple, Callable


class Window(QWidget):
    def __init__(self, minefield: MineField, window_side_size: int, spot_size: int) -> None:
        """
        Square window
        """
        self.spot_size: int = spot_size # each spot is a square button with `spot_size` sized sides
        self.mines: List[Tuple[int, int, int, int]] = [] # Each tuple gives you (co-ord_x, co-ord_y, row_idx, col_idx)
                                                         # for easier access to minefield
        self.mine_widgets: List[QPushButton] = []

        super(Window, self).__init__()
        self.setObjectName("MinesweeperWindow")
        self.setFixedSize(window_side_size, window_side_size)
        self.setWindowTitle("Minesweeper")
        font: QFont = QFont()
        font.setPointSize(12)

        self.centralWidget = QWidget(self)
        self.centralWidget.setGeometry(QRect(0, 20, 800, 780))

        self.layout = QHBoxLayout(self.centralWidget)
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setSpacing(0)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.layout.addWidget(self.scrollArea)

        self.label = QLabel(self)
        self.label.setGeometry(QRect(640, 0, 120, 20))
        self.label.setObjectName("label")
        self.label.setText(QCoreApplication.translate("MainWindow", "Mines remaining:"))
        self.minesRemainingLabel = QLabel(self)
        self.minesRemainingLabel.setGeometry(750, 0, 50, 20)
        self.minesRemainingLabel.setObjectName("minesRemainingLabel")
        self.minesRemainingLabel.setText(QCoreApplication.translate("MainWindow", str(minefield.mines)))
        self.label2 = QLabel(self)
        self.label2.setGeometry(QRect(10, 0, 120, 20))
        self.label2.setObjectName("label2")
        self.label2.setText(QCoreApplication.translate("MainWindow", "Mode:"))
        self.modeLabel = QLabel(self)
        self.modeLabel.setGeometry(QRect(50, 0, 60, 20))
        self.modeLabel.setObjectName("modeLabel")
        self.modeLabel.setText(QCoreApplication.translate("MainWindow", "Flagging"))

        self.generate_minefield_elements(minefield)

    def generate_minefield_elements(self, minefield: MineField) -> None:
        f: Callable[[int], str] = lambda x: " " if x == 0 else str(x) if x < 9 else "!"
        x = y = 0 # starting positions, non-zero for a bit of padding
        for row in range(minefield.rows):
            for col in range(minefield.columns):
                spot = QPushButton()
                spot.setEnabled(True)
                spot.setFixedSize(QSize(self.spot_size, self.spot_size))
                spot.setObjectName(f"spot_{x}_{y}")
                spot.setText(QCoreApplication.translate("scrollArea", f(minefield.minefield[row][col])))

                self.mines.append((x, y, col, row))
                self.gridLayout.addWidget(spot, x, y, self.spot_size, self.spot_size)
                x += self.spot_size
            y += self.spot_size # newline
            x = 0               # carriage return
    
    def update_mines_remaining(self, mines: int) -> None:
        self.minesRemainingLabel.setText(QCoreApplication.translate("MainWindow", str(mines)))

