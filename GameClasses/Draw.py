import pygame
from GameClasses.Color import Color
from GameClasses.Grid import Grid

class Draw:
    """
    Class for drawing anything on the grid
    """

    def __init__(self, screen:pygame.Surface):
        self.__screen = screen

    def draw_grid(self, grid:list):
        """Draws the grid"""
        left, top = 0, 0
        color_object = Color()
        color = color_object.WHITE
        cell_size = grid[0][0].get_cell_size()
        grid_size = len(grid)

        # Loop through the grid area
        for i in range(grid_size):
            top = i * (cell_size + 1)   # Space of 1px between adjacent cells
            for j in range(grid_size):
                left = j * (cell_size + 1)    # Space of 1px between adjacent cells

                if grid[i][j].is_visited():
                    # If cell is visited
                    if grid[i][j].get_type() != "mine":
                        # If cell is not a mine
                        color = color_object.COLORS_LIST[grid[i][j].get_number()]    # Get color of the cell
                        
                        pygame.draw.rect(
                            self.__screen, 
                            color, 
                            pygame.Rect(left, top, cell_size, cell_size)
                        )   # Fill the cell with the given background color

                        if grid[i][j].get_type() == "number":
                            # If the cell is a number, write the number on the cell
                            font = pygame.font.SysFont('Comic Sans MS', 30) # Set font
                            text = font.render(
                                str(grid[i][j].get_number()), 
                                True, 
                                color_object.BLACK
                            )
                            text_rectangle = text.get_rect()
                            cell_center = (int(j * (cell_size + 1) + (cell_size / 2)), int(i * (cell_size + 1) + (cell_size / 2))) # Set the cell center of the text surface
                            text_rectangle.center = cell_center
                            self.__screen.blit(text, text_rectangle) # Display the text surface

                    else:
                        # If cell is a mine, draw the mine image on the cell
                        mine_image = pygame.image.load("images/mine.jpeg").convert()
                        mine_image = pygame.transform.scale(
                            mine_image, 
                            (cell_size, cell_size)
                        )   # Change size of img = cell width
                        img_coords = (j * (cell_size + 1), i * (cell_size + 1))   # Coords of top-left corner of cell
                        self.__screen.blit(mine_image, img_coords) # Display the image at the specified coords

                elif grid[i][j].is_flagged():
                    # If cell is flagged, draw the flag image on the cell
                    flag_image = pygame.image.load("images/flag.png").convert()
                    flag_image = pygame.transform.scale(
                        flag_image, 
                        (cell_size, cell_size)
                    )   # Change size of img = cell width
                    img_coords = (j * (cell_size + 1), i * (cell_size + 1))   # Coords of top-left corner of cell
                    self.__screen.blit(flag_image, img_coords)   # Display the image at the specified coords

                else:
                    # If cell is not yet visited, fill the cell with white color
                    pygame.draw.rect(
                        self.__screen, 
                        color_object.WHITE, 
                        pygame.Rect(left, top, cell_size, cell_size)
                    )
      

    def draw_menu(self, game_status:str, grid:Grid):
        """Draws the score, no. of flagged cells etc."""

        color_object = Color()
        pygame.draw.rect(
            self.__screen, 
            color_object.BLACK, 
            pygame.Rect(
                grid.get_grid_width(), 
                0, 
                self.__screen.get_width() - grid.get_grid_width(), 
                self.__screen.get_height()
            )
        )
        font = pygame.font.SysFont('freesans', 30) # Set font
        text = font.render("Flagged: " + str(len(grid.get_flagged_cells())) + "/" + str(len(grid.get_mine_coordinates())), True, color_object.WHITE)
        text_rectangle = text.get_rect()
        text_rectangle.center = (1000, 400)
        self.__screen.blit(text, text_rectangle)

        if game_status == "lost":
            # If game over (game_status == "lost"), show "GAME OVER"
            font = pygame.font.SysFont('freesans', 30) # Set font
            text = font.render("GAME OVER", True, color_object.WHITE)
            text_rectangle = text.get_rect()
            text_rectangle.center = (1000, 200)
            self.__screen.blit(text, text_rectangle)
        elif game_status == "won":
            # If game is won (game_status == "won"), show "YOU WON"
            font = pygame.font.SysFont('freesans', 30) # Set font
            text = font.render("YOU WON!", True, color_object.WHITE)
            text_rectangle = text.get_rect()
            text_rectangle.center = (1000, 200)
            self.__screen.blit(text, text_rectangle)