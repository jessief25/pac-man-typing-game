# This demos loadImage and scaleImage from a url

from cmu_112_graphics import *

def appStarted(app):

    app.rows = 6
    app.cols = 6

    app.margin = 30
    app.textboxHeight = 100
    app.gridHeight = app.height - app.textboxHeight - 2*app.margin

    app.cellSize = app.gridHeight/app.rows
    print("cellSize", app.cellSize)

    app.pointSize = int(app.cellSize/4)
    app.mcSize = int(app.cellSize/1.75)
    app.carnegieSize = int(app.cellSize/2)
    app.carnegiep = app.carnegieSize/600
    app.randoSize = app.cellSize/2
    
    app.image1 = app.loadImage('carnegie.png')
    app.image2 = app.scaleImage(app.image1, app.carnegiep)

    app.steelp = app.cellSize/1000
    app.imageSteel = app.loadImage('steel.png')
    app.imageSteel2 = app.scaleImage(app.imageSteel, app.steelp)

    app.pointp = app.pointSize/1000
    app.imagePlaid = app.loadImage('plaid.png')
    app.imagePlaid2 = app.pointSize/1000

def drawCarnegie(app, canvas):
    # he's just going to be a purple dot for now
        canvas.create_oval(app.width/2 - app.carnegieSize/2 - 100, app.height/2 - app.carnegieSize/2,
                        app.width/2 + app.carnegieSize/2 - 100, app.height/2 + app.carnegieSize/2,
                        fill = "purple")
        canvas.create_text(app.width/2, app.height/2 - app.carnegieSize/2 -15, anchor = "s", 
                        text = "my heart is in the work")
        canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.image2))
def redrawAll(app, canvas):
    #canvas.create_image(200, 300, image=ImageTk.PhotoImage(app.image1))
    #canvas.create_rectangle(0,0, app.width, app.height, fill = "blue")
    #drawCarnegie(app, canvas)
    #canvas.create_image(app.width/2, app.height/2, image = ImageTk.PhotoImage(app.imageSteel2))
    #canvas.create_rectangle(app.width/2 - app.cellSize/2 + 100, app.height/2 - app.cellSize/2, 
                            app.width/2 + app.cellSize/2 + 100, app.height/2 + app.cellSize/2, fill = "pink")
runApp(width=600, height=705)

'''

running mc sprite from: https://stock.adobe.com/search?k=game+character+sprite&asset_id=184392243

homescreen 
'''