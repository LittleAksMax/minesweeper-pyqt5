from typing import List, Tuple, Set, Type, TypeVar
from random import randint
from .SpotState import SpotState
from .SpotValue import SpotValue

MineFieldType: Type = TypeVar("MineFieldType", bound="MineField")

class MineField:
    def __init__(self, rows: int, columns: int, mines: int) -> None:
        self.minefield_state: List[List[int]] = \
            [[SpotState.Untouched for _ in range(rows)] for _ in range(columns)]
        self.minefield: List[List[int]] = \
            [[SpotValue.Nothing for _ in range(rows)] for _ in range(columns)]
        self.mines: int = mines

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
            minefield.minefield[row][col] = SpotValue.Bomb
            # update each neighbor
            up:    bool = row > 0
            down:  bool = row < rows - 1
            left:  bool = col > 0
            right: bool = col < columns - 1
            if left:
                minefield.minefield[row][col - 1] += 1
            if right:
                minefield.minefield[row][col + 1] += 1
            if up:
                minefield.minefield[row - 1][col] += 1
            if down:
                minefield.minefield[row + 1][col] += 1
            if left and up:
                minefield.minefield[row - 1][col - 1] += 1
            if left and down:
                minefield.minefield[row + 1][col - 1] += 1
            if right and up:
                minefield.minefield[row - 1][col + 1] += 1
            if right and down:
                minefield.minefield[row + 1][col + 1] += 1
        return minefield
