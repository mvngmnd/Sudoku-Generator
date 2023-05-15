from sudoku import Sudoku, Cell, getHints
from copy import deepcopy
from typing import List

# Used to solve single hints. If only one cell in the region has a given possible value
# that cell must be that value. Also attemps to solve any naked singles present.
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
                cell.setValue(cell.hints.pop())
                solved = True

        return solved

    def solveSingleRegionsHint(self, regions):
        solved = False
        for region in regions:
            solved |= self.__solveSingleHint(region)
        return solved

    def __solveSingleHint(self, section: List[Cell]):
        '''Attemps to solve by checking if a cell has a hint that is not present elsewhere in the row/column/block.'''
        solved = False

        for i in range(len(section)):
            cell = section[i]

            hints = set(cell.hints)
            others = deepcopy(section)
            del others[i]

            othersHints = set(getHints(others))
            myHint = hints.difference(othersHints)

            if (len(myHint) == 1):
                cell.setValue(myHint.pop())
                solved = True

        return solved