#################################################
# TP V.1
#
# Your name: Jessie Fan
# Your andrew id: jessief
#################################################

import math, os, string

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

#^^ header from hw10

#################################################
# time log
#################################################

# 11/13
# ~9am - 11:30am
# ~1:30pm - 


'''
ok so i wanted to do a ghost game based on a google doodle
would involve
- different classes of characters 
    - that you have to type their name or like a spell to get rid of them 
    - if they hit you then you lose a life
    - ig you'll have 3 lives
    - they come at different speeds and might have different quirks
        - the can go through walls?
        - maybe like a zig-zag motion?
        - random generation (from the edges of the screen)
        - oh track the mc; where it's going change as the mc moves
            - how do i do this??
    - I think one of them should have like a random spell that you type to get rid of
    - or like randomly circulate among like 3 different ones

concept idea:
- maybe like escape the nightmare
- background randomly chooses from like a list of images (a very long list too)
- so like yeah a lot of different places you could be
- and then the characters would be like pretty random of like what you would have in a dream

- ideas for characters:
    - danny devito
    - andrew carnegie
        - type my heart is in the work to make him go away lol

- levels
    - as levels progress, different characters are introduced?
    - the amount and speed of the characters increase
    - the levels are like randomly generated
        - would have like obstacles in the way 
        - can make classes for different types of obstacles
            - i think they would all be like pluffy cloud type things, but like different shapes
            - or maybe make them a single block but like in the code you randomly generate like putting them together
            - can i give them like a certain transparency so that the characters that go through them look like they're going through them
        - so like they're an image that looks nice
        - and they take up like certain squares on the board and can be positioned certain ways
            - *** need to make board (rows and columns)
        - have to make sure that there's still a path that the mc can take to get to the end
            - generate next level with ***backtracking*** to make sure it's possible
        - mc must collect certain number of items in the path before door is unlocked and they can go to next level
            - ***animation*** of door rising?? when level passed??
        - these pieces will be randomly generated (similar to food in snake game, but probably will have multiple pieces on board at once)
        - and ofc mc has to like stay alive 
        - keep track of high score
    - idt i can do like an infinite number of levels (I mean like hypothetically it could get like faster and faster)
    
    (OH I HAVE TO KEEP TRACK OF LEVELS AND MAYBE I CAN USE IT AS A FUNCTION OF LIKE SPEED 
    AND WHEN LEVEL >= WHATEVER, THEN CERTAIN CHARACTERS CAN BE GENERATED)

-mc (class)
    - keep track of: lives
    - how do i keep track of high score??

- how to do the type box and like inputs
    - should probably do like a bar at the bottom 
    - how do i like animate it so it matches what you type
    - or like how do i make the inputs look nice
    - so it doesn't like ask for input and then process and then ask for input
    - i want like one box that you can type into....

    - maybe like have a box and a timer and like when you press a key it goes into the box
    - or like updates a string/list that goes into the box
    - and like when hit enter it makes a new list (so like 2d list)
    - and when checking the thingy to see if it matches the spell

- how many levels??
- high score? --> how will points be tracked
    - probably should just do by level

* should decide on the theme of this game --> 
like what are the characters you're trying to escape from
where is the MC located
who is the MC??

should it all be in one animation thing?

*** i think the way you keep score (i'm not going to keep high score even when you close the window)
is to just like not have it reset when the game ends and restarts (like it doesn't reset back to zero... )
so might have to have a separate app started function

*** is the way to make everything work together is like it's all run in one animation thing
but like it's broken up into a lot of different like redraws and app started etc. 
is this top down?

*** how do i have it so that the mc can't walk into objects
'''

# this needs to go after appStarted (probably)
class mc(object):
    def __init__(self):
        self.lives = 3
        self.x = app.width/2
        self.y = app.height/2

# based on snake from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#exampleSnake

from cmu_112_graphics import *
import random

def appStarted(app):
    app.rows = 10
    app.cols = 10
    app.margin = 5 # margin around grid
    app.timerDelay = 250
    
    #initSnakeAndFood(app)
    initTextBox(app)
    #app.waitingForFirstKeyPress = True

'''
def initSnakeAndFood(app):
    app.snake = [(0,0)]
    app.direction = (0, +1) # (drow, dcol)
    placeFood(app)
    app.gameOver = False
'''

def initTextBox(app):
    app.text = [[]]

# getCellBounds from grid-demo.py
def getCellBounds(app, row, col):
    # aka 'modelToView'
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    x0 = app.margin + gridWidth * col / app.cols
    x1 = app.margin + gridWidth * (col+1) / app.cols
    y0 = app.margin + gridHeight * row / app.rows
    y1 = app.margin + gridHeight * (row+1) / app.rows
    return (x0, y0, x1, y1)

def keyPressed(app, event):
    #if (app.waitingForFirstKeyPress):
        #app.waitingForFirstKeyPress = False
    #else:
        # like makes a list of the letters
        # and is a 2d list; so a list of the words
        if event.key == "Enter":
            # adds a new list for the next word
            app.text.append([])
        elif event.key in string.printable:
            app.text[-1].append(event.key)

        # can you turn lists to strings?
        # yes you can! with "".join(whateverlistyouwant)
    
    '''
    elif (event.key == 'r'):
        initSnakeAndFood(app)
    elif app.gameOver:
        return
    elif (event.key == 'Up'):      app.direction = (-1, 0)
    elif (event.key == 'Down'):  app.direction = (+1, 0)
    elif (event.key == 'Left'):  app.direction = (0, -1)
    elif (event.key == 'Right'): app.direction = (0, +1)
    # elif (event.key == 's'):
        # this was only here for debugging, before we turned on the timer
        # takeStep(app)
    '''

# ooo we need to do work here.... or do i?
def timerFired(app):
    if app.gameOver or app.waitingForFirstKeyPress: return
    takeStep(app)

# edit this
'''
def takeStep(app):
    (drow, dcol) = app.direction
    (headRow, headCol) = app.snake[0]
    (newRow, newCol) = (headRow+drow, headCol+dcol)
    if ((newRow < 0) or (newRow >= app.rows) or
        (newCol < 0) or (newCol >= app.cols) or
        ((newRow, newCol) in app.snake)):
        app.gameOver = True
    else:
        app.snake.insert(0, (newRow, newCol))
        if (app.foodPosition == (newRow, newCol)):
            placeFood(app)
        else:
            # didn't eat, so remove old tail (slither forward)
            app.snake.pop()

def placeFood(app):
    # Keep trying random positions until we find one that is not in
    # the snake. Note: there are more sophisticated ways to do this.
    while True:
        row = random.randint(0, app.rows-1)
        col = random.randint(0, app.cols-1)
        if (row,col) not in app.snake:
            app.foodPosition = (row, col)
            return
'''

def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill='white')

'''
def drawSnake(app, canvas):
    for (row, col) in app.snake:
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_oval(x0, y0, x1, y1, fill='blue')

def drawFood(app, canvas):
    if (app.foodPosition != None):
        (row, col) = app.foodPosition
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_oval(x0, y0, x1, y1, fill='green')

def drawGameOver(app, canvas):
    if (app.gameOver):
        canvas.create_text(app.width/2, app.height/2, text='Game over!',
                           font='Arial 26 bold')
        canvas.create_text(app.width/2, app.height/2+40,
                           text='Press r to restart!',
                           font='Arial 26 bold')
'''

# i'll need to tinker with the timer and the typing
# and key press to
# and i need to make lists to be saved to appStarted

def drawTextBox(app, canvas):
    if not app.waitingForFirstKeyPress:
        # make the 
        canvas.create_rectangle

def redrawAll(app, canvas):
    
    
    #if (app.waitingForFirstKeyPress):
        # change this!! (make the opening screen pretty?)
        #canvas.create_text(app.width/2, app.height/2,
                           text='Press any key to start!',
                           font='Arial 26 bold')
    #else:
        #drawBoard(app, canvas)
        #drawSnake(app, canvas)
        #drawFood(app, canvas)
        #drawGameOver(app, canvas)

runApp(width=400, height=400)
