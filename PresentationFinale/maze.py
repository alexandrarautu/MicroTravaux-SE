import turtle
import threading
import sys

PART_OF_PATH = 'O'
TRIED = '.'
OBSTACLE = '+'
DEAD_END = '-'

class Maze():
    def __init__(self,mazeFileName):
        rowsInMaze = 0
        columnsInMaze = 0
        self.mazelist = []
        mazeFile = open(mazeFileName,'r')
        rowsInMaze = 0
        for line in mazeFile:
            rowList = []
            col = 0
            for ch in line:
                rowList.append(ch)
                if ch == 'S':
                    self.startRow = rowsInMaze
                    self.startCol = col
                col = col + 1
            rowsInMaze = rowsInMaze + 1
            self.mazelist.append(rowList)
            columnsInMaze = len(rowList)-1

        self.rowsInMaze = rowsInMaze
        self.columnsInMaze = columnsInMaze
        self.xTranslate = -columnsInMaze/2
        self.yTranslate = rowsInMaze/2
        self.t = turtle.Turtle()
        self.t.shape('turtle')
        self.wn = turtle.Screen()
        self.wn.setworldcoordinates(self.xTranslate, -self.yTranslate, -self.xTranslate, self.yTranslate)


    def drawMaze(self):
        self.t.speed(3)
        self.wn.tracer(0)
        for y in range(self.rowsInMaze):
            for x in range(self.columnsInMaze):
                if self.mazelist[y][x] == OBSTACLE:
                    self.drawCenteredBox(x+self.xTranslate,-y+self.yTranslate,'tan')
                    #print(self.mazelist[y][x])
        self.t.color('black')
        self.t.fillcolor('royalblue')
        self.wn.update()
        self.wn.tracer(1)

    def drawCenteredBox(self,x,y,color):
        self.t.up() # pull the pen up, no drawing when moving
        self.t.goto(x-.5,y-.5)
        self.t.color(color)
        self.t.fillcolor(color)
        self.t.setheading(90)
        self.t.down() #pull the pen down, drawing when moving
        self.t.begin_fill()
        for i in range(4):
            self.t.forward(1)
            self.t.right(90)
        self.t.end_fill()

    def moveTurtle(self,x,y):
        self.t.up()
        #self.t.setheading(self.t.towards(x+self.xTranslate,-y+self.yTranslate))
        self.t.goto(x+self.xTranslate,-y+self.yTranslate)

    def dropBreadcrumb(self,color):
        self.t.dot(10,color) #draw a circular dot with diameter size, using color

    def updatePosition(self,row,col,val=None):
        if val:
            self.mazelist[row][col] = val
        self.moveTurtle(col,row)

        if val == PART_OF_PATH:
            color = 'green'
        elif val == OBSTACLE:
            color = 'red'
        elif val == TRIED:
            color = 'black'
        elif val == DEAD_END:
            color = 'red'
        else:
            color = None

        if color:
            self.dropBreadcrumb(color)

    def isExit(self,row,col):
        return (row == 0 or
                row == self.rowsInMaze-1 or
                col == 0 or
                col == self.columnsInMaze-1 )

    def __getitem__(self,idx):
        return self.mazelist[idx]

def deploy_threads(id, stop, maze, startRow, startColumn):
    searchFrom(maze,startRow, startColumn)
    print("I am thread ", id)
    while True:
        print("I am thread {} doing something ".format(id))
        if stop():
            print("Exiting loop")
            break
    print("Thread {}, signing off".format(id))

found1 = False
found2 = False
found3 = False
found4 = False
gasit = False 

def searchFrom(maze, startRow, startColumn):
    # try each of four directions from this point until we find a way out.
    # base Case return values:
    #  1. We have run into an obstacle, return false
    global found1,found2,found3,found4, gasit
    maze.updatePosition(startRow, startColumn)
    if maze[startRow][startColumn] == OBSTACLE :
        print("\nAm dat de un obstacol")
        return False
    #  2. We have found a square that has already been explored
    if maze[startRow][startColumn] == TRIED or maze[startRow][startColumn] == DEAD_END:
        print("\nAm mai fost pe aici..")
        return False
    # 3. We have found an outside edge not occupied by an obstacle
    if maze.isExit(startRow,startColumn):
        maze.updatePosition(startRow, startColumn, PART_OF_PATH)
        gasit = True 
        return True
    maze.updatePosition(startRow, startColumn, TRIED)
    print("\n Caut..")
    # Otherwise, use logical short circuiting to try each direction
    # # in turn (if needed)

    while gasit == False:
        if gasit == False:
            launch_threads(1, maze, startRow, startColumn-1)
        else:
            found1 = True
        if gasit == False:
            launch_threads(2, maze, startRow, startColumn+1)
        else:
            found2 = True
        if gasit == False:
            launch_threads(3, maze, startRow-1, startColumn)
        else:
            found3 = True
        if gasit == False:
            launch_threads(4, maze, startRow+1, startColumn)
        else:
            found4 = True

        found = found1 or found2 or found3 or found4
        if found:
            maze.updatePosition(startRow, startColumn, PART_OF_PATH)
            print()
            print("ATI GASIT IESIREA")
        else:
            maze.updatePosition(startRow, startColumn, DEAD_END)
        return found

    while True:
        maze.updatePosition(startRow, startColumn, PART_OF_PATH)

stop_threads = False
def launch_threads(id, maze, startRow, startColumn):
    
    
    threads = []

    tmp1 = threading.Thread(target = deploy_threads, args=(id, lambda: stop_threads, maze, startRow, startColumn))
    threads.append(tmp1)
    tmp1.start()

    stop_threads = True

    for threads in threads:
        threads.join()

if __name__ == '__main__':
    myMaze = Maze('maze2.txt')
    myMaze.drawMaze()
#myMaze.updatePosition(myMaze.startRow,myMaze.startCol)
    searchFrom(myMaze, myMaze.startRow, myMaze.startCol)
#searchFrom(myMaze, myMaze.startRow, myMaze.startCol)