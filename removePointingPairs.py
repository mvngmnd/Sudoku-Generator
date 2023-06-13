from typing import List

from sudoku import Sudoku, Section, Cell

# Removes pointing pairs.
# 
# If a hint is only present in two cells for a given section, it cant be in other applicable sections.

class RemovePointingPairs:

    def __init__(self, sudoku: Sudoku, logging = False):
        self.sudoku = sudoku
        self.logging = logging

    def run(self):
        removed = False
        removed |= self.removeSectionsPointingPairs(self.sudoku.getRows())
        removed |= self.removeSectionsPointingPairs(self.sudoku.getColumns())
        removed |= self.removeBlocksPointingPairs(self.sudoku.getBlocks())
        return removed

    def removeSectionsPointingPairs(self, sections:List[Section]):
        removed = False

        for section in sections:
            removed |= self.__removeSectionPointingPairs(section)

        return removed

    def removeBlocksPointingPairs(self, blocks:List[Section]):
        removed = False

        for block in blocks:
            removed |= self.__removeBlockPointingPairs(block)

        return removed

    # Remove logic for row and column means removal from block.
    def __removeSectionPointingPairs(self, section:Section):
        removed = False

        foundDict:dict[int, List[Cell]] = dict()

        for hint in section.allHints():
            cellsFound:List[Cell] = list()

            for cell in section:
                if (cell.hasHint(hint)):
                    cellsFound.append(cell)

            if (len(cellsFound) == 2):
                foundDict.update({hint: cellsFound})

        for found in foundDict:
            cells = foundDict[found]

            # If the cells have the same block, then this block has
            # a pair that cant be in the rest of the block.
            if cells[0].block == cells[1].block:
                block = self.sudoku.getBlock(cells[0].block)
                for cell in block:
                    if cell not in [cells[0], cells[1]]:
                        cell.removeHint(found, self.__class__.__name__, self.logging)
                        removed = True
        
        return removed

    # Remove logic for blocks means removal from row and column.
    def __removeBlockPointingPairs(self, block:Section):
        removed = False

        foundDict:dict[int, List[Cell]] = dict()

        for hint in block.allHints():
            cellsFound:List[Cell] = list()

            for cell in block:
                if (cell.hasHint(hint)):
                    cellsFound.append(cell)

            if (len(cellsFound) == 2):
                foundDict.update({hint: cellsFound})

        for found in foundDict:
            cells = foundDict[found]

            # If the cells have the same row, then this row has
            # a pair that cant be in the rest of the row.
            if cells[0].row == cells[1].row:
                row = cells[0].getRow()
                for cell in row:
                    if cell not in [cells[0], cells[1]]:
                        cell.removeHint(found, self.__class__.__name__, self.logging)
                        removed = True

            # If the cells have the same column, then this column has
            # a pair that cant be in the rest of the column.
            if cells[0].column == cells[1].column:
                column = cells[0].getColumn()
                for cell in column:
                    if cell not in [cells[0], cells[1]]:
                        cell.removeHint(found, self.__class__.__name__, self.logging)
                        removed = True
        
        return removed
