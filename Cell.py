class Cell:
    """
    Every grid is made up of these Cell objects.
    """

    def __init__(self, type:str, number:int, size:int=0):
        """
        type: whether cell is a "mine", "number", "blank" or "flagged"
        number: number of mines around the cell (-1 for a mine cell)
        cell_size: dimensions of the cell to be drawn in the grid
        visited: whether the cell is visited or not
        flagged: whether the cell is flagged or not
        """
        self.__type = type
        self.__number = number
        self.__cell_size = size
        self.__visited = False
        self.__flagged = False
    
    def get_number(self) -> int: return self.__number

    def increment_number(self): self.__number += 1

    def decrement_number(self): self.__number -= 1

    def get_type(self) -> str: return self.__type

    def set_type(self, type:str): self.__type = type

    def is_flagged(self) -> bool: return self.__flagged

    def set_flagged(self): self.__flagged = True

    def reset_flagged(self): self.__flagged = False

    def is_visited(self) -> bool: return self.__visited

    def set_visited(self): self.__visited = True

    def get_cell_size(self) -> int: return self.__cell_size