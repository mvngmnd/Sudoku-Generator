from typing import List
from sudoku import Sudoku, Cell

# Removes naked subsets.
# 
# For instance, if {2,7} is present twice in a region
# remove 2,7 from the other cells hints, as this is a 2,7 pair.
#
# Likewise, if {1,3,6} is present three times in a region
# remove 1,3,6 from the other cells hints, as this is a 1,3,6 triple.

class RemoveNakedSubsets:

    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku

    def run(self):
        removed = False
        removed |= self.removeRegionsNakedSubsets(self.sudoku.getBlocks())
        removed |= self.removeRegionsNakedSubsets(self.sudoku.getRows())
        removed |= self.removeRegionsNakedSubsets(self.sudoku.getColumns())
        return removed

    def removeRegionsNakedSubsets(self, regions):
        removed = False

        for region in regions:
            removed |= self.__removeRegionNakedSubsets(region)

        return removed

    def __removeRegionNakedSubsets(self, section: List[Cell]):
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
                    cell.removeHint(hint)

        return removedHint
