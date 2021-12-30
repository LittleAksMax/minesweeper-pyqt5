from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QCoreApplication, Qt
from .SpotState import SpotState
from .SpotValue import SpotValue
from typing import List, Type, TypeVar

SpotType: Type = TypeVar("SpotType", bound="Spot")


class Spot(QPushButton):
    def __init__(self, row: int, col: int, neighbors: List[SpotType], state: int=SpotState.Hidden, value: int=SpotValue.Nothing) -> None:
        super().__init__()
        self.row = row
        self.col = col
        self.neighbors = neighbors
        self.state = state
        self.value = value

        super().clicked.connect(self.clicked)

    def getGameText(self) -> str:
        if self.state == SpotState.Revealed:
            return " " if self.value == 0 else str(self.value) if self.value < 9 else "B"
        return "!" if self.state == SpotState.Flagged else " "

    def clicked(self) -> None:
        print(f"CLICKED row: {self.row + 1} col: {self.col + 1}")
        return
        if qApp.mouseButtons() & Qt.LeftButton:
            self.state = SpotState.Revealed
            self.setText(QCoreApplication.translate("scrollArea", self.getGameText()))
        elif qApp.mouseButtons() & Qt.RightButton:
            if self.state == SpotState.Revealed:
                return
            self.state = SpotState.Flagged if self.state == SpotState.Untouched else SpotState.Untouched
            self.setText(QCoreApplication.translate("scrollArea", self.getGameText()))
