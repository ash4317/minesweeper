import sys, pygame
from algos import *
pygame.init()

screen_info = pygame.display.Info()
screen_width, screen_height = 1200, 880 #880x880 is the grid dimension. 880 is a common multiple of the different grid size 8, 16, 20
screen = pygame.display.set_mode(size=(screen_width, screen_height))

gridWidth = 880

#Colors
white = (255, 255, 255)
gray = (110, 110, 110)
black = (0, 0, 0)
lightGreen = (164, 238, 164)
lightYellow = (255, 255, 174)
orange = (255, 200, 130)
lightRed = (255, 120, 70)
mediumRed = (255, 70, 20)
red = (255, 10, 10)

run = True

visited = set()

def setColor(val):
    """Return color corresponding to cell value"""
    if val == 1:
        return lightGreen
    elif val == 2:
        return lightYellow
    elif val == 3:
        return orange
    elif val == 4:
        return lightRed
    elif val == 5:
        return mediumRed
    elif val == 6:
        return red
    else:
        return gray

def drawGrid(size, side):
    """Draws the grid"""
    left, top = 0, 0
    color = white

    #Loop through the grid area
    for i in range(size):
        top = (i * side) + (1 * i)    #space of 1px between adjacent cells
        for j in range(size):
            left = (j * side) + (1 * j)    #space of 1px between adjacent cells
            
            #if cell is visited
            if (i, j) in visited:
                color = setColor(grid[i][j])    #Get color of the cell
                pygame.draw.rect(screen, color, pygame.Rect(left, top, side, side))
                font = pygame.font.SysFont('Comic Sans MS', 30) #set font
                text = font.render(str(grid[i][j]), True, black)
                textRect = text.get_rect()
                cellCenter = (j * (side+1) + (side/2), i * (side+1) + (side/2)) #set the cell center of the text surface
                textRect.center = cellCenter
                screen.blit(text, textRect) #Display the text surface
            #if cell is not visited
            else:
                pygame.draw.rect(screen, white, pygame.Rect(left, top, side, side))

def revealCell(cursor, side, grid):
    #left = cursor[0] - (cursor[0] % (width+1))
    #top = cursor[1] - (cursor[1] % (height+1))
    (i, j) = (int(cursor[1]/(side+1)), int(cursor[0]/(side+1))) #coordinates of the cell
    global visited

    font = pygame.font.SysFont('Comic Sans MS', 30) #set font

    if grid[i][j] == 0:
        visited = visited.union(revealBlankCells(grid, (i, j)))

    text = font.render(str(grid[i][j]), True, black)
    textRect = text.get_rect()
    cellCenter = (j * (side+1) + (side/2), i * (side+1) + (side/2)) #set the cell center of the text surface
    textRect.center = cellCenter
    screen.blit(text, textRect)
    visited.add((i, j)) #add cell to visited


if __name__ == "__main__":
    visited = set()
    gridSize = 20   #Square grid 
    side = screen_height/gridSize - 1   #-1 is done to account for the spacing between adjacent cells
    grid = generateGrid(gridSize)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                revealCell(pygame.mouse.get_pos(), side, grid)
        drawGrid(gridSize, side)
        pygame.display.update()

    pygame.quit()