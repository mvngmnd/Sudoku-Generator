from sudoku import Sudoku, Cell, getHints
from copy import deepcopy
from typing import List

# Solves single hints.
# 
# If only one cell in the region has a hint that others don't, that cell must be the hint value. 
# 
# Also attempts to solve any naked singles present.

class SolveSingleHints:

    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku

    def run(self):
        solved = False

        solved |= self.solveSingleRegionsHint(self.sudoku.getBlocks())
        solved |= self.solveSingleRegionsHint(self.sudoku.getRows())
        solved |= self.solveSingleRegionsHint(self.sudoku.getColumns())

        solved |= self.solveSingleRegionsNakedSingles(self.sudoku.getBlocks())
        solved |= self.solveSingleRegionsNakedSingles(self.sudoku.getRows())
        solved |= self.solveSingleRegionsNakedSingles(self.sudoku.getColumns())

        return solved

    def solveSingleRegionsNakedSingles(self, regions):
        solved = False
        for region in regions:
            solved |= self.__solveSingleRegionNakedSingles(region)
        return solved

    def __solveSingleRegionNakedSingles(self, region):
        solved = False

        for cell in region:
            if (len(cell.hints) == 1):
                # Naked single with only one hint. Must be that value.
                cell.setValue(cell.hints.pop())
                solved = True

        return solved

    def solveSingleRegionsHint(self, regions):
        solved = False
        for region in regions:
            solved |= self.__solveSingleHint(region)
        return solved

    def __solveSingleHint(self, section: List[Cell]):
        solved = False

        for i in range(len(section)):
            cell = section[i]

            hints = set(cell.hints)
            otherCells = deepcopy(section)
            del otherCells[i]

            # The set difference between all other hints present in the region.
            myHint = hints.difference(set(getHints(otherCells)))

            # If there is a hint here, it means this cell is the only one with that hint.
            if (len(myHint) == 1):
                cell.setValue(myHint.pop())
                solved = True

        return solved