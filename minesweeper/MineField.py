from PyQt5.QtWidgets import QWidget, QLabel, QLabel, QScrollArea, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QRect, QCoreApplication, QSize
from typing import List, Tuple, Set, Type, TypeVar, Callable
from random import randint
from .SpotValue import SpotValue
from .Spot import Spot

MineFieldType: Type = TypeVar("MineFieldType", bound="MineField")

class MineField(QWidget):
    window_side_size = 800

    def __init__(self, rows: int, columns: int, mines: int) -> None:
        super().__init__()

        self.mines:   int = mines
        self.rows:    int = rows
        self.columns: int = columns

        self.setObjectName("MinesweeperWindow")
        self.setFixedSize(MineField.window_side_size, MineField.window_side_size)
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
        self.minesRemainingLabel.setText(QCoreApplication.translate("MainWindow", str(self.mines)))

        self.mines: List[Spot] = []
        spot_size = max(MineField.window_side_size // columns, 30)
        self.spots: List[Spot] = []
        self.generate_minefield_elements(spot_size)
    
    def generate_minefield_elements(self, spot_size: int) -> None:
        f: Callable[[int], str] = lambda x: " " if x == 0 else str(x) if x < 9 else "!"
        x = y = 0 # starting positions, non-zero for a bit of padding
        for row in range(self.rows):
            for col in range(self.columns):
                spot = Spot(row, col)
                spot.setEnabled(True)
                spot.setFixedSize(QSize(spot_size, spot_size))
                spot.setObjectName(f"spot_{x}_{y}")
                spot.setText(QCoreApplication.translate("scrollArea", spot.getGameText()))

                self.gridLayout.addWidget(spot, x, y, spot_size, spot_size)
                self.spots.append(spot)
                x += spot_size
            y += spot_size # newline
            x = 0               # carriage return
        for row in range(self.rows):
            for col in range(self.columns):
                self.spots[row * self.columns + col].neighbors = self.get_neighbors((row, col), self.rows, self.columns)
    
    def get_neighbors(self, spot: Tuple[int, int], rows: int, columns: int) -> List[Spot]:
        row, col = spot
        up:    bool = row > 0
        down:  bool = row < rows - 1
        left:  bool = col > 0
        right: bool = col < columns - 1
        neighbors: List[Tuple[int, int]] = []  # tuple is [row, col]
        if left:
            neighbors.append(self.spots[row * self.columns + col - 1])
        if right:
            neighbors.append(self.spots[row * self.columns + col + 1])
        if up:
            neighbors.append(self.spots[(row - 1) * self.columns + col])
        if down:
            neighbors.append(self.spots[(row + 1) * self.columns + col])
        if left and up:
            neighbors.append(self.spots[(row - 1) * self.columns + col - 1])
        if left and down:
            neighbors.append(self.spots[(row + 1) * self.columns + col - 1])
        if right and up:
            neighbors.append(self.spots[(row - 1) * self.columns + col + 1])
        if right and down:
            neighbors.append(self.spots[(row + 1) * self.columns + col + 1])
        return neighbors

    @classmethod
    def generate(cls: Type[MineFieldType], rows: int, columns: int, mines: int) -> MineFieldType:
        minefield = cls(rows, columns, mines)

        # randomly generate mines
        seen: Set[Tuple[int, int]] = set()
        for _ in range(mines):
            row: int = -1
            col: int = -1
            while (row, col) in seen:
                row = randint(0, rows - 1)
                col = randint(0, columns - 1)
            seen.add((row, col))
            spot: Spot = minefield.spots[row * minefield.columns + col]
            spot.value = SpotValue.Bomb
            minefield.mines.append(spot)

            # update each neighbor
            for neighbor in spot.neighbors:
                neighbor.value += 1
        return minefield
