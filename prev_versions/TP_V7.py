#################################################
# TP V.7
#
# Your name: Jessie Fan
# Your andrew id: jessief
#################################################

import math, os, string, random
from cmu_112_graphics import *

#################################################
# TIMELOG:
# previously had 5ish hours for TP0

# TP1:
# oh writing the design thing i spent like ~30 min on 11/16 doing that ig
# 11/16 11:15pm - 11/17 1am
# 11/17 ~3pm - 4:30 pm
# 11/17 ~30 minutes on design
# 11/18 9am - 1pm
# 11/18 ~20 minutes on the design thing

# TP2:
# 11/22 9:30am - 1pm
# 11/22 2:00pm - 3:15 pm
# 11/22 7:30pm - 8:30pm
# 11/22 9:30pm - 11pm
# 11/23 9:30am - 1:15 pm
# 11/23 like 30 minutes at class

#################################################

# some bits based on snake from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#exampleSnake

#################################################
# INITIALIZE
#################################################

def appStarted(app):
    app.gameOver = False
    app.i = 0
    app.time = 0
    app.rows = 8
    app.cols = 8
    app.margin = 5 # margin around grid
    app.timerDelay = 250

    app.exit = ((app.rows - 2)//2, app.cols - 1)

    # keep track of points
    app.p = 0
    app.pointsNeeded = 10
    
    app.pointSize = 20
    app.mcSize = 20
    app.carnegieSize = 20
    # gets kinda funky when the num is bigger than 1/4 cells
    # can make it so that the num of rows and cols increase when obstacles get to be 1/4 the number of cells
    app.numObstacles = 10

    initChara(app)
    initTextBox(app)
    initObstacles(app, app.numObstacles)
    initPoints(app)
    initCarnegie(app)
    initTank(app)
    #app.waitingForFirstKeyPress = True

def initTextBox(app):
    app.text = [[],[]]

def initChara(app):
    app.chara = mc(app)
    app.start = (app.chara.row, app.chara.col)

def initPoints(app):
    app.points = []
    # places the initial 3 points
    for n in range(3): placePoint(app)

def initCarnegie(app):
    app.carnegies = []
    app.carnegie = carnegie(app)
    #app.graph = makeGraph(app)

def initTank(app):
    app.tanks = []
    app.tank = tank(app)

def initObstacles(app, num):
    app.obstacles = []
    app.obstaclesLocation = set()
    app.attempted = set()
    app.possible = set()
    
    # for now, make 10 obstacles
    while len(app.obstacles) < num:
        newRow = random.randint(0, app.rows - 3)
        newCol = random.randint(0, app.cols - 1)
        newObstacle = obstacle(app, newRow, newCol)

        if (newRow, newCol) not in app.attempted and (newRow, newCol) != app.start and (newRow, newCol) != app.exit:
            app.attempted.add((newRow, newCol))
            app.obstacles.append(newObstacle)
            app.obstaclesLocation.add((newRow, newCol))
            # if it's not possible to make a solution with these obstacles
            if not isSolution(app, app.chara.row, app.chara.col, []):
                # then remove obstacle
                app.obstacles.pop()
                app.obstaclesLocation.pop()
    
    isSolution1(app, app.chara.row, app.chara.col, set())
    print("possible", app.possible)
    print("obstacles", app.obstaclesLocation)
            # ig here is where find all the possible positions
    
#################################################
# CLASSES 
#################################################

class mc(object):
    def __init__(self, app):
        self.lives = 3
        
        self.x = app.margin + app.mcSize/2
        # fix this laterrrr
        self.y = ((4/5)*app.height)/2 + 20
        
        self.row = self.y//((app.height - 2*app.margin)//app.rows)
        self.col = self.x//((app.width - 2*app.margin)//app.cols)

# if I'm lazy, use random word generator and it's j a typing game w generic ghost
# goes away when you type 'my heart is in the work'
class carnegie(object):
    def __init__(self, app):
        # randomize starting position to any of the outer square with out an obstacle
        # for now will just start at the exit (because that def doesn't have a obstacle)
        self.x, self.y = (app.width, (2/3)*app.height)
        iy = random.randint(0, 1)
        Ly = [0, (4/5)*app.height]
        self.y = Ly[iy]
        self.x = random.randint(0, app.width)
    
    def move(self, app):
        step = 5
        directionx, directiony = (0,0)
        leastDistance = app.width
        (mcx, mcy) = app.chara.x, app.chara.y
        for dx, dy in [(0,1), (1,0), (-1,0), (0,-1), (1,1), (-1,-1)]:
            tempx, tempy = (self.x + step*dx),(self.y + step*dy)
            if distance(mcx, mcy, tempx, tempy) < leastDistance:
                leastDistance = distance(mcx, mcy, tempx, tempy)
                directionx, directiony = (dx, dy)
        self.x += step*directionx
        self.y += step*directiony

class tank(object):
    def __init__(self, app):
        # change to randomly generate later
        self.row, self.col = app.rows//2, app.cols//2
    
    def move(self, app, i):
        directions = BFS(app, Point(self.row, self.col), Point(app.chara.row, app.chara.col))
        print("directions", directions)
        print(app.i)
        if directions!= None and i < len(directions):
            print("is this printing")
            drow, dcol = directions[i]
            print("drow, dcol", drow, dcol)
            self.row += drow
            self.col += dcol

            # I have to adjust the list of directions

class obstacle(object):
    def __init__(self, app, row, col):
        # where it's located
        self.row = row
        self.col = col
        return

# largely based on (structure, which functions to use): 
# https://www.geeksforgeeks.org/shortest-path-in-a-binary-maze/

class Point(object):
    def __init__ (self, row, col):
        self.row = row
        self.col = col

class queueNode:
    def __init__(self, pt, directions):
        self.pt = pt
        self.directions = directions

def isValid(app, row, col):
    if (row,col) not in app.obstaclesLocation and 0<=row<app.rows*(4/5) and 0<=col<app.cols:
        return True
    return False

def BFS(app, src, target):
    visited = []
    queue = []

    source = queueNode((src), [])
    queue.append(source)

    while len(queue) > 0:
        curr = queue.pop(0)
        #print("directions1", curr.directions)

        # if we hit the target
        # here is the bug: dont' want directions just when we hit target... want directions when initialize
        if curr.pt.row == target.row and curr.pt.col == target.col:
            return curr.directions
        
        for drow, dcol in [(0,1), (1,0), (-1,0), (0,-1),(1,1),(-1,-1)]:
            row = curr.pt.row + drow
            col = curr.pt.col + dcol

            #print("row, col", row, col)
            #print("visited", visited)
            # and 0<=row<app.rows*(4/5) and 0<=col<app.cols
            # not in app.obstaclesLocation and
            if ((row, col) not in app.obstaclesLocation and (row,col) not in visited
                and 0<=row<app.rows*(4/5) and 0<=col<app.cols):
                #print("directions2", curr.directions)
                visited.append((row,col))
                adj = queueNode(Point(row,col), curr.directions + [(drow, dcol)])
                queue.append(adj)
                #print("directions3", adj.directions)
                #print("queue", queue)

#################################################
# OTHER
#################################################

def inPoint(app, x, y, size):
    for pointx, pointy in app.points:
        x0, x1, y0, y1 = pointx - app.pointSize/2, pointx + app.pointSize/2, pointy - app.pointSize/2, pointy + app.pointSize/2
        if (((x + size/2 >= x0 and x + size/2 <= x1) or (x - size/2 >= x0 and x - size/2 < x1))
            and ((y + size/2 >= y0 and y + size/2 <= y1) or (y - size/2 >= y0 and y - size/2 <= y1))):
            return (pointx, pointy)
    return False

def inMC(app, x, y, size):
    x0, y0, x1, y1 = app.chara.x - app.mcSize, app.chara.y - app.mcSize, app.chara.x + app.mcSize, app.chara.y + app.mcSize
    if (((x + size/2 >= x0 and x + size/2 < x1) or (x - size/2 >= x0 and x - size/2 < x1))
        and ((y + size/2 >= y0 and y + size/2 <= y1) or (y - size/2 >= y0 and y - size/2 <= y1))):
        return True
    return False

def inObstacle(app, x, y, size):
    for obstacleRow, obstacleCol in app.obstaclesLocation:
        x0, y0, x1, y1 = getCellBounds(app, obstacleRow, obstacleCol)
        if (((y + size/2 >= y0 and y + size/2 <= y1) or (y - size/2 >= y0 and y - size/2 <= y1)) and
               ((x + size/2 >= x0 and x + size/2 < x1) or (x - size/2 >= x0 and x - size/2 <= x1))) :
            return True
    return False

def inExit(app, x, y, size):
    # coordinates of the exit
    x0, y0, x1, y1 = app.width - app.margin - 20, app.height*(4/5)/2 - 20, app.width - app.margin, app.height*(4/5)/2 + 20
    print(x0, y0, x1, y1)
    print(x, y)
    if (((x + size/2 >= x0 and x + size/2 < x1) or (x - size/2 >= x0 and x - size/2 < x1))
        and ((y + size/2 >= y0 and y + size/2 <= y1) or (y - size/2 >= y0 and y - size/2 <= y1))):
        return True
    return False

# **** DON"T FORGET TO CHANGE ALL THE 2/3 or 4/5
# rn they're there because that's the ratio of the textbox

def inBounds(app, x, y, size):
    x0, y0, x1, y1 = app.margin, app.margin, app.width - app.margin, (4/5)*app.height
    if ((((x + size/2) >= x0) and ((x + size/2) < x1)) and (((x - size/2) >= x0) and ((x - size/2) < x1))
        and (((y + size/2) >= y0) and ((y + size/2) < y1)) and (((y - size/2) >= y0) and ((y - size/2) < y1))):
        return True
    return False

def newCarnegie(app):
    newCarnegie = carnegie(app)
    app.carnegies.append(newCarnegie)

def newTank(app):
    newTank = tank(app)
    app.tanks.append(newTank)

def getCoordinates(app, row, col):
    cellLength = app.width/app.cols
    x = col * cellLength + 0.5*cellLength
    y = row * cellLength + 0.5*cellLength
    return (x, y)

def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1 - y2)**2)**0.5

# use backtracking to see if there is a solution
# for obstacle placing
def isSolution(app, row, col, visited):
    if (row, col) == app.exit:
        return True
    else:
        for (drow, dcol) in [(-1,0), (1,0), (0,1), (0,-1)]:
            if (0 <= row + drow < (app.rows - 2) and 0 <= col + dcol < app.cols
                and (row + drow, col + dcol) not in visited 
                and (row + drow, col + dcol) not in app.obstaclesLocation):
                #move
                row = row + drow
                col = col + dcol
                visited.append((row, col))
                
                solution = isSolution(app, row, col, visited)
                if solution:
                    return True
                
                #undo move
                row = row - drow
                col = col - dcol
                visited.pop()
        return False

def isSolution1(app, row, col, visited):
    if (row, col) == app.exit:
        return True
    else:
        for (drow, dcol) in [(-1,0), (1,0), (0,1), (0,-1)]:
            if (0 <= row + drow < (app.rows - 2) and 0 <= col + dcol < app.cols
                and (row + drow, col + dcol) not in visited 
                and (row + drow, col + dcol) not in app.obstaclesLocation):
                #move
                row = row + drow
                col = col + dcol
                visited.add((row, col))
                
                solution = isSolution1(app, row, col, visited)
                if solution:
                    app.possible.add((row, col))
                    return True
                
                #undo move
                visited.remove((row, col))
                row = row - drow
                col = col - dcol
        return False

# based off of placeFood in snake case study
def placePoint(app):
    # Keep trying random positions until we find one that is not in
    # the snake. Note: there are more sophisticated ways to do this.
    while(len(app.points) < 3):
        x = random.randint(app.margin + app.pointSize/2, app.width - app.margin - app.pointSize/2)
        y = random.randint(app.margin + app.pointSize/2, (2/3)*app.height)
        #print(x, y)
        if (not inPoint(app, x, y, app.pointSize) and not inMC(app, x, y, app.pointSize)
            and not inObstacle(app, x, y, app.pointSize)):
            app.points.append((x, y))
            #print("points", app.points)

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

#################################################
# MOUSEPRESSED
#################################################

'''
for the level editor
makes an obstacle where the player clicks
ONLY if not on the home screen and in the level editor
'''

#################################################
# KEYPRESSED
#################################################

# later will have to make more functions 
# - to switch from home screen
# - to restart game
# - to go to level editor
# - to go to instructions screen
# each of these screens will get its own draw function

def moveChara(app, event):
    step = 10
    if (event.key == 'Up' and inBounds(app, app.chara.x, app.chara.y - step, app.mcSize)
        and not inObstacle(app, app.chara.x, app.chara.y - step, app.mcSize)):    
        app.chara.row = app.chara.y//((app.height - 2*app.margin)/app.rows)
        app.chara.y -= step
    elif (event.key == 'Down' and inBounds(app, app.chara.x, app.chara.y + step, app.mcSize)
            and not inObstacle(app, app.chara.x, app.chara.y + step, app.mcSize)):  
        app.chara.row = app.chara.y//((app.height - 2*app.margin)/app.rows)
        app.chara.y += step
    elif (event.key == 'Left' and inBounds(app, app.chara.x - step, app.chara.y, app.mcSize)
            and not inObstacle(app, app.chara.x - step, app.chara.y, app.mcSize)):  
        app.chara.col = app.chara.x//((app.width - 2*app.margin)/app.cols)
        app.chara.x -= step
    elif (event.key == 'Right' and inBounds(app, app.chara.x + step, app.chara.y, app.mcSize)
            and not inObstacle(app, app.chara.x + step, app.chara.y, app.mcSize)): 
        app.chara.col = app.chara.x//((app.width - 2*app.margin)/app.cols)
        app.chara.x += step

def typing(app, event):
    if event.key == "Enter":
    # adds a new list for the next word
        app.text.append([])
    elif event.key == "Delete" or event.key == "Backspace":
        if len(app.text[-1]) > 0:
            app.text[-1].pop()
    elif event.key == "Space":
        app.text[-1].append(" ")
    elif event.key in string.printable and not event.key.isdigit():
        app.text[-1].append(event.key)

def keyPressed(app, event):
    #if (app.waitingForFirstKeyPress):
        #app.waitingForFirstKeyPress = False
    #else:
    if event.key == "4":
        print("appstarted")
        appStarted(app)
    if not app.gameOver:
        typing(app, event)
        moveChara(app, event)

        # removes points if the mc is on that square
        if inPoint(app, app.chara.x, app.chara.y, app.mcSize) != False:
            (pointx, pointy) = inPoint(app, app.chara.x, app.chara.y, app.mcSize)
            app.points.remove((pointx, pointy))
            app.p += 1
        
        placePoint(app)
        # next level checks
        nextLevel(app)
        app.i = 0

#################################################
# TIMER
#################################################

# CHANGE TO DO FOR A DIFFERENT GHOST
def carnegieChecks(app):
    if app.time%50== 0:
        newCarnegie(app)
    for c in app.carnegies:
        c.move(app)
    if "".join(app.text[-1]) == "my heart is in the work" and len(app.carnegies) > 0:
        app.carnegies.pop(0)
        app.text.append([""])
        app.p += 2

def tankChecks(app):
    if app.time%50== 0:
        newTank(app)
    for c in app.tanks:
        if app.time%5 == 0:
            c.move(app, 0)
    if "".join(app.text[-1]) == "speedy" and len(app.tanks) > 0:
        app.tanks.pop(0)
        app.text.append([""])
        app.p += 1

def nextLevel(app):
    if app.p >= app.pointsNeeded and inExit(app, app.chara.x, app.chara.y, app.mcSize):
        app.numObstacles += 5
        app.pointsNeeded += 10
        if app.numObstacles > 0.25*(app.cols * (4/5)*app.rows):
            app.rows += 1
            app.cols += 1
        # not quite sure why i need the line below
        initChara(app)
        initObstacles(app, app.numObstacles)
        initPoints(app)
        # adjust other difficulties like speed and types of ghosts later
        
        # fix this later
        # have to place mc back in starting position
        app.chara.x = app.margin + app.mcSize/2
        app.chara.y = ((4/5)*app.height)/2 + 20
        #set back to 0 points
        app.p = 0
        #set ghosts back to none
        initCarnegie(app)

def timerFired(app):
    #if app.gameOver or app.waitingForFirstKeyPress: return
    if not app.gameOver: 
        app.time += 1
        carnegieChecks(app)
        tankChecks(app)

        # if the ghost runs into mc, lose a live and ghost disappears

        
        #*** do for a different ghost instead of carnegie
        for c in app.carnegies:
            x, y = c.x, c.y
            if inMC(app, x, y, app.carnegieSize):
                app.chara.lives -= 1
                app.carnegies.remove(c)
        
        for c in app.tanks:
            row,col = c.row, c.col
            if row == app.chara.row and col == app.chara.col:
                app.chara.lives -= 1
                app.tanks.remove(c)
        

        # game over if no more lives
        if app.chara.lives <= 0:
            app.gameOver = True

#################################################
# DRAWING
#################################################

def drawCarnegie(app, canvas):
    # he's just going to be a purple dot for now
    for carnegie in app.carnegies:
        canvas.create_oval(carnegie.x - app.carnegieSize/2, carnegie.y - app.carnegieSize/2,
                        carnegie.x + app.carnegieSize/2, carnegie.y + app.carnegieSize/2,
                        fill = "purple")
        canvas.create_text(carnegie.x, carnegie.y - app.carnegieSize/2, anchor = "s", 
                        text = "my heart is in the work")

def drawTank(app, canvas):
    # he's just going to be a purple dot for now
    for tank in app.tanks:
        x0, y0, x1, y1 = getCellBounds(app, tank.row, tank.col)
        canvas.create_oval(x0, y0, x1, y1,
                        fill = "red")
        canvas.create_text((x0 + x1)/2, y0, anchor = "s", 
                        text = "speedy")

# drawBoard from snake case study
def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1)

def drawTextBox(app, canvas):
    # make the textbox (height = the height of one square)
    cellHeight = (app.height - 2*app.margin)/app.rows
    canvas.create_rectangle(app.margin, app.height - app.margin - 2*cellHeight, 
                            app.width - app.margin, 
                            app.height - app.margin, fill = "light blue")
    
    # remember that there are [app.rows - 1] rows that the guy can move around

    word1, word2, word3, word4 = "", "", "", ""
    if len(app.text) >= 1:
        word1 = "".join(app.text[-1])
    if len(app.text) >= 2:
        word2 = "".join(app.text[-2])
    if len(app.text) >= 3:
        word3 = "".join(app.text[-3])
    if len(app.text) >= 4:
        word4 = "".join(app.text[-4])

    canvas.create_text(app.margin*2, app.height - app.margin, 
                       text = (word4 + "\n" + word3 + "\n" + word2 + "\n" + word1), 
                       anchor = "sw", font="Times 10")

def drawPoint(app, canvas):
    for i in range(len(app.points)):
        (x, y) = app.points[i]

        canvas.create_oval(x - app.pointSize/2, y - app.pointSize/2, 
                           x + app.pointSize/2, y + app.pointSize/2, fill='green')

def drawObstacle(app, canvas):
    for o in app.obstacles:
        (x0, y0, x1, y1) = getCellBounds(app, o.row, o.col)
        canvas.create_rectangle(x0, y0, x1, y1, fill='pink')

def drawPossible(app, canvas):
    for row,col in app.possible:
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_rectangle(x0, y0, x1, y1, fill='light green')

def redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawTextBox(app, canvas)
    drawObstacle(app, canvas)
    drawPossible(app, canvas)
    drawPoint(app, canvas)
    drawCarnegie(app, canvas)
    drawTank(app, canvas)

    # draw the mc (he's j a circle for now)
    canvas.create_oval(app.chara.x - app.mcSize/2, app.chara.y - app.mcSize/2, 
                       app.chara.x + app.mcSize/2, app.chara.y + app.mcSize/2, fill='blue')

    # prints how many points collected
    canvas.create_text(0,0, anchor = "nw", text = f'points: {app.p}')
    #prints how many lives mc has
    canvas.create_text(app.width - app.margin, 0, anchor = "ne", text = f'lives: {app.chara.lives}')
    #create exit
    canvas.create_rectangle(app.width - app.margin - 20, app.height*(4/5)/2 - 20, 
                            app.width - app.margin, app.height*(4/5)/2 + 20, fill = "yellow")


    # print game over
    if app.gameOver:
        canvas.create_text(app.width/2, app.height*(4/5)/2, text = "GAME OVER\npress 4 to try again")

runApp(width=600, height=600)

