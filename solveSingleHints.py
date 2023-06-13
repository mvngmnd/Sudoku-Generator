from copy import deepcopy
from typing import List

from sudoku import Sudoku, Cell, getHints

# Solves single hints.
# 
# If only one cell in the section has a hint that others don't, that cell must be the hint value. 
# 
# Also attempts to solve any naked singles present.

class SolveSingleHints:

    def __init__(self, sudoku: Sudoku, logging = False):
        self.sudoku = sudoku
        self.logging = logging

    def run(self):
        solved = False

        solved |= self.solveSingleSectionsHint(self.sudoku.getRows())
        solved |= self.solveSingleSectionsHint(self.sudoku.getColumns())
        solved |= self.solveSingleSectionsHint(self.sudoku.getBlocks())

        solved |= self.solveSingleSectionsNakedSingles(self.sudoku.getRows())
        solved |= self.solveSingleSectionsNakedSingles(self.sudoku.getColumns())
        solved |= self.solveSingleSectionsNakedSingles(self.sudoku.getBlocks())

        return solved

    def solveSingleSectionsNakedSingles(self, sections):
        solved = False
        for section in sections:
            solved |= self.__solveSingleSectionNakedSingles(section)
        return solved

    def __solveSingleSectionNakedSingles(self, section:List[Cell]):
        solved = False

        for cell in section:
            if (len(cell.hints) == 1):
                # Naked single with only one hint. Must be that value.
                cell.setValue(cell.hints.pop(), self.__class__.__name__, self.logging)
                solved = True

        return solved

    def solveSingleSectionsHint(self, sections):
        solved = False
        for section in sections:
            solved |= self.__solveSingleHint(section)
        return solved

    def __solveSingleHint(self, section: List[Cell]):
        solved = False

        for i in range(len(section)):
            cell = section[i]

            hints = set(cell.hints)
            otherCells = deepcopy(section)
            del otherCells[i]

            # The set difference between all other hints present in the section.
            myHint = hints.difference(set(getHints(otherCells)))

            # If there is a hint here, it means this cell is the only one with that hint.
            if (len(myHint) == 1):
                cell.setValue(myHint.pop(), self.__class__.__name__, self.logging)
                solved = True

        return solved