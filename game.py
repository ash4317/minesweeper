import sys, pygame
pygame.init()

screen_info = pygame.display.Info()
screen_width, screen_height = 1200, 880 #880x880 is the grid dimension. 880 is a common multiple of the different grid size 8, 16, 20
screen = pygame.display.set_mode(size=(screen_width, screen_height))

gridWidth = 880
gridRows, gridCols = 16, 16

white = (255, 255, 255)
run = True

def drawGrid(rows, cols, height, width, color):
    """Draws the grid"""
    left, top = 0, 0

    for i in range(rows):
        top = (i * height) + (1 * i)    #space of 1px between adjacent cells
        for j in range(cols):
            left = (j * width) + (1 * j)    #space of 1px between adjacent cells
            pygame.draw.rect(screen, color, pygame.Rect(left, top, width, height))


if __name__ == "__main__":
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        height, width = screen_height/gridRows - 1, gridWidth/gridCols - 1  #-1 is done to account for the spacing between adjacent cells
        drawGrid(gridRows, gridCols, height, width, white)
        pygame.display.update()

    pygame.quit()