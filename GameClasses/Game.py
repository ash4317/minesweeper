from GameClasses.Grid import Grid

class Game:
    """
    Consists of the running state and status of the ongoing game.
    """

    def __init__(self):
        self.__status = "ongoing"
        self.__run_state = True
    
    def get_run_state(self):
        return self.__run_state
    
    def reset_run__state(self):
        self.__run_state = False
    
    def get_status(self):
        return self.__status
    
    def set_status(self, status:str):
        self.__status = status
    
    def is_game_won(self, grid:Grid) -> bool:
        """
        Returns true if game is won. False if game is lost or is ongoing.
        A game is won only if all cells that are not mines are visited AND all mines are flagged.
        """
        
        for mine_x, mine_y in grid.get_mine_coordinates():
            # Check if every mine is flagged
            if not grid.get_grid()[mine_x][mine_y].is_flagged():
                return False
            
        # If every mine is flagged and rest of the cells are visited, then game is won
        if len(grid.get_visited_cells()) != (grid.get_grid_size() ** 2) - grid.get_no_of_mines():
            return False
        return True