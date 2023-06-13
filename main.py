from sudoku import *
from sudokuSolver import *

import json

file = open("nytimes-hard-20230515.json", "r").read()
board = json.loads(file)

sudoku = Sudoku(board["puzzle"])

solve = SudokuSolver(sudoku)
solve.print()