import pygame
from random import sample
from math import ceil
from Color import Color
from Cell import Cell

class Grid:
    """
    Main grid where the game takes place.
    """

    def __init__(self, grid_size, grid_width, cell_size):
        """
        grid_size: order of the grid matrix
        grid_width: width of the grid that is drawn on the pygame screen
        grid: 2D matrix that consists of all the cells
        mine_coordinates: locations of all the mines on the grid
        visited_cells: set of all the visited cells on the grid
        flagged_cells: set of all the flagged cells on the grid
        """
        self.__grid_size = grid_size
        self.__grid_width = grid_width
        self.__grid, self.__mine_coordinates = self.generate_grid(cell_size)
        self.__visited_cells = set()
        self.__flagged_cells = set()

    
    def generate_grid(self, cell_size:int):
        """
        Generates the grid and fills it with mines and numbers
        """
        grid = list()
        for i in range(self.__grid_size):
            grid.append(list())
            for j in range(self.__grid_size):
                grid[i].append(Cell("blank", 0, cell_size)) #Add a blank cell at every grid location
        
        
        #Generate mines and locate them randomly on the grid
        random_numbers = sample(range(1, self.__grid_size ** 2), ceil((self.__grid_size ** 2) / 8))  #No. of mines = 12.5% of the cells
        mine_coordinates = [(int(i / self.__grid_size), i % self.__grid_size) for i in random_numbers]


        """
        Fill those cells which have mines surrounding them.
        Fill it with a number indicating no. of mines surrounding it.
        """

        #Loop through all mine locations
        for mine in mine_coordinates:
            #Add 1 to all the 8 surrounding cells of the mine
            for i in range(mine[0] - 1, mine[0] + 2):
                for j in range(mine[1] - 1, mine[1] + 2):
                    if i in range(0, len(grid)) and j in range(0, len(grid)):
                        #If (i,j) is in the grid
                        if (i, j) == mine:
                            #If cell is a mine, decrement the number of the cell to make it -1, and set type of cell to "mine"
                            grid[i][j].decrement_number()
                            grid[i][j].set_type("mine")
                            continue

                        if grid[i][j].get_type() != "mine":
                            #If cell is not a mine, increment the number of the cell, and set its type to "number"
                            grid[i][j].increment_number()
                            grid[i][j].set_type("number")
        
        return grid, mine_coordinates
    

    def draw_grid(self, screen:pygame.Surface):
        """Draws the grid"""
        left, top = 0, 0
        color_object = Color()
        color = color_object.WHITE
        cell_size = self.__grid[0][0].get_cell_size()

        #Loop through the grid area
        for i in range(self.__grid_size):
            top = i * (cell_size + 1)   #Space of 1px between adjacent cells
            for j in range(self.__grid_size):
                left = j * (cell_size + 1)    #Space of 1px between adjacent cells

                if self.__grid[i][j].is_visited():
                    #If cell is visited
                    if self.__grid[i][j].get_type() != "mine":
                        #If cell is not a mine
                        color = color_object.COLORS_LIST[self.__grid[i][j].get_number()]    #Get color of the cell
                        pygame.draw.rect(screen, color, pygame.Rect(left, top, cell_size, cell_size))   #Fill the cell with the given background color

                        if self.__grid[i][j].get_type() == "number":
                            #If the cell is a number, write the number on the cell
                            font = pygame.font.SysFont('Comic Sans MS', 30) #Set font
                            text = font.render(str(self.__grid[i][j].get_number()), True, color_object.BLACK)
                            text_rectangle = text.get_rect()
                            cell_center = (int(j * (cell_size + 1) + (cell_size / 2)), int(i * (cell_size + 1) + (cell_size / 2))) #Set the cell center of the text surface
                            text_rectangle.center = cell_center
                            screen.blit(text, text_rectangle) #Display the text surface

                    else:
                        #If cell is a mine, draw the mine image on the cell
                        mine_image = pygame.image.load("images/mine.jpeg").convert()
                        mine_image = pygame.transform.scale(mine_image, (cell_size, cell_size))   #Change size of img = cell width
                        img_coords = (j * (cell_size + 1), i * (cell_size + 1))   #Coords of top-left corner of cell
                        screen.blit(mine_image, img_coords) #Display the image at the specified coords

                elif self.__grid[i][j].is_flagged():
                    #If cell is flagged, draw the flag image on the cell
                    flag_image = pygame.image.load("images/flag.png").convert()
                    flag_image = pygame.transform.scale(flag_image, (cell_size, cell_size))   #Change size of img = cell width
                    img_coords = (j * (cell_size + 1), i * (cell_size + 1))   #Coords of top-left corner of cell
                    screen.blit(flag_image, img_coords)   #Display the image at the specified coords

                else:
                    #If cell is not yet visited, fill the cell with white color
                    pygame.draw.rect(screen, color_object.WHITE, pygame.Rect(left, top, cell_size, cell_size))
        

    def reveal_blank_cells(self, clicked_cell_coordinates) -> set:
        """
        When a blank cell is clicked, reveal the sequence of cells near this cell which are empty or a number. This function uses 'Swarm searching' which keeps on searching for the goal in all the 8 directions.
        Returns a set of cells that are revealed because of the swarm search.
        """
        frontier = list()   #Stack frontier
        visited_cells = set()     #Visited set to keep a record of visited cells
        frontier.append(clicked_cell_coordinates)
        visited_cells.add(clicked_cell_coordinates)


        while len(frontier) > 0:
            current_cell = frontier.pop()

            #Loop through all 8 adjacent cells
            for i in range(current_cell[0] - 1, current_cell[0] + 2):
                for j in range(current_cell[1] - 1, current_cell[1] + 2):
                    if i in range(0, len(self.__grid)) and j in range(0, len(self.__grid)):
                        #If index is within the grid
                        if (i, j) == current_cell or self.__grid[i][j].get_type() == "mine" or self.__grid[i][j].is_flagged() or self.__grid[i][j].is_visited():
                            #If (i,j) is either the current cell, or it is a mine, or it is already visited, or it is flagged, then do nothing and continue
                            continue
            
                        if self.__grid[i][j].get_type() == "blank":
                            #If cell is blank, reveal it and add its surrounding cells to the frontier. If cell is a number, only visit it and don't add surrounding cells to the frontier
                            frontier.append((i, j))
                        
                        #Add the cell to visited_cells set and mark it as visited
                        visited_cells.add((i, j))
                        self.__grid[i][j].set_visited()
        return visited_cells
    

    def draw_menu(self, screen:pygame.Surface, game_status):
        """Draws the score, no. of flagged cells etc."""

        color_object = Color()
        pygame.draw.rect(screen, color_object.BLACK, pygame.Rect(self.__grid_width, 0, screen.get_width() - self.__grid_width, screen.get_height()))
        font = pygame.font.SysFont('freesans', 30) #Set font
        text = font.render("Flagged: " + str(len(self.__flagged_cells)) + "/" + str(len(self.__mine_coordinates)), True, color_object.WHITE)
        text_rectangle = text.get_rect()
        text_rectangle.center = (1000, 400)
        screen.blit(text, text_rectangle)

        if game_status == "lost":
            #If game over (game_status == "lost"), show "GAME OVER"
            font = pygame.font.SysFont('freesans', 30) #Set font
            text = font.render("GAME OVER", True, color_object.WHITE)
            text_rectangle = text.get_rect()
            text_rectangle.center = (1000, 200)
            screen.blit(text, text_rectangle)
        elif game_status == "won":
            #If game is won (game_status == "won"), show "YOU WON"
            font = pygame.font.SysFont('freesans', 30) #Set font
            text = font.render("YOU WON!", True, color_object.WHITE)
            text_rectangle = text.get_rect()
            text_rectangle.center = (1000, 200)
            screen.blit(text, text_rectangle)
    

    def reveal_mines(self):
        """Displays all the mines on the grid"""

        #Just add all the mines into the visited_cells property of the class. draw_grid() method of this class will then draw all mines
        for mine_x, mine_y in self.__mine_coordinates:
            if not self.__grid[mine_x][mine_y].is_flagged():
                self.__visited_cells.add(self.__grid[mine_x][mine_y])
                self.__grid[mine_x][mine_y].set_visited()


    def reveal_cell(self, cell_coord_x, cell_coord_y, screen:pygame.Surface):
        """Shows the cell when it is clicked, returns cell object"""

        color_object = Color()
        cell = self.__grid[cell_coord_x][cell_coord_y]

        font = pygame.font.SysFont('dejavuserif', 30) #Set font

        if not cell.is_flagged():
            #If the cell is not flagged

            if cell.get_type() == "mine":
                #If clicked cell is a mine, then game over and reveal all the mines
                return Cell("mine", -1)
            else:
                self.__visited_cells.add((cell_coord_x, cell_coord_y))
                self.__grid[cell_coord_x][cell_coord_y].set_visited()

                #If clicked cell is a blank cell, then reveal blank cells surrounding it
                if cell.get_type() == "blank":
                    return Cell("blank", 0)
                else:
                    return Cell("number", self.__grid[cell_coord_x][cell_coord_y].get_number())

        else:
            return Cell("flagged", 0)
                
    
    def get_cell_index(self, cursor_coordinates):
        """Returns the cell index (in the grid) of the clicked cell"""

        cell_size = self.__grid[0][0].get_cell_size()
        if cursor_coordinates[0] >= self.__grid_width:
            return (-1, -1)
        return (int(cursor_coordinates[1] / (cell_size + 1)), int(cursor_coordinates[0] / (cell_size + 1)))
        
    
    def get_flagged_cells(self) -> set: return self.__flagged_cells

    def get_visited_cells(self) -> set: return self.__visited_cells

    def set_visited_cells(self, visited_cells): self.__visited_cells = visited_cells

    def get_mine_coordinates(self) -> list: return self.__mine_coordinates

    def get_no_of_mines(self) -> int: return len(self.__mine_coordinates)

    def get_grid(self) -> list: return self.__grid

    def get_grid_size(self) -> int: return self.__grid_size