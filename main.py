import sys, pygame
from GameClasses.Game import Game
from GameClasses.Cell import Cell
from GameClasses.Grid import Grid
from GameClasses.Draw import Draw
from math import ceil

# Initialize the pygame app
pygame.init()

# Initialize screen dimensions
screen_info = pygame.display.Info()
screen_width, screen_height = 1200, 800 # 800x800 is the grid dimension.
screen = pygame.display.set_mode(size=(screen_width, screen_height))


if __name__ == "__main__":

    # grid_size: Size of the grid (no. of rows), cell_size: length of cell side
    grid_size = int(sys.argv[1])   # Square grid
    cell_size = int(screen_height / (grid_size)) - 1   # -1 is done to account for the spacing between adjacent cells

    # Initialize a Game and Grid object
    game = Game()
    grid = Grid(
        grid_size=grid_size, 
        grid_width=800, 
        cell_size=cell_size
    )
    draw = Draw(screen)

    while game.get_run_state():
        # While game is running (close button of window isn't clicked)

        # Loop through the events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                # If pygame window is closed
                game.reset_run__state()

            if game.get_status() == "ongoing":
                "Game is running"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If mouse is clicked

                    # Get cursor position and convert it to cell index in the grid
                    cursor_coordinates = pygame.mouse.get_pos()
                    (cell_coord_x, cell_coord_y) = grid.get_cell_index(cursor_coordinates)

                    if pygame.mouse.get_pressed() == (True, False, False):
                        # If left mouse button is clicked
                        cell = grid.reveal_cell(
                            cell_coord_x, 
                            cell_coord_y, 
                            screen
                        ) # Reveal the cell

                        if cell.get_type() == "mine":
                            # Game is lost. Show all the mines on the grid
                            grid.reveal_mines()
                            game.set_status("lost")
                        elif cell.get_type() == "blank":
                            # If blank, reveal all blank cells near it, and mark them as visited
                            visited_cells = grid.get_visited_cells()
                            visited_cells = visited_cells.union(
                                grid.reveal_blank_cells((cell_coord_x, cell_coord_y))
                            )
                            grid.set_visited_cells(visited_cells)
                        elif cell.get_type() == "number":
                            # If number, just mark it as visited
                            visited_cells = grid.get_visited_cells()
                            visited_cells.add((cell_coord_x, cell_coord_y))
                            grid.set_visited_cells(visited_cells)
                            
                    elif pygame.mouse.get_pressed() == (False, False, True):
                        # If right mouse button is clicked

                        clicked_cell = grid.get_grid()[cell_coord_x][cell_coord_y]

                        if not clicked_cell.is_visited():
                            # Flag the cell only if it is not visited
                            if not clicked_cell.is_flagged():
                                # If it isn't flagged, then flag it
                                if len(grid.get_flagged_cells()) < grid.get_no_of_mines():
                                    # Number of flags allowed = number of mines. Hence, if already that many cells are flagged, don't flag it
                                    grid.get_flagged_cells().add((cell_coord_x, cell_coord_y))
                                    clicked_cell.set_flagged()  # Set flagged property of cell
                            else:
                                # If it is already flagged, unflag it
                                grid.get_flagged_cells().remove((cell_coord_x, cell_coord_y))
                                clicked_cell.reset_flagged()    # Reset flagged property of cell

                    flagged_cells = grid.get_flagged_cells()
                    if len(flagged_cells) == grid.get_no_of_mines():
                        # If no. of flagged cells = no. of mines, check if game is won
                        if game.is_game_won(grid):
                            game.set_status("won")

        draw.draw_grid(grid.get_grid()) # Draw the grid
        draw.draw_menu(game.get_status(), grid)  # Draw the menu
        pygame.display.update() # Update the display

    pygame.quit()
