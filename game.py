import sys, pygame
pygame.init()

screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w - 200, screen_info.current_h - 100
screen = pygame.display.set_mode(size=(screen_width, screen_height))

gray = (153, 153, 153)
run = True

top, left = 0, 0
rectSide = 60

def drawGrid(rows, cols, side, color):
    for i in range(rows):
        top = (i * side) + (3 * i)
        for j in range(cols):
            left = (j * side) + (3 * j)
            pygame.draw.rect(screen, color, pygame.Rect(left, top, side, side))


if __name__ == "__main__":
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        drawGrid(16, 30, rectSide, gray)
        pygame.display.update()

    pygame.quit()