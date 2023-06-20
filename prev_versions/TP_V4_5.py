#################################################
# TP V.4
#
# Your name: Jessie Fan
# Your andrew id: jessief
#################################################

import math, os, string, random
from cmu_112_graphics import *

#################################################
# Helper functions
# from: https://www.cs.cmu.edu/~112/notes/notes-variables-and-functions.html
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
# TIMELOG:
# previously had 5ish hours for TP0

# TP1:
# oh writing the design thing i spent like ~30 min on 11/16 doing that ig
# 11/16 11:15pm - 11/17 1am
# 11/17 ~3pm - 4:30 pm
# 11/17 ~30 minutes on design
# 11/18 9am - 1pm
# 11/18 ~20 minutes on the design thing

# 11/22 9:30am - 

# change it so that the points and the mc aren't confined to rows and cols 
#   give them a size and like bounds (like the edges can't be within the obstacles)
# but the carnegie ghost can be confined to the rows and columns (like in a tank)
# can make a different ghost who is faster but not confined to the rows and cols
#################################################

# some bits based on snake from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#exampleSnake

#################################################
# INITIALIZE
#################################################

def appStarted(app):
    app.time = 0
    app.rows = 10
    app.cols = 10
    app.margin = 5 # margin around grid
    app.timerDelay = 250

    app.exit = ((app.rows - 2)//2, app.cols - 1)

    # keep track of points
    app.p = 0
    
    app.pointSize = 20
    app.mcSize = 10

    initChara(app)
    initTextBox(app)
    initObstacles(app)
    initPoints(app)
    initCarnegie(app)
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

# makes a graph for each ghost
def makeGraph(app):
    #recursively add edges until the end has been found?
    # starts at start
    g = graph(app)
    row, col = app.carnegie.row, app.carnegie.col
    paths = []
    pathsWeight = []

    # to get the path would have to go backwards from the exit node and see 
    # which 
    if (row, col) == app.exit:
        #paths.append()
        return
        
    else:
        # node B becomes node A
        # new move becomes node A
        # at the end can check if the last move in the path is the exit
        # if it is then it is a path
        nodeA = (app.carnegie.row, app.carnegie.col)
        for (drow, dcol) in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                    (nrow, ncol) = (row + drow, col + dcol)
                    if ((nrow, ncol) not in app.obstaclesLocation and # not an obstacle
                        (nrow, ncol) not in positions and #haven't moved there before
                        0 <= nrow < (app.rows - 2) and 0 <= ncol < app.cols):  #not off board
                        #move
                        return

    def getPaths(app, row, col, positions, paths):
        if (row, col) == (app.chara.row, app.chara.col):
            return (positions, paths)
        else:
            # for later ones I will have to add diagonals to directions
            for (drow, dcol) in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                (nrow, ncol) = (row + drow, col + dcol)
                if ((nrow, ncol) not in app.obstaclesLocation and # not an obstacle
                    (nrow, ncol) not in positions and #haven't moved there before
                    0 <= nrow < (app.rows - 2) and 0 <= ncol < app.cols):  #not off board
                    #move
                    row += drow
                    col += dcol
                    positions.append((row,col))
                    # must add edge for all possible ones...
                    g.addEdge(app, (row - drow, col - dcol), (row, col))

                    # this prolly doesn't work
                    solution = (positions, paths) = getPaths(app, row, col, positions)
                    if solution != None and positions not in paths:
                        paths.append(positions)
                    #else undo move
                    row = row - drow
                    col = col - dcol
                    positions.pop()
            return None
    
    return g

def initCarnegie(app):
    app.carnegies = []
    app.carnegie = carnegie(app)
    #app.graph = makeGraph(app)

# later add a parameter of level to control how many obstacles made
# have to use backtracking to confirm that it's possible to escape
# with these obstacles... so only add obstacle if there is a solution...
def initObstacles(app):
    app.obstacles = []
    app.obstaclesLocation = []
    
    # for now, make 10 obstacles
    while len(app.obstacles) < 10:
        newRow = random.randint(0, app.rows - 3)
        newCol = random.randint(0, app.cols - 1)
        newObstacle = obstacle(app, newRow, newCol)
        if (newRow, newCol) not in app.obstaclesLocation and (newRow, newCol) != app.start:
            app.obstacles.append(newObstacle)
            app.obstaclesLocation.append((newRow, newCol))
            # if it's not possible to make a solution with these obstacles
            if not isSolution(app, app.chara.row, app.chara.col, []):
                # then remove obstacle
                app.obstacles.pop()
                app.obstaclesLocation.pop()
    
#################################################
# CLASSES 
#################################################

class mc(object):
    def __init__(self, app):
        self.lives = 3
        self.row = (app.rows - 2)//2
        self.col = 0
        self.x = app.margin + app.mcSize/2
        self.y = 0

# if I'm lazy, use random word generator and it's j a typing game w generic ghost
# goes away when you type 'my heart is in the work'
class carnegie(object):
    def __init__(self, app):
        # randomize starting position to any of the outer square with out an obstacle
        # for now will just start at the exit (because that def doesn't have a obstacle)
        self.x, self.y = (app.width, (2/3)*app.height)
    
    def move(self, app):
        step = 20
        directionx, directiony = (0,0)
        leastDistance = app.width
        (mcx, mcy) = getCoordinates(app, app.chara.row, app.chara.col)
        for dx, dy in [(0,1), (1,0), (-1,0), (0,-1)]:
            tempx, tempy = (self.x + step*dx),(self.y + step*dy)
            if distance(mcx, mcy, tempx, tempy) < leastDistance:
                leastDistance = distance(mcx, mcy, tempx, tempy)
                directionx, directiony = (dx, dy)
        self.x += step*directionx
        self.y += step*directiony

# from the Graph mini-lecture
# idek where to put this or like initialize it
class graph(object):
    def __init__(self, app):
        self.table = {}
    
    # Add an edge between two nodes in a graph
    # each node should be the state of 
    # will be a tree instead of interconnected thing
    # so finds the best path (least amount of points)

    # makes a dicitonary of all the nodes (which would be the states or board in my case)
    # when do I add an edge? (each time the ghost makes a hypothetical move, right?)
    # maybe use recursion to find all the possible paths and then add edges for each move made
    #   this works for finding one path that works... to find all possible paths... hmmm?
    #   i would probably have to keep a set or list or whatever to keep track of the paths that were taken
    #   and like backtrack if that path has been taken at the end
    #   maybe make another list for like the edges
    #   have to make another function to find the totals of the edges
    #   then find the path that has the minimum total and have the ghost move along that path...
    #   so function that returns the smallest path
    #   and run that when move ghost (bc ghost will go along the smallest path)

    #   is legal (when not in seen steps and not on an obstacle), target is where the player is
    def addEdge(self, app, nodeA, nodeB):
        if nodeA not in self.table:
            self.table[nodeA] = dict()
        if nodeB not in self.table:
            self.table[nodeB] = dict()
        d = distance(app.carnegie.row, app.carnegie.col, app.mc.row, app.mc.col)
        self.table[nodeA][nodeB] = d
        #self.table[nodeB][nodeA] = d
    
    # dictionary of nodes
    # each node is a place a ghost can be
    # each node to another dictionary of possible places it can move
    # each place it can move is weighted with (I'm going to use the distance from the ghost)
    # then makes a new node and adds to dictionary 
    # a path would then be like a path from node to node
    # if it works (like there is a path) ** still not sure how to go through all the paths**
    # then add upthe total and add to a list ig

    # so instead of giant recurion stuff, use dictionaries
    # for each node 
    def getPath(self, app, row, col, paths):
        return
    
    # Return the weight of an edge between nodeA and nodeB:
    def getEdge(self, nodeA, nodeB):
        return self.table[nodeA][nodeB]
    
    # Return a list of all nodes in the graph
    def getNodes(self):
        return list(self.table)
    
    def getNeighbors(self, node):
        return set(self.table[node])

    # similar to solving a maze i think
    # how do I get all the paths??
    # 1. keep a set of all vertices that are visited, initially empty
    # 2. stop if the start node = target node [target node is the mc]
    # 3. add the start node to the visisted set
    # 4. loop over all the neighbors of the start node
    # 5. if the neighbor is unvisted, do a DFS w the neighbor as the start node
    #       a. done with recursion usually...
    def DFS():
        return
        # used to solve mazes??
    
    def BFS():
        return 
        # used to find shortest path between 2 points on UNWEIGHTED GRAPH
        # 1. Keep a set of all vertices that are visited, initially empty
        # 2. Have a queue of unvisited neighbors (initially just the start node)
        # 3. Extract the current node from the front of the queue
        # 4. Skip if the current node has already been visited, otherwise mark it as visited
        # 5. Stop if the current node = the target node
        # 6. Loop over the neighbors of the current node
        # 7. If they are unvisited, add them to the end of the queue
        # 8. Repeat 3-7 until the queue is empty
                # This is typically not done with recursion


    # returns a path from the start node to the target node
    # would use to get the minimum weighted path...
    # weight the path based on how far from mc (distance from)

    # maybe do another function to get the weight of a path...
    # 1. have dicitonary mapping each node to a previous node (initially None)
    # 2. Whenever the search visits node V from node U, have V point to U in the dictionary
    # 3. At the end of the search, start at the target node and follow the pointers back to the start 
    #    node, building the list up as we go

    '''
    each state is like when the ghost moves one square 
    (gotta go through all the directions), each would be a state and a new branch
    use like greatest algorithm (and update it, if it's the least...)
    then moves the ghost in the least direction
    '''

class obstacle(object):
    def __init__(self, app, row, col):
        # where it's located
        self.row = row
        self.col = col
        return

#################################################
# OTHER
#################################################

def inPoint(app, x, y, size):
    for pointx, pointy in app.points:
        x0, x1, y0, y1 = pointx - size/2, pointx + size/2, pointy - size/2, pointy + size/2
        if ((((x + size/2) >= x0) and ((x + size/2) < x1)) or (((x - size/2) >= x0) and ((x - size/2) < x1))
            or (((y + size/2) >= y0) and ((y + size/2) < y1)) or (((y - size/2) >= y0) and ((y - size/2) < y1))):
            return True
    return False

def inMC(app, x, y, size):
    x0, y0, x1, y1 = x - app.mcSize/2, y - app.mcSize, x + app.mcSize, y + app.mcSize
    if ((((x + size/2) >= x0) and ((x + size/2) < x1)) or (((x - size/2) >= x0) and ((x - size/2) < x1))
        or (((y + size/2) >= y0) and ((y + size/2) < y1)) or (((y - size/2) >= y0) and ((y - size/2) < y1))):
        return True
    return False

def inObstacle(app, x, y, size):
    for obstacleRow, obstacleCol in app.obstaclesLocation:
        x0, y0, x1, y1 = getCellBounds(app, obstacleRow, obstacleCol)
        if ((((x + size/2) >= x0) and ((x + size/2) < x1)) or (((x - size/2) >= x0) and ((x - size/2) < x1))
            or (((y + size/2) >= y0) and ((y + size/2) < y1)) or (((y - size/2) >= y0) and ((y - size/2) < y1))):
            return True
    return False

# **** DON"T FORGET TO CHANGE ALL THE 2/3
# rn they're there because that's the ratio of the textbox

def inBounds(app, x, y, size):
    x0, y0, x1, y1 = app.margin, app.margin, app.width - app.margin, (2/3)*app.height
    if ((((x + size/2) >= x0) and ((x + size/2) < x1)) or (((x - size/2) >= x0) and ((x - size/2) < x1))
        or (((y + size/2) >= y0) and ((y + size/2) < y1)) or (((y - size/2) >= y0) and ((y - size/2) < y1))):
        return True
    return False

def newCarnegie(app):
    newCarnegie = carnegie(app)
    app.carnegies.append(newCarnegie)

def getCoordinates(app, row, col):
    cellLength = app.width/app.cols
    x = col * cellLength + 0.5*cellLength
    y = row * cellLength + 0.5*cellLength
    return (x, y)

def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1 - y2)**2)**0.5

# returns one of the paths a ghost can take to get to mc
# row and col is row and col of ghost (when call function)
# and positions will initially include just the starting position
def getPaths(app, row, col, positions, paths):
    if (row, col) == (app.chara.row, app.chara.col):
        return (positions, paths)
    else:
        # for later ones I will have to add diagonals to directions
        for (drow, dcol) in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            (nrow, ncol) = (row + drow, col + dcol)
            if ((nrow, ncol) not in app.obstaclesLocation and # not an obstacle
                (nrow, ncol) not in positions and #haven't moved there before
                0 <= nrow < (app.rows - 2) and 0 <= ncol < app.cols):  #not off board
                #move
                row += drow
                col += dcol
                positions.append((row,col))

                # this prolly doesn't work
                solution = (positions, paths) = getPaths(app, row, col, positions)
                if solution != None and positions not in paths:
                    paths.append(positions)
                #else undo move
                row = row - drow
                col = col - dcol
                positions.pop()
        return None

'''
after the path has been found
check that it doesn't already exist in the list of paths
if it does, then i have to undo the last move and redo it so that it's possible 
and not in the list
will return the list of paths
'''

# to get all the possible paths that the ghost can take
# paths will initially be empty
def getAllPaths(app, paths):
    return


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
    # Keep trying random positions until we find one that is not in
    # the snake. Note: there are more sophisticated ways to do this.
    while(len(app.points) < 3):
        x = random.randint(app.margin, app.width - app.margin)
        y = random.randint(app.margin, (2/3)*app.height)
        print(x, y)
        if (not inPoint(app, x, y, app.pointSize) and not inMC(app, x, y, app.pointSize)
            and not inObstacle(app, x, y, app.pointSize)):
            app.points.append((x, y))
            print("points", app.points)

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
    # MOVES THE MC
    # it's app.chara.row - 2 because the last 2 rows are for the text box
    step = 10
    if (event.key == 'Up' and inBounds(app, app.chara.x, app.chara.y - step, app.mcSize) 
        and not inObstacle(app, app.chara.x, app.chara.y - step, app.mcSize)):    
        app.chara.y -= step
    elif (event.key == 'Down' and 0 <= app.chara.row + 1 < app.rows - 2
          and (app.chara.y + 1, app.chara.x) not in app.obstaclesLocation):  
        app.chara.row += 1
    elif (event.key == 'Left' and 0 <= app.chara.col - 1 < app.cols
          and (app.chara.y, app.chara.x - 1) not in app.obstaclesLocation):  
        app.chara.col -= 1
    elif (event.key == 'Right' and 0 <= app.chara.col + 1 < app.cols
          and (app.chara.y, app.chara.x + 1) not in app.obstaclesLocation): 
        app.chara.col += 1

def typing(app, event):
    if event.key == "Enter":
    # adds a new list for the next word
        app.text.append([])
    elif event.key == "Delete" or event.key == "Backspace":
        if len(app.text[-1]) > 0:
            app.text[-1].pop()
    elif event.key == "Space":
        app.text[-1].append(" ")
    elif event.key in string.printable:
        app.text[-1].append(event.key)

def keyPressed(app, event):
    #if (app.waitingForFirstKeyPress):
        #app.waitingForFirstKeyPress = False
    #else:
    typing(app, event)
    moveChara(app, event)

    # removes points if the mc is on that square
    # CHANGE!!!
    if (app.chara.row,app.chara.col) in app.points:
        app.points.remove((app.chara.row,app.chara.col))
        app.p += 1
    
    placePoint(app)

#################################################
# TIMER
#################################################

def carnegieChecks(app):
    if app.time%50== 0:
        newCarnegie(app)
    for c in app.carnegies:
        c.move(app)
    if "".join(app.text[-1]) == "my heart is in the work" and len(app.carnegies) > 0:
        app.carnegies.pop()
        app.text.append([""])

def timerFired(app):
    #if app.gameOver or app.waitingForFirstKeyPress: return
    app.time += 1
    carnegieChecks(app)


#################################################
# DRAWING
#################################################

def drawCarnegie(app, canvas):
    #he's just going to be a purple dot for now
    size = 20
    for carnegie in app.carnegies:
        canvas.create_oval(carnegie.x - size/2, carnegie.y - size/2,
                        carnegie.x + size/2, carnegie.y + size/2,
                        fill = "purple")
        canvas.create_text(carnegie.x, carnegie.y - size/2, anchor = "s", 
                        text = "my heart is in the work")

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

def redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawTextBox(app, canvas)
    drawObstacle(app, canvas)
    drawPoint(app, canvas)
    drawCarnegie(app, canvas)

    # draw the mc (he's j a circle for now)
    (x0, y0, x1, y1) = getCellBounds(app, app.chara.row, app.chara.col)
    canvas.create_oval(app.chara.x - app.mcSize/2, app.chara.y - app.mcSize/2, 
                       app.chara.x + app.mcSize/2, app.chara.y + app.mcSize/2, fill='blue')

    # prints how many points collected
    canvas.create_text(0,0, anchor = "nw", text = f'points: {app.p}')

runApp(width=600, height=600)