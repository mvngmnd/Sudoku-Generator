from itertools import product, groupby
from copy import deepcopy
from typing import List

from sudoku import Sudoku, Section, Cell

# Removes hidden pairs.
# 
# If two given hints are only present in two cells, these are a hidden pair for a section.

class RemoveHiddenPairs:

    def __init__(self, sudoku: Sudoku, logging = False):
        self.sudoku = sudoku
        self.logging = logging

    def run(self):
        removed = False
        removed |= self.removeSectionsHiddenPairs(self.sudoku.getRows())
        removed |= self.removeSectionsHiddenPairs(self.sudoku.getColumns())
        removed |= self.removeSectionsHiddenPairs(self.sudoku.getBlocks())
        return removed

    def removeSectionsHiddenPairs(self, sections:List[Section]):
        removed = False

        for section in sections:
            removed |= self.__removeSectionHiddenPairs(section)

        return removed

    # Remove logic for row and column means removal from block.
    def __removeSectionHiddenPairs(self, section:Section):
        removed = False

        hintDict:dict[int, set[Cell]] = dict()

        for hint in section.allHints():
            hintDict.update({hint: set()})

        for cell in section:
            for hint in cell.hints:
                hintDict.get(hint).add(cell)
        
        for uniqueHintPairs in list(
            k for k,_ in groupby(
                sorted(
                    sorted(x) for x in list(product(section.allHints(), section.allHints())) if x[0] != x[1]
                )
            )
        ):
            hintA = uniqueHintPairs[0]
            hintB = uniqueHintPairs[1]

            if (len(hintDict[hintA]) != 2 or len(hintDict[hintB]) != 2): continue

            # If the sets dont differ, then this is a pair. All such, all other hints that
            # are not A or B should be removed from both cells.
            if (len(hintDict[hintA].symmetric_difference(hintDict[hintB])) == 0):

                # All cells with this pair
                for cell in hintDict[hintA].union(hintDict[hintB]):
                    hints = deepcopy(cell.hints)
                    hints.remove(hintA)
                    hints.remove(hintB)
                    cell.removeHints(hints, self.__class__.__name__, self.logging)
                    removed = True
            
        return removed
