#################################################
# TP V.12
#
# Your name: Jessie Fan
# Your andrew id: jessief
#################################################

import math, os, string, random
from cmu_112_graphics import *

#################################################
# TIMELOG:
# previously had 5ish hours for TP0

# TP1: --> 9
# oh writing the design thing i spent like ~30 min on 11/16 doing that ig
# 11/16 11:15pm - 11/17 1am
# 11/17 ~3pm - 4:30 pm
# 11/17 ~30 minutes on design
# 11/18 9am - 1pm
# 11/18 ~20 minutes on the design thing

# TP2: --> 12
# 11/22 9:30am - 1pm
# 11/22 2:00pm - 3:15 pm
# 11/22 7:30pm - 8:30pm
# 11/22 9:30pm - 11pm
# 11/23 9:30am - 1:15 pm
# 11/23 like 30 minutes at class

# TP3: --> 10
# 11/23 5:15pm - 5:45pm
# 11/25 11:45am - 1:30pm
# 11/29 9:00am - 1pm
# 11/29 2:30pm - 3:30pm
# 11/29 7:30pm - 8:45pm
# 11/29 9:30pm - 10:30pm
# 11/30 12:15am - 1:15am
# 11/30 9:00am - 1:15pm
# ~~ 30 minutes
# 11/30 3:00pm - 3:30pm
# 11/30 4:30pm - 6:45pm
# 11/30 7:45pm - 9:00pm
# ~~ 10 minutes on the video
# 12/1 1:00am - 

#################################################

# if the image/part of an image/sprite isn't cited, that's because I did it

# some bits based on snake from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#exampleSnake

#################################################
# INITIALIZE
#################################################

def appStarted(app):
    app.level = 1
    app.gameOver = True
    app.homeScreen = True
    app.instructions = False

    app.time = 0
    app.shipCounter = 0
    app.mcCounter = 0
    app.randoCounter = 0
    
    app.rows = 6
    app.cols = 6
    app.margin = 30 # margin around grid
    app.textboxHeight = 100
    app.gridHeight = app.height - app.textboxHeight - 2*app.margin

    # keep track of points
    app.p = 0
    app.pointsNeeded = 3
    
    # gets kinda funky when the num is bigger than 1/4 num of cells
    app.numObstacles = 6

    app.carnegieGenerationSpeed = 200
    app.tankSpeed = 25
    app.randoSpeed = 13

#################################################
# INITIALIZE : IMAGES
#################################################

    # Andrew Carnegie (1835-1919) American industrialist and humanitarian philanthropist, 1913. (Photo by APIC/Getty Images)
    # https://www.gettyimages.com/detail/news-photo/andrew-carnegie-american-industrialist-and-humanitarian-news-photo/112087977?adppopup=true
    app.imageCarnegie = app.loadImage('carnegie.png')
    # mouth of shockedCarnegie: https://www.clipartmax.com/middle/m2i8d3G6N4m2A0Z5_shocked-mouth-open-2-shocked-mouth/
    app.imageShockedCarnegie = app.loadImage('shockedcarnegie.png')
    # https://www.dreamstime.com/old-steel-texture-background-iron-metal-grunge-metallic-design-wall-pattern-plate-industrial-industry-aluminum-gray-sheet-rough-image153764686
    app.imageSteel = app.loadImage('steel.png')
    # https://www.cmu.edu/brand/brand-guidelines/visual-identity/colors.htm
    app.imagePlaid = app.loadImage('plaid.png')
    # https://www.123rf.com/photo_17932823_abandoned-old-factory-with-closed-door-and-windows.html
    app.imageDoor = app.loadImage('door.png')
    app.imageOpenDoor = app.loadImage('openDoor.png')
    # https://csengineermag.com/carbon-sequestration-in-cement-creates-significant-environmental-advances-in-new-construction/cement-floor-texture-concrete-floor-texture-use-for-background/
    app.imageFloor2 = app.loadImage('floor.png')
    app.instruction = app.loadImage('instructions.png')
    # font for "ESCAPE" from: https://www.dafont.com/abandon.font
    app.home = app.loadImage('home.png')
    
    # steamship: https://www.vectorstock.com/royalty-free-vector/steamship-vector-9944560
    # wave: https://pngimg.com/image/37191
    app.shipSprite = app.loadImage('shipSprite.png')
    app.sinkingSprite = app.loadImage('sinking.png')
    app.scribbleSprite = app.loadImage('scribbleSprite.png')
    # https://www.dreamstime.com/animation-fire-flame-explosion-sprite-game-design-vector-illustration-animations-flames-image105995344
    app.burningSprite = app.loadImage('burning.png')
    #https://stock.adobe.com/search?k=game+character+sprite&asset_id=184392243
    app.mcSprite = app.loadImage('mcSprite.png')

    initSize(app)
    initChara(app)
    initTextBox(app)
    initExit(app)
    initObstacles(app, app.numObstacles)
    initPoints(app)
    initCarnegie(app)
    initTank(app)
    initRando(app)

def initSize(app):
    app.cellSize = app.gridHeight/app.rows
    x1, y1, x2, y2 = getCellBounds(app, 0, 0)
    app.cellDiag = distance(x1, y1, x2, y2)
    
    # so every time the rows and cols increase and the cellSize decreases, 
    # all the elements also change size
    app.exitWidth = app.cellSize/10
    app.pointSize = int(app.cellSize/4)
    app.mcSize = int(app.cellSize/1.75)
    app.carnegieSize = int(app.cellSize/2)
    app.carnegiep = app.carnegieSize/600
    app.randoSize = app.cellSize/4

    # what to scale by
    app.shipp = app.steelp = app.cellSize/1000
    app.pointp = app.pointSize/1000
    app.doorp = app.exitWidth/100
    app.scribblep = app.pointSize/100
    app.mcp = app.mcSize/1000
    # used carnegieSize because I want it to be bigger than the rando
    app.burnp = app.carnegieSize/1000

    # scale all the images
    app.imageCarnegie2 = app.scaleImage(app.imageCarnegie, app.carnegiep)
    app.imageShockedCarnegie2 = app.scaleImage(app.imageShockedCarnegie, app.carnegiep)
    app.imageSteel2 = app.scaleImage(app.imageSteel, app.steelp)
    app.imagePlaid2 = app.scaleImage(app.imagePlaid, app.pointp)
    app.imageDoor2 = app.scaleImage(app.imageDoor, app.doorp)
    app.imageOpenDoor2 = app.scaleImage(app.imageOpenDoor, app.doorp)
    app.shipSprite2 = app.scaleImage(app.shipSprite, app.shipp)
    app.sinkingSprite2 = app.scaleImage(app.sinkingSprite, app.shipp)
    app.scribbleSprite2 = app.scaleImage(app.scribbleSprite, app.scribblep)
    app.burningSprite2 = app.scaleImage(app.burningSprite, app.burnp)
    app.mcSprite2 = app.scaleImage(app.mcSprite, app.mcp)
    
    # all the sprite stuff based on : https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#spritesheetsWithCropping
    app.shipSprites = []
    for i in range(3):
        sprite = app.shipSprite2.crop((app.cellSize*i, 0, app.cellSize*(i+1), app.cellSize))
        app.shipSprites.append(sprite)
    
    app.sinkingSpritez = []
    for i in range(6):
        sprite = app.sinkingSprite2.crop((app.cellSize*i, 0, app.cellSize*(i+1), app.cellSize))
        app.sinkingSpritez.append(sprite)

    app.scribbleSprites = []
    for i in range(4):
        sprite = app.scribbleSprite2.crop((app.pointSize*i, 0, app.pointSize*(i+1), app.pointSize))
        app.scribbleSprites.append(sprite)
    
    app.burningSpritez = []
    for i in range(7):
        sprite = app.burningSprite2.crop((app.carnegieSize*i, 0, app.carnegieSize*(i+1), app.carnegieSize))
        app.burningSpritez.append(sprite)
    
    app.mcSprites = []
    for i in range(8):
        sprite = app.mcSprite2.crop((app.mcSize*i, 0, app.mcSize*(i+1), app.mcSize))
        app.mcSprites.append(sprite)

def initExit(app):
    app.exit = ((app.rows - 1)//2, app.cols - 1)

def initTextBox(app):
    app.text = [[],[]]

def initChara(app):
    app.chara = mc(app)
    app.start = (app.chara.row, app.chara.col)
    print(app.start)

def initPoints(app):
    app.points = []
    # places the initial 3 points
    for n in range(3): placePoint(app)

def initCarnegie(app):
    app.carnegies = []
    # tracks coordinates to place collision animation
    app.oop = []
    # tracks which sprite each collision is on
    app.oopSprites = []

def initTank(app):
    app.tanks = []
    app.sinking = []
    app.sinkingSprites = []

def initRando(app):
    app.randos = []
    app.randWords = []
    app.burning = []
    app.burningSprites = []

def initObstacles(app, num):
    app.obstacles = []
    app.obstaclesLocation = set()
    app.attempted = set()
    
    while len(app.obstaclesLocation) < num:
        newRow = random.randint(0, app.rows - 1)
        newCol = random.randint(0, app.cols - 1)

        if (newRow, newCol) not in app.attempted and (newRow, newCol) != app.start and (newRow, newCol) != app.exit:
            app.attempted.add((newRow, newCol))
            app.obstaclesLocation.add((newRow, newCol))
            # if it's not possible to make a solution with these obstacles
            if not isSolution(app, app.chara.row, app.chara.col, []):
                # then remove obstacle
                app.obstaclesLocation.pop()
        
#################################################
# CLASSES 
#################################################

class mc(object):
    def __init__(self, app):
        self.lives = 5    
        # starts in left center cell  
        self.row, self.col = app.rows//2, 0
        x0, y0, x1, y1 = getCellBounds(app, self.row, self.col)
        self.y, self.x = (y1 + y0)/2, app.margin + app.mcSize/2   
        self.d = "W"

class carnegie(object):
    def __init__(self, app):
        # randomize starting position to any top or bottom edge
        iy = random.randint(0, 1)
        Ly = [app.margin + app.carnegieSize, app.gridHeight + app.margin - app.carnegieSize/2]
        self.y = Ly[iy]
        self.x = random.randint(app.margin, app.width - app.margin)
    
    def move(self, app):
        step = 5
        directionx, directiony = (0,0)
        leastDistance = app.width
        (mcx, mcy) = app.chara.x, app.chara.y
        # finds which direction will move the ghost closer to the target
        for dx, dy in [(0,1), (1,0), (-1,0), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)]:
            tempx, tempy = (self.x + step*dx),(self.y + step*dy)
            if distance(mcx, mcy, tempx, tempy) < leastDistance:
                leastDistance = distance(mcx, mcy, tempx, tempy)
                directionx, directiony = (dx, dy)
        self.x += step*directionx
        self.y += step*directiony

class tank(object):
    def __init__(self, app):
        self.row, self.col = app.rows//2, app.cols//2
        self.d = "E"
    
    def move(self, app, i):
        directions = BFS(app, Point(self.row, self.col), Point(app.chara.row, app.chara.col))
        if directions!= None and i < len(directions):
            drow, dcol = directions[i]
            self.row += drow
            self.col += dcol
            if (drow,dcol) == (0,1) or (drow,dcol) == (1,1) or (drow,dcol) == (-1,1):
                self.d = "E"
            elif (drow,dcol) == (0,-1) or (drow,dcol) == (-1,-1) or (drow,dcol) == (1,-1):
                self.d = "W"
            elif (drow,dcol) == (1,0):
                self.d = "S"
            elif (drow,dcol) == (-1,0):
                self.d = "N"

# largely based on : https://www.geeksforgeeks.org/shortest-path-in-a-binary-maze/
class Point(object):
    def __init__ (self, row, col):
        self.row = row
        self.col = col

class queueNode(object):
    def __init__(self, pt, directions):
        self.pt = pt
        self.directions = directions

def isValid(app, row, col):
    # if the ghost isn't in an obstacle's cell and not out of bounds
    if (row,col) not in app.obstaclesLocation and 0<=row<app.rows and 0<=col<app.cols:
        return True
    return False

def BFS(app, src, target):
    visited = []
    queue = []

    source = queueNode((src), [])
    queue.append(source)

    while len(queue) > 0:
        curr = queue.pop(0)
        # if reach the target
        if curr.pt.row == target.row and curr.pt.col == target.col:
            return curr.directions
        
        for drow, dcol in [(0,1), (1,0), (-1,0), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)]:
            row = curr.pt.row + drow
            col = curr.pt.col + dcol
            if ((row, col) not in app.obstaclesLocation and (row,col) not in visited
                and 0<=row<app.rows and 0<=col<app.cols):
                visited.append((row,col))
                adj = queueNode(Point(row,col), curr.directions + [(drow, dcol)])
                queue.append(adj)

class rando(object):
    def __init__(self, app):
        foundPlace = False
        while not foundPlace:
            iy = random.randint(0, 1)
            Ly = [app.margin + app.cellSize//2, app.gridHeight + app.margin - app.cellSize//2]
            y, x = Ly[iy], random.randint(0, app.cols - 1) * app.cellSize + app.cellSize//2
            if not inObstacle(app, x, y, app.randoSize):
                self.y = y
                self.x = x
                foundPlace = True
    
    def move(self, app, i):
        step = app.randoSize

        directions = astar(app, (self.x, self.y), (app.chara.x, app.chara.y))
        if directions != None and i < len(directions):
            dx, dy = directions[i]
            self.x += dx*step
            self.y += dy*step
        

# A* generally based off of: 
# https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
# https://www.geeksforgeeks.org/a-search-algorithm/

# this class heavily based from: https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
class Node(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.g = 0
        self.h = 0
        self.f = 0
    
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
    
    def __repr__(self):
        return f"({self.x}, {self.y})"

class qNode(object):
    def __init__(self, parent, node, directions):
        self.parent = parent
        self.node = node

        self.directions = directions
    
    def __eq__(self, other):
        return (self.node.x, self.node.y) == (other.node.x, other.node.y)

# src and target are x,y coordinates!
def astar(app, src, target):
    tx, ty = target
    sx, sy = src

    closed = []
    open = []

    step = app.randoSize

    start = qNode(None, Node(sx, sy), [])
    open.append(start)

    while len(open) > 0:
        leastF = 10000
        leastNode = None
        for qnode in open:
            if type(leastNode) != qNode or qnode.node.f < leastF:
                leastF = qnode.node.f
                leastNode = qnode
        q = leastNode
        open.remove(q)

        kids = []
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1)]:
            kiddy = None
            if (not inObstacle(app, q.node.x + dx*step, q.node.y + dy*step, app.randoSize) and
                inBounds(app, q.node.x + dx*step, q.node.y + dy*step, app.randoSize)):
                kiddy = qNode(None, Node(q.node.x + dx*step, q.node.y + dy*step), q.directions + [(dx, dy)])
            if type(kiddy) == qNode and kiddy not in closed:
                    kids.append(kiddy)
        #print("kids", kids)

        for kid in kids:
            # if reach target
            if inMC(app, kid.node.x, kid.node.y, app.randoSize):
                #print("directions", kid.directions)
                return kid.directions

            kid.node.g = q.node.g + distance(q.node.x, q.node.y, kid.node.x, kid.node.y)
            kid.node.h = diagDistance(app, tx, kid.node.x, ty, kid.node.y)
            kid.node.f = kid.node.g + kid.node.h
            if kid not in open:
                open.append(kid)
                kid.parent = q
            else:
                index = open.index(kid)
                # there's prolly something funky here
                if open[index].node.g < kid.node.g:
                    kid.parent = open[index]
                    kid.node.g = open[index].node.g + distance(open[index].node.x, open[index].node.y, kid.node.x, kid.node.y)
                    kid.node.f = kid.node.g + kid.node.h
        closed.append(q)
    return [(0,0)]

#################################################
# OTHER
#################################################

# incorrect because really it should be the point is in it (not it's in the point)
def inPoint(app, x, y, size):
    for pointx, pointy in app.points:
        x0, x1, y0, y1 = x - size/2, x + size/2, y - size/2, y + size/2
        if (((pointx + app.pointSize/2 >= x0 and pointx + app.pointSize/2 <= x1) or (pointx - app.pointSize/2 >= x0 and pointx - app.pointSize/2 < x1))
            and ((pointy + app.pointSize/2 >= y0 and pointy + app.pointSize/2 <= y1) or (pointy - app.pointSize/2 >= y0 and pointy - app.pointSize/2 <= y1))):
            return (pointx, pointy)
    return False

    '''
    for pointx, pointy in app.points:
        x0, x1, y0, y1 = pointx - app.pointSize/2, pointx + app.pointSize/2, pointy - app.pointSize/2, pointy + app.pointSize/2
        if (((x + size/2 >= x0 and x + size/2 <= x1) or (x - size/2 >= x0 and x - size/2 < x1))
            and ((y + size/2 >= y0 and y + size/2 <= y1) or (y - size/2 >= y0 and y - size/2 <= y1))):
            return (pointx, pointy)
    return False
    '''

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
    row, col = app.exit
    x0, y0, x1, y1 = getCellBounds(app, row, col)
    x0 = app.width - app.margin - app.exitWidth
    if (((x + size/2 >= x0 and x + size/2 < x1) or (x - size/2 >= x0 and x - size/2 < x1))
        and ((y + size/2 >= y0 and y + size/2 <= y1) or (y - size/2 >= y0 and y - size/2 <= y1))):
        return True
    return False

def inBounds(app, x, y, size):
    x0, y0, x1, y1 = app.margin, app.margin, app.width - app.margin, app.gridHeight + app.margin
    if ((((x + size/2) >= x0) and ((x + size/2) < x1)) and (((x - size/2) >= x0) and ((x - size/2) < x1))
        and (((y + size/2) >= y0) and ((y + size/2) < y1)) and (((y - size/2) >= y0) and ((y - size/2) < y1))):
        return True
    return False

def newWord():
    word = ""
    while len(word) < 6:
        newLetter = string.ascii_lowercase[random.randint(0,25)]
        word += newLetter
    return word

def newCarnegie(app):
    newCarnegie = carnegie(app)
    app.carnegies.append(newCarnegie)

def newTank(app):
    newTank = tank(app)
    app.tanks.append(newTank)

def newRando(app):
    newRando = rando(app)
    app.randos.append(newRando)
    app.randWords.append(newWord())

def getCoordinates(app, row, col):
    cellLength = app.width/app.cols
    x = col * cellLength + 0.5*cellLength
    y = row * cellLength + 0.5*cellLength
    return (x, y)

def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1 - y2)**2)**0.5

# from "2) Diagonal Distance" from : https://www.geeksforgeeks.org/a-search-algorithm/
def diagDistance(app, x1, y1, x2, y2):
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
 
    distance = app.cellSize*(dx + dy) + (app.cellDiag - 2 * app.cellSize)*min(dx, dy)
    return distance


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

# based off of placeFood in snake case study
def placePoint(app):
    while(len(app.points) < 3):
        x = random.randint(app.margin + app.pointSize//2, app.width - app.margin - app.pointSize//2)
        y = random.randint(app.margin + app.pointSize//2, app.gridHeight + app.margin - app.pointSize//2)
        if (not inPoint(app, x, y, app.pointSize) and not inMC(app, x, y, app.pointSize)
            and not inObstacle(app, x, y, app.pointSize) and not inExit(app, x, y, app.pointSize)):
            app.points.append((x, y))

# getCellBounds from grid-demo.py
def getCellBounds(app, row, col):
    # aka 'modelToView'
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = app.width - 2*app.margin
    x0 = app.margin + gridWidth * col / app.cols
    x1 = app.margin + gridWidth * (col+1) / app.cols
    y0 = app.margin + app.gridHeight * row / app.rows
    y1 = app.margin + app.gridHeight * (row+1) / app.rows
    return (x0, y0, x1, y1)

#################################################
# KEYPRESSED
#################################################

# later will have to make more functions 
# - to switch from home screen
# - to go to instructions screen
# each of these screens will get its own draw function

def moveChara(app, event):
    step = 10
    cellHeight = app.gridHeight/app.rows
    cellWidth = (app.width - 2*app.margin)/app.cols
    if event.key =='Up' or event.key =='Down' or event.key =='Left' or event.key =='Right':
        app.mcCounter = (1+app.randoCounter) % len(app.scribbleSprites)
    if (event.key == 'Up' and inBounds(app, app.chara.x, app.chara.y - step, app.mcSize)
        and not inObstacle(app, app.chara.x, app.chara.y - step, app.mcSize)):    
        app.chara.row = (app.chara.y - app.margin)//cellHeight
        app.chara.y -= step
        app.chara.d = "S"
    elif (event.key == 'Down' and inBounds(app, app.chara.x, app.chara.y + step, app.mcSize)
            and not inObstacle(app, app.chara.x, app.chara.y + step, app.mcSize)):  
        app.chara.row = (app.chara.y - app.margin)//cellHeight
        app.chara.y += step
        app.chara.d = "N"
    elif (event.key == 'Left' and inBounds(app, app.chara.x - step, app.chara.y, app.mcSize)
            and not inObstacle(app, app.chara.x - step, app.chara.y, app.mcSize)):  
        app.chara.col = (app.chara.x - app.margin)//cellWidth
        app.chara.x -= step
        app.chara.d = "E"
    elif (event.key == 'Right' and inBounds(app, app.chara.x + step, app.chara.y, app.mcSize)
            and not inObstacle(app, app.chara.x + step, app.chara.y, app.mcSize)): 
        app.chara.col = (app.chara.x - app.margin)//cellWidth
        app.chara.x += step
        app.chara.d = "W"

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
    if event.key == "1":
        appStarted(app)
        app.gameOver = False
        app.homeScreen = False
        app.instructions = False
    if event.key == "2":
        app.gameOver = True
        app.homeScreen = False
        app.instructions = True
    if not app.gameOver:
        typing(app, event)
        moveChara(app, event)

        # removes points if the mc is on that square
        if inPoint(app, app.chara.x, app.chara.y, app.mcSize) != False:
            (pointx, pointy) = inPoint(app, app.chara.x, app.chara.y, app.mcSize)
            app.points.remove((pointx, pointy))
            app.p += 1
        
        placePoint(app)
        nextLevel(app)

#################################################
# TIMER
#################################################

def carnegieChecks(app):
    if app.time%app.carnegieGenerationSpeed == 0:
        newCarnegie(app)
    for c in app.carnegies:
        if app.time%5 == 0:
            c.move(app)
    if "".join(app.text[-1]) == "my heart is in the work" and len(app.carnegies) > 0:
        app.carnegies.pop(0)
        app.text.append([""])
        app.p += 3

def tankChecks(app):
    if app.time%75== 0:
        newTank(app)
    for c in app.tanks:
        if app.time%app.tankSpeed == 0:
            c.move(app, 0)
    if "".join(app.text[-1]) == "SPEED" and len(app.tanks) > 0:
        app.tanks.pop(0)
        app.text.append([""])
        app.p += 1

def randoChecks(app):
    if app.time%110 == 0:
        newRando(app)
    #print("randos", app.randos)
    for rando in app.randos:
        if app.time%app.randoSpeed == 0:
            rando.move(app,0)
    if len(app.randos) > 0:
        #print("word", app.randWords[0])
        for word in app.randWords:
            if "".join(app.text[-1]) == word:
                index = app.randWords.index(word)
                #print("is this running")
                app.randos.pop(index)
                app.randWords.remove(word)
                app.text.append([""])
                app.p += 1

def nextLevel(app):
    if app.p >= app.pointsNeeded and inExit(app, app.chara.x, app.chara.y, app.mcSize):
        app.level += 1
        app.numObstacles += 3
        app.pointsNeeded += 3
        if app.numObstacles > 0.30*(app.cols * app.rows):
            app.rows += 1
            app.cols += 1
        if app.level > 2:
            app.carnegieGenerationSpeed -= 12
        if app.level > 5:
            app.tankSpeed -= 3
        if app.level > 6:
            app.randoSpeed -= 2
        
        initSize(app)
        initChara(app)
        initExit(app)
        initObstacles(app, app.numObstacles)
        initPoints(app)
        
        #set ghosts back to none
        initCarnegie(app)
        initTank(app)
        initRando(app)
        
        #set back to 0 points
        app.p = 0
        
        app.oop = []
        app.oopSprites = []
        app.sinking = []
        app.sinkingSprites = []
        app.burning = []
        app.burningSprites = []

def timerFired(app):
    #if app.gameOver or app.waitingForFirstKeyPress: return
    if not app.gameOver: 
        if app.time%5 == 0:
            app.shipCounter = (1+app.shipCounter) % len(app.shipSprites)
            for i in range(len(app.oop)):
                if app.oopSprites[i] < 4:
                    app.oopSprites[i]+=1
        for i in range(len(app.sinking)):
                if app.sinkingSprites[i] < 6:
                    app.sinkingSprites[i]+=1
        for i in range(len(app.burning)):
                if app.burningSprites[i] < 7:
                    app.burningSprites[i]+=1
        app.randoCounter = (1+app.randoCounter) % len(app.scribbleSprites)

        app.time += 1
        if app.level > 1:
            carnegieChecks(app)
        if app.level > 2:
            tankChecks(app)
        if app.level > 3:
            randoChecks(app)

        # if the ghost runs into mc, lose a live and ghost disappears
        for c in app.carnegies:
            x, y = c.x, c.y
            if inMC(app, x, y, app.carnegieSize):
                app.chara.lives -= 1
                app.oop.append((x,y))
                app.oopSprites.append(0)
                app.carnegies.remove(c)
        
        for c in app.tanks:
            row,col = c.row, c.col
            x0,y0,x1,y1 = getCellBounds(app, row, col)
            x,y = (x0+x1)/2, (y0+y1)/2
            if row == app.chara.row and col == app.chara.col:
                app.chara.lives -= 1
                app.sinking.append((x,y))
                app.sinkingSprites.append(0)
                app.tanks.remove(c)
        
        for rando in app.randos:
            x, y = rando.x, rando.y
            if inMC(app, x, y, app.randoSize):
                index = app.randos.index(rando)
                app.chara.lives -= 1
                app.burning.append((x,y))
                app.burningSprites.append(0)
                app.randos.remove(rando)
                app.randWords.pop(index)
        
        # game over if no more lives
        if app.chara.lives <= 0 or app.level > 10:
            app.gameOver = True

#################################################
# DRAWING
#################################################

def drawCarnegie(app, canvas):
    # he's just going to be a purple dot for now
    for carnegie in app.carnegies:
        #canvas.create_oval(carnegie.x - app.carnegieSize/2, carnegie.y - app.carnegieSize/2,
        #                carnegie.x + app.carnegieSize/2, carnegie.y + app.carnegieSize/2,
        #                fill = "purple")
        canvas.create_text(carnegie.x, carnegie.y - app.carnegieSize/2 - app.cellSize/6, anchor = "s", 
                        text = "my heart is in the work")
        canvas.create_image(carnegie.x, carnegie.y, image=ImageTk.PhotoImage(app.imageCarnegie2))

def drawTank(app, canvas):
    # he's just going to be a purple dot for now
    for tank in app.tanks:
        x0, y0, x1, y1 = getCellBounds(app, tank.row, tank.col)
        x,y = (x0+x1)/2, (y0+y1)/2
        sprite = app.shipSprites[app.shipCounter]
        if tank.d == "E":
            canvas.create_image(x, y, image = ImageTk.PhotoImage(sprite.transpose(Image.FLIP_LEFT_RIGHT)))
        elif tank.d == "W":
            canvas.create_image(x, y, image = ImageTk.PhotoImage(sprite))
        elif tank.d == "N":
            canvas.create_image(x, y, image = ImageTk.PhotoImage(sprite.transpose(Image.ROTATE_270)))
        elif tank.d == "S":
            canvas.create_image(x, y, image = ImageTk.PhotoImage(sprite.transpose(Image.ROTATE_90)))
        canvas.create_text((x0 + x1)/2, y0, anchor = "s", 
                        text = "SPEED")

def drawRando(app, canvas):
    # he's just going to be a orange dot for now
    for rando in app.randos:
        sprite = app.scribbleSprites[app.randoCounter]
        canvas.create_image(rando.x, rando.y, image = ImageTk.PhotoImage(sprite))
        canvas.create_text(rando.x, rando.y - app.randoSize/2, anchor = "s", 
                        text = app.randWords[app.randos.index(rando)])

def drawTextBox(app, canvas):
    # make the textbox (height = the height of one square)
    canvas.create_rectangle(app.margin, app.height - app.textboxHeight, 
                            app.width - app.margin, 
                            app.height - app.margin, fill = "white")
    
    word1, word2, word3, word4 = "", "", "", ""
    if len(app.text) >= 1:
        word1 = "".join(app.text[-1])
    if len(app.text) >= 2:
        word2 = "".join(app.text[-2])
    if len(app.text) >= 3:
        word3 = "".join(app.text[-3])
    if len(app.text) >= 4:
        word4 = "".join(app.text[-4])

    canvas.create_text(app.margin + 6, app.height - app.margin - 5, 
                       text = (word4 + "\n" + word3 + "\n" + word2 + "\n" + word1), 
                       anchor = "sw", font="Arial 14")

def drawPoint(app, canvas):
    for i in range(len(app.points)):
        (x, y) = app.points[i]
        canvas.create_image(x , y, image = ImageTk.PhotoImage(app.imagePlaid2))

def drawObstacle(app, canvas):
    for row, col in app.obstaclesLocation:
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        x, y = (x0+x1)/2, (y0+y1)/2
        canvas.create_image(x,y, image = ImageTk.PhotoImage(app.imageSteel2))

def drawExit(app, canvas):
    row, col = app.exit
    x0, y0, x1, y1 = getCellBounds(app, row, col)
    x0 = app.width - app.margin - app.exitWidth
    x, y = app.width - app.margin, (y0+y1)/2
    if app.p < app.pointsNeeded:
        canvas.create_image(x, y, anchor = "e", image = ImageTk.PhotoImage(app.imageDoor2) )
    else:
        canvas.create_image(x, y, anchor = "e", image = ImageTk.PhotoImage(app.imageOpenDoor2) )

    
    #canvas.create_rectangle(x0, y0, x1, y1, fill = "yellow")

def drawMC(app, canvas):
    # draw the mc (he's j a circle for now)
    #canvas.create_oval(app.chara.x - app.mcSize/2, app.chara.y - app.mcSize/2, 
    #                   app.chara.x + app.mcSize/2, app.chara.y + app.mcSize/2, fill='blue')
    x, y = app.chara.x, app.chara.y
    sprite = app.mcSprites[app.mcCounter]
    if app.chara.d == "E":
        canvas.create_image(x, y, image = ImageTk.PhotoImage(sprite.transpose(Image.FLIP_LEFT_RIGHT)))
    elif app.chara.d == "W":
        canvas.create_image(x, y, image = ImageTk.PhotoImage(sprite))
    elif app.chara.d == "N":
        canvas.create_image(x, y, image = ImageTk.PhotoImage(sprite.transpose(Image.ROTATE_270)))
    elif app.chara.d == "S":
        canvas.create_image(x, y, image = ImageTk.PhotoImage(sprite.transpose(Image.ROTATE_90)))

def drawOop(app, canvas):
    for i in range(len(app.oop)):
        if app.oopSprites[i] < 4:
            x,y = app.oop[i]
            canvas.create_image(x, y, image = ImageTk.PhotoImage(app.imageShockedCarnegie2))

def drawSinking(app, canvas):
    for i in range(len(app.sinking)):
        if app.sinkingSprites[i] < 6:
            x,y = app.sinking[i]
            canvas.create_image(x,y, image = ImageTk.PhotoImage(app.sinkingSpritez[app.sinkingSprites[i]]))

def drawBurning(app, canvas):
    for i in range(len(app.burning)):
        if app.burningSprites[i] < 7:
            x,y = app.burning[i]
            y += app.pointSize/2
            canvas.create_image(x,y, anchor = "s", image = ImageTk.PhotoImage(app.burningSpritez[app.burningSprites[i]]))

def redrawAll(app, canvas):
    # make background black
    canvas.create_rectangle(0,0, app.width, app.height, fill = "black")
    # draw floor
    canvas.create_image(app.width/2, app.gridHeight/2+app.margin, image = ImageTk.PhotoImage(app.imageFloor2) )

    drawTextBox(app, canvas)
    drawObstacle(app, canvas)
    
    drawOop(app, canvas)
    drawSinking(app, canvas)
    drawBurning(app, canvas)
    
    drawExit(app, canvas)
    drawPoint(app, canvas)
    drawMC(app, canvas)
    drawCarnegie(app, canvas)
    drawTank(app, canvas)
    drawRando(app, canvas)

    # prints how many points collected
    canvas.create_text(5,0, anchor = "nw", text = f'points: {app.p}', fill = "white")
    #prints how many lives mc has
    canvas.create_text(app.width - 10, 0, anchor = "ne", text = f'lives: {app.chara.lives}', fill = "white")
    canvas.create_text(app.width/2, app.margin/2, text = f'ROOM {app.level}', font = "bold 20", fill = "white")
    pointsNeeded = app.pointsNeeded - app.p
    if pointsNeeded < 0:
        pointsNeeded = 0
    canvas.create_text(app.width/2, app.height - app.textboxHeight - app.margin/2, 
                       text = f"points needed: {pointsNeeded}", fill = "white")

    # print game over
    if app.gameOver:
        if app.level > 10:
            canvas.create_rectangle(app.width/2 - 75, app.margin + app.gridHeight/2 - 25, app.width/2 + 100, app.margin + app.gridHeight/2 + 25, fill = "black")
            canvas.create_text(app.width/2, app.gridHeight/2 + app.margin, text = "YOU WIN\npress 1 to play again", fill = "white")
        else:
            canvas.create_rectangle(app.width/2 - 100, app.margin + app.gridHeight/2 - 25, app.width/2 + 100, app.margin + app.gridHeight/2 + 25, fill = "black")
            canvas.create_text(app.width/2, app.gridHeight/2 + app.margin, text = "GAME OVER\npress 1 to try again", fill = "white")
    if app.homeScreen:
        canvas.create_rectangle(0,0,app.width, app.height, fill = "white")
        canvas.create_image(app.width/2, app.height/2, image = ImageTk.PhotoImage(app.home))
        canvas.create_text(app.width/2, app.height/2, text = "Press 1 or 2 any time to:\n1--> PLAY\n2--> instructions")
    if app.instructions:
        canvas.create_image(app.width/2, app.height/2, image = ImageTk.PhotoImage(app.instruction))

runApp(width=600, height=705)

