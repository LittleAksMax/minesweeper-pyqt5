from minesweeper import run
from sys import setrecursionlimit

if __name__ == "__main__":
    setrecursionlimit(10000)
    run(50, 50, 500, 800)
