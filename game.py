import sys, pygame
pygame.init()

screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w - 200, screen_info.current_h - 100
screen = pygame.display.set_mode(size=(screen_width, screen_height))

gridWidth = screen_width - 500
gridRows, gridCols = 8, 8

gray = (153, 153, 153)
white = (255, 255, 255)
run = True

def getInitialPosition(rows, cols, height, width):
    """Sets the top-left corner position of the grid"""
    extraSpaceVertical, extraSpaceHorizontal = screen_height % rows, screen_width % cols
    return (int(extraSpaceHorizontal/2), int(extraSpaceVertical/2))


def drawGrid(rows, cols, height, width, color):
    """Draws the grid"""
    initialPosition = getInitialPosition(rows, cols, height, width) #get the top-left position of the grid
    left, top = initialPosition[0], initialPosition[1]

    for i in range(rows):
        top = (i * height) + (1 * i)    #space of 1px between adjacent blocks
        for j in range(cols):
            left = (j * width) + (1 * j)    #space of 1px between adjacent blocks
            pygame.draw.rect(screen, color, pygame.Rect(left, top, width, height))


if __name__ == "__main__":
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        height, width = int((screen_height - 7)/8), int((screen_width - 7 - 500)/8)
        drawGrid(gridRows, gridCols, height, width, gray)
        pygame.display.update()

    pygame.quit()