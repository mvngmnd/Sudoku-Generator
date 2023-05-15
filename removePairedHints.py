from typing import List
from sudoku import Sudoku, Cell

# Used to remove paired hints. For instance, if {2,7} is present twice in a region
# remove 2 and 7 from the other cells hints, as this is a 2,7 pair.
class RemovePairedHints:

    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku

    def run(self):
        removed = False
        removed |= self.removeRegionsPairedHints(self.sudoku.getBlocks())
        removed |= self.removeRegionsPairedHints(self.sudoku.getRows())
        removed |= self.removeRegionsPairedHints(self.sudoku.getColumns())
        return removed

    def removeRegionsPairedHints(self, regions):
        removed = False

        for region in regions:
            removed |= self.__removeRegionPairedHints(region)

        return removed

    def __removeRegionPairedHints(self, section: List[Cell]):
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
            # IE if {2,7} matched above once, its in the list, so add it.
            # IE if {3,4,5} match above twice, its in the list, so add it.

            hints = [x for x in innerHint if innerHint.count(x) == len(x)-1]
            for hint in hints:
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
