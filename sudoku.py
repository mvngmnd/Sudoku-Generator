import math
from colorama import Fore, Style
from typing import List

from datetime import datetime

class Cell:

    def __init__(self, value: int):
        self.hints = set([1,2,3,4,5,6,7,8,9])
        self.value = 0
        self.solved = False
        self.intial = False
        if (value != 0):
            self.setValue(value)
            self.intial = True

    def getValue(self):
        return self.value

    def setValue(self, value: int, printLog = False):
        self.value = value
        self.hints = set([])
        self.solved = True
        if (printLog):
            print("Guess made", datetime.now())

    def removeHint(self, value: int, printLog = False):
        if (self.hints.__contains__(value)):
            if (printLog):
                print(f"Hint {value} removed from {self.hints}", datetime.now())
            self.hints.discard(value)
        
    def removeHints(self, values: List[int], printLog = False):
        for value in values:
            self.removeHint(value, printLog)

class Sudoku:
    
    def __init__(self, rows):
        self.rows = []
        for row in rows:
            parsedCells = []
            for value in row:
                cell = Cell(value)
                parsedCells.append(cell)
            self.rows.append(parsedCells)

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
                    print(f"{Fore.BLACK}{cell.value}{Style.RESET_ALL}", end = " ")
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

        startingRow = math.floor(index/3) * 3
        startingColumn = (index % 3) * 3

        for x in range(startingRow, startingRow + 3):
            row = self.getRow(x)
            cells = row[startingColumn: startingColumn+3]

            for cell in cells: block.append(cell)

        return block

    def getColumns(self):
        columns = []
        for i in range(0,9):
            columns.append(self.getColumn(i))
        return columns

    def getColumn(self, index: int):
        column = []
        for row in self.rows:
            column.append(row[index])
        return column

    def getRows(self):
        return self.rows

    def getRow(self, index: int):
        return self.rows[index]

    
def getValues(items):
    vals = []
    for item in items:
        if isinstance(item, Cell):
            vals.append(item.getValue())
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