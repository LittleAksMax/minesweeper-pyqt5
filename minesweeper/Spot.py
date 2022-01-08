from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5 import QtGui
from .SpotState import SpotState
from .SpotValue import SpotValue
from typing import List, Type, TypeVar

SpotType: Type = TypeVar("SpotType", bound="Spot")


class Spot(QPushButton):
    def __init__(self, row: int, col: int, state: int=SpotState.Hidden, value: int=SpotValue.Nothing) -> None:
        super().__init__()
        self.row: int = row
        self.col: int = col
        self.neighbors: List[SpotType] = []
        self.state: int = state
        self.value: int = value
        self.neighboring_mines: int = 0

    def flood_fill(self, seen: List[SpotType]=None):
        if seen is None:
            seen = set()
        elif self in seen:
            # already checked this node
            return

        self.state = SpotState.Revealed
        self.updateText()
        if self.value == SpotValue.Bomb or self.neighboring_mines > self.value:
            # TODO: player lost
            return
        elif self.neighboring_mines < self.value:
            # not enough bombs flagged to flood_fill
            return
        seen.add(self)
        print(self.neighboring_mines, self.value)
        for neighbor in self.neighbors:
            if neighbor.state != SpotState.Flagged:
                neighbor.flood_fill(seen)

    def getGameText(self) -> str:
        if self.state == SpotState.Revealed:
            return " " if self.value == 0 else str(self.value) if self.value < 9 else "B"
        return "!" if self.state == SpotState.Flagged else " "
    
    def updateText(self):
        self.setText(QCoreApplication.translate("scrollArea", self.getGameText()))
    
    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        if e.button() == Qt.LeftButton:
            if self.state == SpotState.Flagged:
                # can't reveal flagged spot
                return
            self.flood_fill()
        elif e.button() == Qt.RightButton:
            if self.state == SpotState.Revealed:
                return
            self.state = SpotState.Flagged if self.state == SpotState.Hidden else SpotState.Hidden
            for neighbor in self.neighbors: neighbor.neighboring_mines += 1
            self.updateText()
