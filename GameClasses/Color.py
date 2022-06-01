class Color:
    """
    Consists of the cell colors for every numbered or blank or unvisited cell
    """

    def __init__(self):
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        WHITESMOKE = (220, 220, 220)
        LIGHT_GREEN = (164, 238, 164)
        LIGHT_YELLOW = (255, 255, 174)
        ORANGE = (255, 200, 130)
        LIGHT_RED = (255, 120, 70)
        MEDIUM_RED = (255, 70, 20)
        RED = (255, 10, 10)
        self.COLORS_LIST = [WHITESMOKE, LIGHT_GREEN, LIGHT_YELLOW, ORANGE, LIGHT_RED, MEDIUM_RED, RED]