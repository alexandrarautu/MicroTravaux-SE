"""

Premiere partie du code. Creation de l'interface grafique de base. 

"""

class Maze:
    def __init__(self,mazeFileName):
        rowsInMaze = 0
        columnsInMaze = 0
        self.mazelist = []
        mazeFile = open(mazeFileName,'r')
        rowsInMaze = 0
        for line in mazeFile:
            rowList = []
            col = 0
            for ch in line[:-1]:  #Renvoie tous les elements [:] sauf le dernier -1, qui est \n
                rowList.append(ch)  
                if ch == 'S':	# on determine la position initiale
                    self.startRow = rowsInMaze
                    self.startCol = col
                col = col + 1
            rowsInMaze = rowsInMaze + 1
            self.mazelist.append(rowList)
            columnsInMaze = len(rowList)
			

maze = Maze('maze2.txt')
for x in maze.mazelist:
    print x
