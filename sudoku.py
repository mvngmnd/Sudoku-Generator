from __future__ import annotations
from colorama import Fore, Style
from typing import List

class Cell:

    def __init__(self, value: int, sudoku: Sudoku, row: int, column: int):
        self.hints = set([1,2,3,4,5,6,7,8,9])
        self.value = 0
        self.solved = False
        self.intial = False

        self.sudoku = sudoku
        self.row = row
        self.column = column
        self.block = (row // 3) * 3 + column // 3

        if (value != 0):
            self.value = value
            self.hints = set([])
            self.solved = True
            self.intial = True

    def getBlock(self):
        return self.sudoku.getBlock(self.block)

    def getColumn(self):
        return self.sudoku.getColumn(self.column)

    def getRow(self):
        return self.sudoku.getRow(self.row)

    def setValue(self, value: int, method:str, logging = False):
        
        if (self.getBlock().containsValue(value)):
            raise KeyError("Block already contains value")

        if (self.getColumn().containsValue(value)):
            raise KeyError("Column already contains value")

        if (self.getRow().containsValue(value)):
            raise KeyError("Row already contains value")

        self.value = value
        self.hints = set([])
        self.solved = True
        self.sudoku.setHints()
        if (logging):
            print(f"{method}: (R{self.row+1},C{self.column+1}) solved as {value}")

    def hasHint(self, value: int):
        return self.hints.__contains__(value)

    def removeHint(self, value: int, method: str, logging = False):
        if (self.hints.__contains__(value)):
            if (logging):
                print(f"{method}: Hint {value} removed from {self.hints} (R{self.row+1},C{self.column+1})")
            self.hints.discard(value)
        
    def removeHints(self, values: List[int], method: str = "", logging = False):
        if (len(values) != 0):
            if (logging):
                print(f"{method}: Hints {values} removed from {self.hints} (R{self.row+1},C{self.column+1})")
            for value in values:
                self.removeHint(value, method, False)

class Section(List[Cell]):

    def __init__(self, iterable):
        super().__init__(item for item in iterable)

    def __setitem__(self, index, item):
        super().__setitem__(index, item)

    def insert(self, index, item):
        super().insert(index, item)

    def append(self, item):
        super().append(item)

    def extend(self, other):
        if isinstance(other, type(self)):
            super().extend(other)
        else:
            super().extend(item for item in other)

    def containsValue(self, value: int):
        for cell in self:
            if (cell.value == value):
                return True
        return False
    
    def allHints(self):
        hints = set()
        for cell in self:
            for hint in cell.hints:
                hints.add(hint)
        return hints


class Sudoku:
    
    def __init__(self, rows):
        self.rows:List[List[Cell]] = []
        for row in range(0, len(rows)):
            parsedCells = []
            for col in range(0, len(rows[row])):
                cell = Cell(rows[row][col], self, row, col)
                parsedCells.append(cell)
            self.rows.append(parsedCells)

    def setHints(self):
        sudoku = self
        for block in sudoku.getBlocks():
            vals = set(getValues(block))
            for cell in block:
                cell.removeHints(vals)
        
        for row in sudoku.getRows():
            vals = set(getValues(row))
            for cell in row:
                cell.removeHints(vals)

        for col in sudoku.getColumns():
            vals = set(getValues(col))
            for cell in col:
                cell.removeHints(vals)

    def isSolved(self):
        for row in self.getRows():
            for cell in row:
                if (not cell.solved):
                    return False
        return True

    def getCell(self, x: int, y: int):
        return self.rows[y][x]

    def print(self):
        self.printRows(self.rows)

    def printRows(self, rows: List[List[Cell]]):
        for i in range(0, len(rows)):
            row = rows[i]
            if (i % 3 == 0 and len(rows) > 3):
                print ("-"*(len(rows[0])*3-2))

            for i in range(0,len(row)):
                cell = row[i]
                if i == 0:
                    print("|", end= " ")
                if (cell.solved and not cell.intial):
                    print(f"{Fore.GREEN}{cell.value}{Style.RESET_ALL}", end = " ")
                elif (cell.value == 0):
                    print(f"{Fore.BLACK}{len(cell.hints)}{Style.RESET_ALL}", end = " ")
                else:
                    print(f"{cell.value}", end = " ")
                if (i % 3 == 2):
                    print("|", end= " ")
            print()
        if (len(rows) > 3):
            print("-"*(len(rows[0])*3-2))

    def getBlocks(self):
        blocks = []
        for i in range(0,9):
            blocks.append(self.getBlock(i))
        return blocks

    def getBlock(self, index: int):
        block = []

        startingRow = index // 3 * 3
        startingColumn = (index % 3) * 3

        for x in range(startingRow, startingRow + 3):
            row = self.getRow(x)
            cells = row[startingColumn: startingColumn+3]

            for cell in cells: block.append(cell)

        return Section(block)

    def getColumns(self):
        for i in range(0,9):
            yield self.getColumn(i)

    def getColumn(self, index: int):
        column:List[Cell] = []
        for row in self.rows:
            column.append(row[index])
        return Section(column)

    def getRows(self):
        for i in range(0,9):
            yield self.getRow(i)

    def getRow(self, index: int):
        return Section(self.rows[index])

    
def getValues(items):
    vals = []
    for item in items:
        if isinstance(item, Cell):
            vals.append(item.value)
        elif isinstance(item, list):
            for val in getValues(item):
                vals.append(val)
    return vals

def getHints(items):
    vals = []
    for item in items:
        if isinstance(item, Cell):
            hints = item.hints
            for hint in hints:
                vals.append(hint)
        elif isinstance(item, list):
            for val in getHints(item):
                hints = val.hints
                for hint in hints:
                    vals.append(hint)
    return vals