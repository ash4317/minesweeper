from random import sample
from math import ceil

def printGrid(grid):
    for i in range(len(grid)):
        for j in range(len(grid)):
            print(grid[i][j], end=" ")
        print("\n")

def generateNumbers(grid, mineCoords):
    """Fill those cells which have mines surrounding them.
       Fill it with a number indicating no. of mines surrounding it."""
    
    #Loop through all mine locations
    for mine in mineCoords:
        #Add 1 to all the 8 surrounding cells of the mine
        #print(f"Mine: {mine}")
        for i in range(mine[0]-1, mine[0]+2):
            for j in range(mine[1]-1, mine[1]+2):
                if i in range(0, len(grid)) and j in range(0, len(grid)):
                    if (i, j) == mine:
                        grid[i][j] = -1
                        continue
                #if the cell is not a mine, increment by 1
                    if grid[i][j] != -1:
                        grid[i][j] += 1
        #printGrid(grid)
    #print("Final:")
    return grid

def generateMines(size):
    """Generate mines and locate them randomly on the grid"""
    nos = sample(range(1, size ** 2), ceil((size ** 2)/8))  #No. of mines = 20% of the cells
    mineCoords = [(int(i/size), i%size) for i in nos]
    #print(mineCoords)
    return mineCoords

def revealBlankCells(grid, clicked):
    """When a blank cell is clicked, reveal the sequence of cells near this cell which are empty or a number.
       This function uses 'Swarm searching' which keeps on searching for the goal in all the 8 directions."""
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

def generateGrid(size):
    grid = list()
    for i in range(size):
        grid.append(list())
        for j in range(size):
            grid[i].append(0)
    mines = generateMines(size)
    grid = generateNumbers(grid, mines)
    return grid, mines


def test():
    """Test case"""
    grid = list()
    for i in range(8):
        grid.append(list())
        for j in range(8):
            grid[i].append(0)
    grid = generateNumbers(grid, generateMines(8))
    #printGrid(grid)
    return grid
