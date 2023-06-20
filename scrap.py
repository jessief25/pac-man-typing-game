# me trying with rows and columns
# src and target are x,y coordinates!
def astar(app, src, target):
    tr, tc = target
    tx, ty = getCoordinates(app, tr, tc)
    sr, sc = src

    closed = []
    open = []

    start = Node(app, None, sr, sc, [])
    open.append(start)

    while len(open) > 0:
        leastF = 10000
        leastNode = None
        for node in open:
            if leastNode == None or node.f < leastF:
                leastF = node.f
                leastNode = node
        q = leastNode
        open.remove(q)

        #print("does it get to here")

        kids = []
        for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1)]:
            if not inObstacle(app, q.r + dr, q.r + dc, app.randoSize):
                kids.append(Node(q, q.r + dr, q.c + dc, q.directions + [(dr, dc)]))
        
        print("kids", kids)

        for kid in kids:
            add = True
            # if reach target
            if (kid.r, kid.c) == (tr, tc):
                print("im assuming it doesn't return")
                return kid.directions
            kid.g = q.g + distance(q.x, q.y, kid.x, kid.y)
            kid.h = diagDistance(app, tx, kid.x, ty, kid.y)
            kid.f = kid.g + kid.h
            # only add kid to open list
            # if there isn't a node with the same position and lower f in the open list
            # and there isn't a node with the same position and lower f in the closed list
            for node1 in open:
                if (node1.r, node1.c) == (kid.r, kid.c) and node1.f < kid.f:
                    add = False
            for node2 in closed:
                if (node2.x, node2.y) == (kid.x, kid.y) and node2.f < kid.f:
                    add = False
            if add:
                open.append(kid)
        closed.append(q)
    print("why is it printing None???")