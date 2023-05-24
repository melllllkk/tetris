#################################################
# Tetris!
#################################################

import math, copy, random

from cmu_112_graphics import *

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Functions for you to write
#################################################
def gameDimensions():
    row = 15
    cols = 10
    cellSize = 20 
    margin = 25
    return (row, cols, cellSize, margin)

def playTetris():
    (r, c, cs, m) = gameDimensions()
    width = 0
    height = 0
    for i in range(r):
        height += cs
    for j in range(c):
        width += cs 
    height += (2*m)
    width += (2*m)
    runApp(width = width, height = height)

# Seven "standard" pieces
def setupPieces():
    iPiece = [
        [  True,  True,  True,  True ]
    ]

    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]

    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]

    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]

    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]

    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]

    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]

    piecesList = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
    return piecesList

def appStarted(app):
    # board setup 
    (app.rows, app.cols, 
     app.cellSize, app.margin) = gameDimensions()
    app.board = []
    app.emptyColor = '#68738c'
    for x in range(app.rows):
        temp = []
        for y in range(app.cols):
            temp.append(app.emptyColor)
        app.board.append(temp)
    # app.board[0][0] = "#f26c4e" # top-left is red
    # app.board[0][app.cols-1] = "white" # top-right is white
    # app.board[app.rows-1][0] = "#81b07b" # bottom-left is green
    # app.board[app.rows-1][app.cols-1] = "#bfbfbf" # bottom-right is gra

    # tetris piece
    app.tetrisPieces = setupPieces()
    app.tetrisPieceColors = [ "#f26c4e", "#fce597", "#e68ae2", 
                              "#ffc7da", "#bcf2f5", "#81b07b", "#f5b562" ]
    app.fallingPiece = []
    app.fallingPieceColor = ''
    app.fallingPieceRow = 0
    app.fallingPieceCol = 0
    newFallingPiece(app)

    # functionalities 
    app.timerDelay = 250
    app.score = 0
    app.paused = False
    app.gameOver = False

def newFallingPiece(app):
    randomIndex = random.randint(0, 
    len(app.tetrisPieces) - 1)
    app.fallingPiece = app.tetrisPieces[randomIndex]
    app.fallingPieceColor = app.tetrisPieceColors[randomIndex]
    app.fallingPieceRow = 0
    numFallingPieceCols = len(app.fallingPiece[0]) // 2
    app.fallingPieceCol = (app.cols // 2) - numFallingPieceCols

def fallingPieceIsLegal(app):
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[row])):
            if app.fallingPiece[row][col]:
                currRow = app.fallingPieceRow + row 
                currCol = app.fallingPieceCol + col 
                if currRow < 0 or currRow >= app.rows:
                    return False
                if currCol < 0 or currCol >= app.cols:
                    return False
                if app.board[currRow][currCol] != app.emptyColor:
                    return False
    return True

def moveFallingPiece(app, drow, dcol):
    moveOccured = False
    app.fallingPieceRow = app.fallingPieceRow + drow
    app.fallingPieceCol = app.fallingPieceCol + dcol 
    if not fallingPieceIsLegal(app):
        moveOccured = True
    return moveOccured

def rotateFallingPiece(app):

    tempPiece = copy.deepcopy(app.fallingPiece)
    newPiece = []

    #rotate 
    for col in range(len(tempPiece[0])):
        temp = []
        for row in range(len(tempPiece)):
            maxIdx = len(tempPiece[0]) - 1
            temp.append(tempPiece[row][maxIdx - (1*col)])
        newPiece.append(temp) 
    
    # Old Row
    oldRow = app.fallingPieceRow
    oldNumRows = len(app.fallingPiece)
    #Old Col
    oldCol = app.fallingPieceCol
    oldNumCols = len(app.fallingPiece[0])

    app.fallingPiece = newPiece
    
    #New Row
    newNumRows = len(app.fallingPiece)
    newRow = oldRow + oldNumRows//2 - newNumRows//2
    app.fallingPieceRow = newRow
    #New Col
    newNumCols = len(app.fallingPiece[0])
    newCol = oldCol + oldNumCols//2 - newNumCols//2
    app.fallingPieceCol = newCol
    #Check if Legal
    if not fallingPieceIsLegal(app):
        app.fallingPiece = tempPiece
        app.fallingPieceRow = oldRow  
        app.fallingPieceCol = oldCol   

def placeFallingPiece(app):
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[row])):
            if app.fallingPiece[row][col]:
                bRow = (app.fallingPieceRow + row) - 1
                bCol = (app.fallingPieceCol + col)
                app.board[bRow][bCol] = app.fallingPieceColor
    removeFullRows(app)
    app.fallingPieceRow = 0

def isFullRow(app, row):
    for x in row:
        if x == app.emptyColor:
            return False
    return True
        
def removeFullRows(app):
    newBoard = []
    rowsRemoved = 0
    for row in app.board:
        if not isFullRow(app, row):
            newBoard.append(row)
        else:
            rowsRemoved += 1
            app.score += 1
    
    newRow = []
    for c in range(app.cols):
        newRow.append(app.emptyColor)
    while len(newBoard) <= (app.rows - 1):
        newBoard.insert(0, newRow)

    app.board = newBoard
    
def keyPressed(app, event):
    if not app.gameOver:
        #regenerate new piece
        # if event.key == "n" or event.key == "N":
        #     newFallingPiece(app)
        
        #control
        if event.key == "Up":
            rotateFallingPiece(app)
        if event.key == "Down":
            moveFallingPiece(app, +1, 0)
            if not fallingPieceIsLegal(app):
                moveFallingPiece(app, -1, 0)
        if event.key == "Left":
            moveFallingPiece(app, 0, -1)
            if not fallingPieceIsLegal(app):
                moveFallingPiece(app, 0, +1)
        if event.key == "Right":
            moveFallingPiece(app, 0, +1)
            if not fallingPieceIsLegal(app):
                moveFallingPiece(app, 0, -1)
        if event.key == "Space":
            while fallingPieceIsLegal(app):
                moveFallingPiece(app, +1, 0)
            moveFallingPiece(app, -1, 0)

        
        # debugging things 
        if event.key == "p" or event.key == "P":
            if not app.paused:
                app.paused = True
            else:
                app.paused = False
        if event.key == "s" or event.key == "S":
            if app.paused:
                moveFallingPiece(app, +1, 0)
                if not fallingPieceIsLegal(app):
                    moveFallingPiece(app, -1, 0)
    if event.key == "r" or event.key == "R":
        appStarted(app)

def timerFired(app):
    if not app.gameOver:
        if (not app.paused):
            if moveFallingPiece(app, +1, 0):
                placeFallingPiece(app)
                if not fallingPieceIsLegal(app):
                    app.gameOver = True
                    return
                newFallingPiece(app)
            if not fallingPieceIsLegal(app):
                moveFallingPiece(app, -1, 0)

def drawCell(app, canvas, row, col, color):
    x1 = (col)*20 + app.margin
    y1 = (row)*20 + app.margin
    x2 = (col + 1)*20 + app.margin
    y2 = (row + 1)*20 + app.margin
    canvas.create_rectangle(x1, y1, x2, y2,
                            fill = color, outline = '#5e5e5e',
                            width = 3)

def drawBoard(app, canvas):
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            drawCell(app, canvas, row, col, app.board[row][col])

def drawFallingPiece(app, canvas):
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[row])):
            if app.fallingPiece[row][col]:
                drawCell(app, canvas, app.fallingPieceRow + row,
                app.fallingPieceCol + col, app.fallingPieceColor)

def drawTextAndGameOver(app, canvas):
    #score
    canvas.create_text(app.width/2, 2, anchor = 'n',
                       text = f'Score: {app.score}',
                       font = "Comic\ Sans\ MS 15 bold",
                       fill = '#3b3c3d')
    
    if app.gameOver:
        x1 = app.margin
        y1 = 20 + app.margin
        x2 = (app.cols) * 20 + app.margin
        y2 = 80 + app.margin
        canvas.create_rectangle(x1, y1, x2, y2,
                                fill = "#bfbfbf", width = 2,
                                outline = "#4f4e4e") 
        y3 = (y1 + y2)/2
        canvas.create_text(app.width/2, y3,
                           text = "Game Over!",
                           fill = "black",
                           font = "Comic\ Sans\ MS 25 bold")

def redrawAll(app, canvas):
    canvas.create_rectangle(-1, -1, app.width, app.height, 
                            fill = '#edb574', width = 0)
    drawBoard(app, canvas)
    drawFallingPiece(app,canvas)
    drawTextAndGameOver(app, canvas)

#################################################
# main
#################################################

def main():
    playTetris()

if __name__ == '__main__':
    main()