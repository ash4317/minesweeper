import sys, pygame
pygame.init()

screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w - 200, screen_info.current_h - 100
screen = pygame.display.set_mode(size=(screen_width, screen_height))

gray = (153, 153, 153)
run = True

def getInitialPosition(rows, cols, height, width):
    """Sets the top-left corner position of the grid"""
    extraSpaceVertical, extraSpaceHorizontal = screen_height % rows, screen_width % cols
    return int(extraSpaceVertical/2), int(extraSpaceHorizontal/2)


def drawGrid(rows, cols, height, width, color):
    """Draws the grid"""
    top, left = getInitialPosition(rows, cols, height, width)   #get the top-left position of the grid

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
        h, w = int((screen_height - 7)/8), int((screen_width - 14)/15)
        drawGrid(8, 15, h, w, gray)
        pygame.display.update()

    pygame.quit()