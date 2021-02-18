from random import sample
from math import ceil

def generateNumbers(grid, mineCoords):
    """Fill those cells which have mines surrounding them.
       Fill it with a number indicating no. of mines surrounding it."""
    
    #Loop through all mine locations
    for mine in mineCoords:
        #Add 1 to all the 8 surrounding cells of the mine
        for i in range(mine[0]-1, mine[0]+2):
            for j in range(mine[1]-1, mine[1]+2):
                if (i, j) == mine:
                    grid[i][j] = -1
                    continue
                #if the array position is valid, then increment by 1. Else, continue
                try:
                    if grid[i][j] != -1:
                        grid[i][j] += 1
                except:
                    continue
    return grid

def generateMines(side):
    """Generate mines and locate them randomly on the grid"""
    nos = sample(range(0, side ** 2), ceil((side ** 2)/5))  #No. of mines = 20% of the cells
    mineCoords = [(int(i/side), i%side) for i in nos]
    #print(mineCoords)
    return mineCoords

def revealBlankCells(grid, clicked):
    """When a blank cell is clicked, reveal the sequence of cells near this cell which are empty or a number"""
    frontier = list()   #Stack frontier
    visited = set()     #Visited set to keep a record of visited cells
    frontier.append(clicked)
    visited.add(clicked)

    while len(frontier) > 0:
        current = frontier.pop()
        #Loop through all 8 adjacent cells
        for i in range(current[0]-1, current[0]+2):
            for j in range(current[1]-1, current[1]+2):
                #if index is within the grid
                if i in range(0, len(grid)) and j in range(0, len(grid)):
                    #if (i,j) is the current cell or it is a mine or it is already visited
                    if (i, j) == current or grid[i][j] == -1 or (i, j) in visited:
                        continue
                    #if cell is blank, reveal it and explore its surrounding
                    if grid[i][j] == 0:
                        frontier.append((i, j))
                        visited.add((i, j))
                    #if cell is a number, only visit it
                    else:
                        visited.add((i, j))
    return visited

def test():
    """Test case"""
    grid = list()
    for i in range(16):
        grid.append(list())
        for j in range(16):
            grid[i].append(0)
    grid = generateNumbers(grid, generateMines(16))
    for i in range(len(grid)):
        for j in range(len(grid)):
            print(grid[i][j], end=" ")
        print("\n")
    return grid