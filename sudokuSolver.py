from sudoku import Sudoku, Cell, getValues, getHints
from copy import deepcopy
from typing import List

from removeNakedSubsets import RemoveNakedSubsets
from solveSingleHints import *

class SudokuSolver:

    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku
        
        self.runSolveStrategiesClassLoop([RemoveNakedSubsets, SolveSingleHints])

    def runSolveStrategiesClassLoop(self, strategies):
        for strategy in strategies:
            obj = strategy(self.sudoku)
            self.__runSolveStrategyLoop(obj.run)

    def runSolveStrategiesLoop(self, strategies):
        for strategy in strategies:
            self.__runSolveStrategyLoop(strategy)

    def boardHasChanged(self, sudoku1: Sudoku, sudoku2: Sudoku):
        for y in range(0,9):
            for x in range(0,9):
                b1 = sudoku1.getRow(y)[x]
                b2 = sudoku2.getRow(y)[x]

                if (b1.solved != b2.solved or set(b1.hints) != set(b2.hints)):
                    return True
        return False

    def print(self):
        self.sudoku.print()

    def __runSolveStrategyLoop(self, strategy):
        while(self.__runSolveStrategy(strategy)):
            continue
        return False

    def __runSolveStrategy(self, strategy):
        self.sudoku.setHints()
        boardCopy = deepcopy(self.sudoku)
        strategy()
        self.sudoku.setHints()
        return self.boardHasChanged(boardCopy, self.sudoku)