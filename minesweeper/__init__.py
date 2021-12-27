"""
Minesweeper game
"""

def f(s):
    if s == 0:
        return "  "
    elif s == 1:
        return "1 "
    elif s == 2:
        return "2 "
    elif s == 3:
        return "3 "
    elif s == 4:
        return "4 "
    elif s == 5:
        return "5 "
    elif s == 6:
        return "6 "
    elif s == 7:
        return "7 "
    elif s == 8:
        return "8 "
    else:
        return "B "

from .Game import Game

def run(rows: int, columns: int, mines: int):
    g = Game(rows, columns, mines)
    for i in range(20):
        for j in range(20):
            print(f(g.minefield.minefield[i][j]), end="")
        print()
