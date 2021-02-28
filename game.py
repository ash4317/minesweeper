import sys, pygame
from algos import *
from math import ceil
pygame.init()

screen_info = pygame.display.Info()
screen_width, screen_height = 1200, 880 #880x880 is the grid dimension. 880 is a common multiple of the different grid size 8, 16, 20
screen = pygame.display.set_mode(size=(screen_width, screen_height))

gridWidth = 880
noOfFlagged = 0
mines = 0

#Colors
white = (255, 255, 255)
whitesmoke = (220, 220, 220)
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
flagged = set()

def getCoords(cursor, side):
    """Returns the cell number of the clicked cell"""
    if cursor[0] >= gridWidth:
    	return (-1, -1)
    return (int(cursor[1]/(side+1)), int(cursor[0]/(side+1)))

def setColor(val):
    """Return color corresponding to cell value"""
    if val == 0:
        return whitesmoke
    elif val == 1:
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
                #if cell != 0, display the number
                if grid[i][j] != 0:
                    font = pygame.font.SysFont('Comic Sans MS', 30) #set font
                    text = font.render(str(grid[i][j]), True, black)
                    textRect = text.get_rect()
                    cellCenter = (j * (side+1) + (side/2), i * (side+1) + (side/2)) #set the cell center of the text surface
                    textRect.center = cellCenter
                    screen.blit(text, textRect) #Display the text surface

            #if cell is flagged
            elif (i, j) in flagged:
                font = pygame.font.SysFont('Comic Sans MS', 30) #set font
                text = font.render('F', True, black)
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
    (i, j) = getCoords(cursor, side) #coordinates of the cell
    global visited

    font = pygame.font.SysFont('dejavuserif', 30) #set font

    #if the cell is not flagged
    if (i, j) not in flagged:
        if grid[i][j] == 0:
            visited = visited.union(revealBlankCells(grid, (i, j)))

        text = font.render(str(grid[i][j]), True, black)
        textRect = text.get_rect()
        cellCenter = (j * (side+1) + (side/2), i * (side+1) + (side/2)) #set the cell center of the text surface
        textRect.center = cellCenter
        screen.blit(text, textRect)
        visited.add((i, j)) #add cell to visited

def drawMenu(noOfFlagged):
    pygame.draw.rect(screen, black, pygame.Rect(880, 0, screen_width-gridWidth, screen_height))
    font = pygame.font.SysFont('freesans', 30) #set font
    text = font.render("Flagged: " + str(noOfFlagged) + "/" + str(mines), True, white)
    textRect = text.get_rect()
    textRect.center = (1000, 400)
    screen.blit(text, textRect)

if __name__ == "__main__":

    #gridSize: Size of the grid (no. of rows), side: length of cell side
    gridSize = 20   #Square grid 
    side = screen_height/gridSize - 1   #-1 is done to account for the spacing between adjacent cells
    mines = ceil((gridSize ** 2)/5)

    grid = generateGrid(gridSize)
    while run:

        #Loop through the events
        for event in pygame.event.get():

            #if pygame window is closed
            if event.type == pygame.QUIT:
                run = False
            
            #if mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                #if left mouse button is clicked
                if pygame.mouse.get_pressed() == (True, False, False):
                    revealCell(pygame.mouse.get_pos(), side, grid)
                #if right mouse button is clicked
                elif pygame.mouse.get_pressed() == (False, False, True):
                    cursor = pygame.mouse.get_pos()
                    coords = getCoords(cursor, side)

                    #only update no of flagged if it is not visited
                    if coords not in visited:
                        #if not flagged, then flag it
                        if coords not in flagged:
                            if noOfFlagged < mines:
                                flagged.add(coords)
                                noOfFlagged += 1
                        #if already flagged, unflag it
                        else:
                            flagged.remove(coords)
                            noOfFlagged -= 1

        drawGrid(gridSize, side)    #Draw the grid
        drawMenu(noOfFlagged)
        pygame.display.update()

    print("Thank you for playing!")
    pygame.quit()
