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

    def __getitem__(self,idx):
        return self.mazelist[idx]

    def isExit(self,row,col):
        return (row == 0 or
                row == self.rowsInMaze-1 or
                col == 0 or
                col == self.columnsInMaze-1 )

    def updatePosition(self,row,col,val=None):
        if val:
            self.mazelist[row][col] = val

def deploy_threads(id, stop, maze, startRow, startColumn):
    searchFrom(maze,startRow, startColumn)
    print("I am thread ", id)
    print("I am thread {} doing something ".format(id))
    if stop():
        print("Exiting loop")
    print("Thread {}, signing off".format(id))

gasit = False 
found1 = False
def searchFrom(maze, startRow, startColumn):
    # try each of four directions from this point until we find a way out.
    # base Case return values:
    #  1. We have run into an obstacle, return false
    global gasit, found1
    maze.updatePosition(startRow, startColumn)
    if maze[startRow][startColumn] == OBSTACLE :
        print("Am dat de un obstacol")
        print("\n")
        return False
    #  2. We have found a square that has already been explored
    if maze[startRow][startColumn] == TRIED or maze[startRow][startColumn] == DEAD_END:
        print("Am mai fost pe aici")
        print("\n")
        return False
    # 3. We have found an outside edge not occupied by an obstacle
    if maze.isExit(startRow,startColumn):
        gasit = True 
        found1 = True
        return True
    maze.updatePosition(startRow, startColumn, TRIED)
    # Otherwise, try each direction
    # # in turn (if needed)
    if found1 == False:
        print("Caut...")
        launch_threads(maze, startRow, startColumn)
    else:
        print("AM GASIT IESIREA!")
        while True:
            pass
    return found1


def launch_threads(maze, startRow, startColumn):
    stop_threads = False
    threads = []
    tmp1 = threading.Thread(target = deploy_threads, args=(1, lambda: stop_threads, maze, startRow, startColumn-1))
    threads.append(tmp1)
   # tmp1.start()
    tmp2 = threading.Thread(target = deploy_threads, args=(2, lambda: stop_threads, maze, startRow, startColumn+1))
    threads.append(tmp2)
   # tmp2.start()
    tmp3 = threading.Thread(target = deploy_threads, args=(3, lambda: stop_threads, maze, startRow-1, startColumn))
    threads.append(tmp3)
   # tmp3.start()
    tmp4 = threading.Thread(target = deploy_threads, args=(4, lambda: stop_threads, maze, startRow+1, startColumn))
    threads.append(tmp4)
    #tmp4.start()
    
    for threads in threads:
        threads.start()
        stop_threads = True
        threads.join()
    sys.exit()

if __name__ == '__main__':
    myMaze = Maze('maze2.txt')
    searchFrom(myMaze, myMaze.startRow, myMaze.startCol)