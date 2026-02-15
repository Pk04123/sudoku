from cmu_graphics import *
import random
import copy
import math
import itertools

class State:
    def __init__(self, board):
        self.board = copy.deepcopy(board)
        self.legals = self.legalsMaker()
        self.manualLegals = copy.deepcopy(self.legals)
        self.immutableValues = self.immutableValueMaker()
        self.lowestLegalCount = 1
        self.usedCombis = set()
    
    def legalsMaker(self):
        legalsList = [[0] * 9 for _ in range(9)]
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                cellLegals = self.getLegals(row, col)
                legalsList[row][col] = cellLegals
        return legalsList

    def getLegals(self, row, col):
        colSet = self.colMaker(row, col)
        rowSet = set(self.board[row])
        blockSet = self.blockMaker(row, col)
        allVals = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        legals = allVals - (colSet | rowSet | blockSet)
        return legals
    
    def colMaker(self, row, col):
        res = set()
        for row in range(len(self.board)):
            res.add(self.board[row][col])
        return res
    
    def blockMaker(self, row, col):
        startRow = (row // 3) * 3
        startCol = (col // 3) * 3
        endRow = startRow + 2
        endCol = startCol + 2
        res = set()
        for row in range(startRow, endRow + 1):
            for col in range(startCol, endCol + 1):
                val = self.board[row][col]
                if val != 0:
                    res.add(val)
        return res
    
    def immutableValueMaker(self):
        res = []
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                val = self.board[row][col]
                if val != 0:
                    res.append((row, col))
        return res
    
    def makeMove(self, num, row, col):
        if (row, col) in app.state.immutableValues:
            app.notification = 'Cannot change cell!' 
            return
        
        self.board[row][col] = num
        if (row, col) == app.hintCell:
            app.hintCell = None
        if (row, col) in app.invalids:
            app.invalids.remove((row, col))
        if num in self.legals[row][col]:
            self.deleteLegals(num, row, col)
        else:
            app.notification = 'Invalid Value!'
            app.invalids.add((row, col))

    def deleteLegals(self, num, row, col):
        #update cell
        self.legals[row][col].remove(num)

        #we do not need to check the current cell for each of these
        # because that has already been updated

        #update row
        for colIdx in range(len(self.board[0])):
            if num in self.legals[row][colIdx]:
                self.legals[row][colIdx].remove(num)

        #update column
        for rowIdx in range(len(self.board)):
            if num in self.legals[rowIdx][col]:
                self.legals[rowIdx][col].remove(num)

        #update block
        startRow = (row // 3) * 3
        startCol = (col // 3) * 3
        endRow = startRow + 2
        endCol = startCol + 2
        for rowIdx in range(startRow, endRow + 1):
            for colIdx in range(startCol, endCol + 1):
                if num in self.legals[rowIdx][colIdx]:
                    self.legals[rowIdx][colIdx].remove(num)

    def deleteValue(self, row, col):
        #cell should not be immutable
        if (row, col) in app.state.immutableValues:
            app.notification = 'Cannot change cell!' 
            return
        
        self.board[row][col] = 0
        if (row, col) in app.invalids:
            app.invalids.remove((row, col))
    
        self.addLegals(row, col)

    def addLegals(self, row, col):
        #update row legals
        for colIdx in range(len(self.board[0])):
            cellLegals = self.getLegals(row, colIdx)
            self.legals[row][colIdx] = cellLegals

        #update column legals
        for rowIdx in range(len(self.board)):
            cellLegals = self.getLegals(rowIdx, col)
            self.legals[rowIdx][col] = cellLegals

        #update block legals
        startRow = (row // 3) * 3
        startCol = (col // 3) * 3
        endRow = startRow + 2
        endCol = startCol + 2
        for rowIdx in range(startRow, endRow + 1):
            for colIdx in range(startCol, endCol + 1):
                cellLegals = self.getLegals(rowIdx, colIdx)
                self.legals[rowIdx][colIdx] = cellLegals

    def getHintCell(self):
        for row in range(app.rows):
            for col in range(app.cols):
                if self.board[row][col] == 0 and len(self.legals[row][col]) == 1:
                    return (row, col)
        return None
    
    def manuallyUpdateLegals(self, row, col, key):
        if key == '!':
            if 1 not in self.manualLegals[row][col]:
                self.manualLegals[row][col].add(1)
            else:
                self.manualLegals[row][col].remove(1)
        elif key == '@':
            if 2 not in self.manualLegals[row][col]:
                self.manualLegals[row][col].add(2)
            else:
                self.manualLegals[row][col].remove(2)
        elif key == '#':
            if 3 not in self.manualLegals[row][col]:
                self.manualLegals[row][col].add(3)
            else:
                self.manualLegals[row][col].remove(3)
        elif key == '$':
            if 4 not in self.manualLegals[row][col]:
                self.manualLegals[row][col].add(4)
            else:
                self.manualLegals[row][col].remove(4)
        elif key == '%':
            if 5 not in self.manualLegals[row][col]:
                self.manualLegals[row][col].add(5)
            else:
                self.manualLegals[row][col].remove(5)
        elif key == '^':
            if 6 not in self.manualLegals[row][col]:
                self.manualLegals[row][col].add(6)
            else:
                self.manualLegals[row][col].remove(6)
        elif key == '&':
            if 7 not in self.manualLegals[row][col]:
                self.manualLegals[row][col].add(7)
            else:
                self.manualLegals[row][col].remove(7)
        elif key == '*':
            if 8 not in self.manualLegals[row][col]:
                self.manualLegals[row][col].add(8)
            else:
                self.manualLegals[row][col].remove(8)
        elif key == '(':
            if 9 not in self.manualLegals[row][col]:
                self.manualLegals[row][col].add(9)
            else:
                self.manualLegals[row][col].remove(9)

    #making iterations taken from https://www.cs.cmu.edu/~112/notes/tp-sudoku.html
    #watched these videos to understand how obvious pairs/triples work:
    #https://www.youtube.com/watch?v=MfH3hHi7qrw
    #https://www.youtube.com/watch?v=GLWG4BoeUYo
    #https://www.youtube.com/watch?v=xvwCFGvTSiM

    def blockIdxs(self, row, col):
        rowStart = (row // 3) * 3
        colStart = (col // 3) * 3
        block = []
        for i in range(rowStart, rowStart + 3):
            for j in range(colStart, colStart + 3):
                block.append((i, j))
        return block
    
    def getSols(self, iterable, n):
        for combi in iterable:
            if combi in self.usedCombis:
                continue
            checker = True
            #make the set union
            setUnion = set()
            
            for cell in combi:
                rIdx, cIdx = cell
                if self.board[rIdx][cIdx] != 0:
                    checker = False
                    break   #stop and check next thing
                setUnion = setUnion | self.legals[rIdx][cIdx]

            if checker == True and len(setUnion) == n:
                return (combi, setUnion)
            
        return None, None    #if all combination have been tried
            
    
    def getHintTuples(self):
        for n in range(2, 10):  #no of possible legals
            for rIdx in range(app.rows):
                for cIdx in range(app.cols):
                    #list of block indeces
                    block = self.blockIdxs(rIdx, cIdx)
                    iterable = tuple(itertools.combinations(block, n))
                    tempSol, legalsToRemove = self.getSols(iterable, n)
                    if tempSol != None:
                        return (tempSol, legalsToRemove, 'block')
                    
                    #list of row indeces
                    row = [(rIdx, i) for i in range (app.cols)]
                    iterable = tuple(itertools.combinations(row, n))
                    tempSol, legalsToRemove = self.getSols(iterable, n)
                    if tempSol != None:
                        return (tempSol, legalsToRemove, 'row')

                    #list of column indeces
                    col = [(i, cIdx) for i in range(app.rows)]
                    iterable = tuple(itertools.combinations(col, n))
                    tempSol, legalsToRemove= self.getSols(iterable, n)
                    if tempSol != None:
                        return (tempSol, legalsToRemove, 'col')

        return (None, None, None)
    
    def applyTupleHint(self):
        if app.whereFound == 'block':
            sRow = app.hintTuples[0][0]
            sCol = app.hintTuples[0][1]
            blockIds = self.blockIdxs(sRow, sCol)
            for rIdx, cIdx in blockIds:
                if self.board[rIdx][cIdx] != 0 or (rIdx, cIdx) in app.hintTuples:
                    continue
                self.legals[rIdx][cIdx] = self.legals[rIdx][cIdx].difference(app.legalsToRemove)   #set difference

        #things that have been common in blocks may also be in the same row or column!
        if (app.whereFound == 'row' or
            (len(app.hintTuples) == 2 and app.hintTuples[0][0] == app.hintTuples[1][0]) or
            (len(app.hintTuples) == 3 and app.hintTuples[0][0] == app.hintTuples[1][0] == app.hintTuples[2][0])):
            rIdx = app.hintTuples[0][0] #since all elements' rows are the same
            for cIdx in range(app.cols):
                if self.board[rIdx][cIdx] != 0 or (rIdx, cIdx) in app.hintTuples:
                    continue
                self.legals[rIdx][cIdx] = self.legals[rIdx][cIdx].difference(app.legalsToRemove)   #set difference
        
        if (app.whereFound == 'col' or
            (len(app.hintTuples) == 2 and app.hintTuples[0][1] == app.hintTuples[1][1]) or
            (len(app.hintTuples) == 3 and app.hintTuples[0][1] == app.hintTuples[1][1] == app.hintTuples[2][1])):
            cIdx = app.hintTuples[0][1] #since all elements' cols are the same
            for rIdx in range(app.rows):
                if self.board[rIdx][cIdx] != 0 or (rIdx, cIdx) in app.hintTuples:
                    continue
                self.legals[rIdx][cIdx] = self.legals[rIdx][cIdx].difference(app.legalsToRemove)   #set difference

        

        self.usedCombis.add(app.hintTuples) #we don't want this hint again
        app.hintTuples = None
        app.whereFound = None
        app.legalsToRemove = set()

    #backtracker and solver
    def solve(self, rows = 9, cols = 9):

        for rowIdx in range (rows):
            for colIdx in range(cols):
                #if there is some empty that doesn't have legal values, return None
                #there must have been a problem in the last, or previous values
                if (self.board[rowIdx][colIdx] == 0 and 
                    self.legals[rowIdx][colIdx] == set()):
                    return None
                
        self.lowestLegalCount = 1   #reset each time as legals get updated               
        newRow, newCol = self.findLowestLegalCell(rows, cols)

        #If there are no more empty cells, board must have been solved
        if newRow == None and newCol == None:
            return self.board
        
        for num in range(1, 10):
            legals = self.getLegals(newRow, newCol)
            if num in legals:
                self.board[newRow][newCol] = num
                self.deleteLegals(num, newRow, newCol)   #as values will get updated
                tempRes = self.solve()
                if tempRes == None:    #if there is no solution using  num
                    self.board[newRow][newCol] = 0   #reset value and try again
                    self.addLegals(newRow, newCol)     #reset legals
                else:               #if we don't return None, solution is valid
                    return self.board          
        return None
    
    #change to find cells with lowest number of legals
    def findLowestLegalCell(self, rows, cols):
        for rIdx in range(rows):
            for cIdx in range(cols):
                if (self.board[rIdx][cIdx] == 0 and    #don't edit a used cell
                    self.lowestLegalCount == len(self.legals[rIdx][cIdx])):
                    return rIdx, cIdx
                
        if self.lowestLegalCount < 9:
            self.lowestLegalCount += 1
            #search again with the lowestLegalValueIncremented
            return self.findLowestLegalCell(rows, cols)
       
        return None, None       #return None if all cells have been filled

class Button:
    def __init__(self, cx, cy, name, color, width = 100, height = 50):
        self.cx = cx
        self.cy = cy
        self.width = width
        self.height = height
        self.fill = color
        self.name = name

# Learnt about switching screens from Lecture and
# https://www.cs.cmu.edu/~112/notes/tp-resources.html
def Sudoku_onScreenActivate(app):
    app.rows = 9
    app.cols = 9
    app.boardLeft = 35
    app.boardTop = 100
    app.boardWidth = 450
    app.boardHeight = 450
    app.cellBorderWidth = 1
    app.stepsPerSecond = 4
    app.notification = None
    app.originalBoard = Sudoku_boardConverter()
    app.state = State(app.originalBoard)
    app.solvedState = State(app.originalBoard)
    app.solvedState.solve()
    print(app.solvedState.board)
    app.selectedCell = (0, 0)
    app.invalids = set()
    app.showHint = False
    app.hintCell = None
    app.hintTuples = None
    app.whereFound = None  #check if found in row, col, or block
    app.legalsToRemove = set()  #after we have found a tuple
    app.manualLegals = False
    app.autoPlay = False
    app.gameOver = False
    app.toggleLegalsModeButton = Button(app.width - 275, app.height - 290,
                                        'Toggle Legal Mode', 'tomato',
                                        width = 200, height = 50)
    app.viewHintButton = Button(app.width - 350, app.height - 165,
                                'View Hint', 'cyan')
    app.applyHintButton = Button(app.width - 200, app.height - 165, 
                                 'Apply Hint', 'yellow')
    app.solveButton = Button(app.width - 350, app.height - 90,
                             'Solve', 'lightGreen')
    app.resetButton = Button(app.width - 200, app.height - 90,
                             'Reset', 'red')
    app.buttons = (app.toggleLegalsModeButton, app.viewHintButton, app.applyHintButton, app.solveButton, app.resetButton)
    
    
    
def reset(app):
    app.selectedCell = (0, 0)
    app.state = State(app.originalBoard)
    app.notification = None
    app.invalids = set()
    app.showHint = False
    app.hintCell = None
    app.hintTuples = None
    app.whereFound = None
    app.legalsToRemove = set()
    app.manualLegals = False
    app.gameOver = False

#  reading the file (taken from 'Term Project Resources')
#  https://www.cs.cmu.edu/~112/notes/tp-resources.html
def Sudoku_readFile(path):
    with open(path, "rt") as f:
        return f.read()
    
#Generating Random number
def chooseBoard():
    if app.level == 'easy' or app.level == 'medium' or app.level == 'hard':
        boardIdx = random.randint(1, 50)
    else:
        boardIdx = random.randint(1, 25)

    if boardIdx <= 9:
        boardIdx = f'0{boardIdx}'
    else:
        boardIdx = str(boardIdx)

    path = f'SudokuBoards/boards/{app.level}-{boardIdx}.png.txt'
    board = Sudoku_readFile(path)
    return board

def Sudoku_boardConverter():
    board = chooseBoard()
    result = []
    board = board.splitlines()
    for row in range(len(board)):
        tempList = []
        for col in range(len(board[0])):
            char = board[row][col]
            if char.isdigit(): #since there are spaces too!
                tempList.append(int(char))
        result.append(tempList)
    return result

#Drawing the board and labels
def Sudoku_drawCellAndLabel(app, row, col):
    cellLeft, cellTop = Sudoku_getCellLeftTop(app, row, col)
    cellWidth, cellHeight = Sudoku_getCellSize(app)

    if app.showHint and (row, col) == app.hintCell:
        bg = 'lightGreen'
    elif (app.showHint and 
          app.hintTuples != None and (row, col) in app.hintTuples):
        bg = 'lightBlue'
    elif (row, col) == app.selectedCell:
        bg = 'pink'
    elif (row, col) in app.state.immutableValues:
        bg = 'gray'
    elif (row, col) in app.invalids:
        bg = 'red'
    else:
        bg = None

    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=bg, border='black',
             borderWidth=app.cellBorderWidth)
    
    value = app.state.board[row][col]
    #draw immutable cells
    if value != 0:  #only number for filled cell
        drawLabel(value, cellLeft + cellWidth / 2, cellTop + cellHeight / 2,
                  size = 20)
    #draw legals for empty cells  
    else:
        if app.manualLegals == False:
            legals = app.state.legals[row][col]
        else:
            legals = app.state.manualLegals[row][col]

        size = 10
        for num in legals:
            if num == 1:
                drawLabel(num, 
                          cellLeft + 7, cellTop + 10, 
                          size = size)
            elif num == 2:
                drawLabel(num, 
                          cellLeft + (cellWidth / 2), cellTop + 10, 
                          size = size)
            elif num == 3:
                drawLabel(num, 
                          cellLeft - 10 + cellWidth, cellTop + 10, 
                          size = size)
            elif num == 4:
                drawLabel(num, 
                          cellLeft + 7, cellTop + (cellHeight / 2), 
                          size = size)
            elif num == 5:
                drawLabel(num, 
                          cellLeft + (cellWidth / 2), cellTop + (cellHeight / 2), 
                          size = size)
            elif num == 6:
                drawLabel(num, 
                          cellLeft - 10 + cellWidth, cellTop + (cellHeight / 2), 
                          size = size)
            elif num == 7:
                drawLabel(num, 
                          cellLeft + 7, cellTop + cellHeight - 7, 
                          size = size)
            elif num  == 8:
                drawLabel(num, 
                          cellLeft + (cellWidth / 2), cellTop + cellHeight - 7, 
                          size = size)
            elif num == 9:
                drawLabel(num, 
                          cellLeft - 10 + cellWidth, cellTop + cellHeight - 7, 
                          size = size)
    
def Sudoku_getCellLeftTop(app, row, col):
    cellWidth, cellHeight = Sudoku_getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def Sudoku_getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def Sudoku_drawBoardBorder(app):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
             fill=None, border='black', borderWidth = 4 * app.cellBorderWidth)

def Sudoku_drawBoxBorder(app):
    cellWidth, cellHeight = Sudoku_getCellSize(app)
    for row in range(0, app.rows, 3):
        for col in range(0, app.cols, 3):
            drawRect(app.boardLeft + (col * cellWidth), 
                     app.boardTop + (row * cellHeight),
                     cellWidth * 3, cellHeight * 3, fill = None,
                     border = 'black', borderWidth = 2 * app.cellBorderWidth)

def Sudoku_redrawAll(app):
    #background
    drawRect(0, 0, app.width, app.height, fill = 'lightCyan')

    #labels
    drawLabel('SUDOKU', app.width / 2, 50, size = 40, bold = True, font = 'cursive')
    drawLabel('INSTRUCTIONS: ', app.width - 275, 120, size = 20)
    drawLabel('Press "View Hint" to view cells that',
              app.width - 275, 150, size = 16)
    drawLabel('have only one legal value (shown in green)',
              app.width - 275, 170, size = 16)
    drawLabel('Press "View Hint" to view cells that',
              app.width - 275, 200, size = 16)
    drawLabel('are obvious tuples (shown in blue)',
              app.width - 275, 220, size = 16)
    drawLabel('Press shift-[num] to update the legals with [num] ',
               app.width - 275, 250, size = 16)
    drawLabel('when using candidate mode',
               app.width - 275, 270, size = 16)
    drawLabel('Press shift-H to fill all the cells that have only one legal value',
               app.width - 275, 300, size = 16)
    drawLabel('Press shift-N to play a new game',
              app.width- 275, 330, size = 16)
    drawLabel('------------------------------',
              app.width - 275, 375, size = 30)
    if app.manualLegals == False:
        mode ='Automatic'
    else:
        mode = 'Candidate'
    drawLabel(f'Current legal mode: {mode}', app.width - 275, app.height - 235, size = 20)

    #buttons
    for button in app.buttons:
        drawRect(button.cx, button.cy, button.width, button.height,
                 fill = button.fill, border = 'black', align = 'center')
        drawLabel(button.name, button.cx, button.cy, size = 20)

    #board
    for row in range(app.rows):
        for col in range(app.cols):
            Sudoku_drawCellAndLabel(app, row, col)
    Sudoku_drawBoardBorder(app)
    Sudoku_drawBoxBorder(app)

    #notification
    if app.notification != None:
        if app.notification == 'You Won!':
            color = 'green'
        elif app.notification == 'Autoplay working...':
            color = 'blue'
        else:
            color = 'red'
        drawLabel(app.notification, 260, app.height - 100, size = 30, fill = color)

#Performing auto singleton fill
def Sudoku_onStep(app):
    if app.autoPlay == True:
        app.notification = 'Autoplay working...'
        tempCell = app.state.getHintCell()
        if tempCell != None:
            app.hintCell = tempCell
            x, y = app.hintCell
            num = app.state.legals[x][y].pop()  #we want to extract it
            app.state.legals[x][y].add(num) #but not delete it!
            app.state.makeMove(num, x, y)
            tempCell = app.state.getHintCell()
        else:
            app.autoPlay = False  #if there are no more hints, stop
            app.notification = 'No more singleton hints'
            app.showHint = False

    #to display notification if this solves the board
    if isSolved(app):
            app.notification = 'You Won!'
            app.gameOver = True

#Selecting cells (by both the mouse and keys)
def Sudoku_onKeyPress(app, key):
    app.notification = None

    if app.gameOver:
        return
    
    row, col = app.selectedCell

    if key in {'up', 'down', 'left', 'right'}:
        moveSelector(app, key)

    elif key.isdigit():
        app.state.makeMove(int(key), row, col)

    elif key in {'!', '@', '#', '$', '%', '^', '&', '*', '('}:
        if not app.manualLegals:
            app.notification = 'Toggle Legal Mode First!'
            return
        app.state.manuallyUpdateLegals(row, col, key)

    elif key == 'H':
        app.autoPlay = True
        #see onStep
    
    elif key == 'N':
        setActiveScreen('LevelSelector')

    elif key == 'backspace':
        app.state.deleteValue(row, col)    

    if isSolved(app):
        app.notification = 'You Won!'
        app.gameOver = True

def Sudoku_onMousePress(app, mouseX, mouseY):
    app.notification = None

    #if click is in the board
    if ((app.boardLeft <= mouseX <= app.boardLeft + app.boardWidth) and
        app.boardTop <= mouseY <= app.boardTop + app.boardHeight):
        row, col = getCell(app, mouseX, mouseY)
        if row != None and col != None:
            app.selectedCell = (row, col)
        return
    
    #elif click is in buttons
    for i in range(len(app.buttons)):
        button = app.buttons[i]
        left = button.cx - button.width / 2 
        right = button.cx + button.width / 2
        top = button.cy - button.height / 2
        bottom = button.cy + button.height / 2
        if left <= mouseX <= right and top <= mouseY <= bottom:
            #toggle legal mode
            if i == 0 and not app.gameOver:
                app.manualLegals = not app.manualLegals
                if app.manualLegals == True:
                    app.state.manualLegals = copy.deepcopy(app.state.legals)
                break
            
            #show hint
            elif i == 1 and not app.gameOver: 
                app.showHint = not app.showHint

                tempCell = app.state.getHintCell()
                if tempCell != None:
                    app.hintCell = tempCell
                    break
                
                tempTuples = app.state.getHintTuples()
                if tempTuples[0] != None:   #0th index contains the tuples
                    app.hintTuples, app.legalsToRemove, app.whereFound = tempTuples
                    break

                #if we do not have any hint
                app.notification = 'No more hints!' 
                break
                
            #apply hint
            elif i == 2 and not app.gameOver:
                if not app.showHint:
                    app.notification = 'View the hint first!'
                
                elif app.hintCell != None:
                    x, y = app.hintCell
                    num = app.state.legals[x][y].pop()  #we want to extract it
                    app.state.legals[x][y].add(num) #but not delete it!
                    app.state.makeMove(num, x, y)
                    app.showHint = False
                
                elif app.hintTuples != None:
                    app.state.applyTupleHint()
                    app.showHint = False
                
                break

            #solve board
            elif i == 3 and not app.gameOver:
                app.gameOver = True
                app.state = app.solvedState
                
            #reset app
            elif i == 4:
                reset(app)

    if isSolved(app):
        app.notification = 'You Won!'
        app.gameOver = True
        

def getCell(app, mouseX, mouseY):
    if (mouseX < app.boardLeft or mouseX > app.boardLeft + app.boardWidth or
        mouseY < app.boardTop or mouseY > app.boardTop + app.boardHeight or
        app.gameOver):
        return None, None

    cellWidth, cellHeight = Sudoku_getCellSize(app)
    col = math.floor((mouseX - app.boardLeft) / cellWidth)
    row = math.floor((mouseY - app.boardTop) / cellHeight)
    return row, col
        
def moveSelector(app, key):
    app.notification = None
    if key == 'up':
        drow = -1
        dcol = 0
        if isValidSelect(app, drow, dcol):
            currRow, currCol = app.selectedCell
            newRow = currRow + drow
            newCol = currCol + dcol
            app.selectedCell = (newRow, newCol)

    elif key == 'down':
        drow = 1
        dcol = 0
        if isValidSelect(app, drow, dcol):
            currRow, currCol = app.selectedCell
            newRow = currRow + drow
            newCol = currCol + dcol
            app.selectedCell = (newRow, newCol)

    elif key == 'left':
        drow = 0
        dcol = -1
        if isValidSelect(app, drow, dcol):
            currRow, currCol = app.selectedCell
            newRow = currRow + drow
            newCol = currCol + dcol
            app.selectedCell = (newRow, newCol)

    elif key == 'right':
        drow = 0
        dcol = 1
        if isValidSelect(app, drow, dcol):
            currRow, currCol = app.selectedCell
            newRow = currRow + drow
            newCol = currCol + dcol
            app.selectedCell = (newRow, newCol)

def isValidSelect(app, drow, dcol):
    currRow, currCol = app.selectedCell
    newRow = currRow + drow
    newCol = currCol + dcol
    if (newRow < 0 or newRow >= app.rows or newCol < 0 or newCol >= app.cols):
        return False
    return True

def isSolved(app):
    return app.state.board == app.solvedState.board