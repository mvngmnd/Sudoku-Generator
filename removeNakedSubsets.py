from typing import List

from sudoku import Sudoku, Cell

# Removes naked subsets.
# 
# For instance, if {2,7} is present twice in a section
# remove 2,7 from the other cells hints, as this is a 2,7 pair.
#
# Likewise, if {1,3,6} is present three times in a section
# remove 1,3,6 from the other cells hints, as this is a 1,3,6 triple.

class RemoveNakedSubsets:

    def __init__(self, sudoku: Sudoku, logging = False):
        self.sudoku = sudoku
        self.logging = logging

    def run(self):
        removed = False
        removed |= self.removeSectionsNakedSubsets(self.sudoku.getRows())
        removed |= self.removeSectionsNakedSubsets(self.sudoku.getColumns())
        removed |= self.removeSectionsNakedSubsets(self.sudoku.getBlocks())
        return removed

    def removeSectionsNakedSubsets(self, sections):
        removed = False

        for section in sections:
            removed |= self.__removeSectionNakedSubsets(section)

        return removed

    def __removeSectionNakedSubsets(self, section: List[Cell]):
        hintsFound = []
        removedHint = False

        for i in range(len(section)):
            innerHint = []
            cell = section[i]
            if (cell.solved or len(cell.hints) == 0): continue

            # Does anywhere else have the same hints?
            for ii in range(len(section)):
                # Same section or hints already found (the second time around)
                if (i == ii or section[ii].solved): continue
                if (set(section[ii].hints) == set(cell.hints)):
                    innerHint.append((cell.hints))

            # A hint is only unique if there are the same number present.
            # IE if {2,7} matched above once, add it.
            # IE if {1,3,6} matches twice, add it.

            for hint in [x for x in innerHint if innerHint.count(x) == len(x)-1]:
                if (not hintsFound.__contains__(hint)):
                    hintsFound.append(hint)
        
        if (len(hintsFound) == 0): return removedHint

        for hintFound in hintsFound:
            hintSet = set(hintFound)
            for cell in section:
                if (cell.hints == hintSet or cell.solved): continue
                for hint in hintSet:
                    cell.removeHint(hint, self.__class__.__name__, self.logging)
                    removedHint = True

        return removedHint
