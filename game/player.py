class Player:
    """
    The class of the player.
    """
    def __init__(self, name, first):
        """
        :param name: the name of the player
        :param first: True if he's first in the game
        """
        self.name = name
        self.starter = first
        self.now = True if self.starter else False
