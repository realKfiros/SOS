from kivy.app import App

NONE = 0
S = 1
O = 2


class Action:
    """
    The class for an action, needed for the ai turns
    """
    def __init__(self, let, dist, instance):
        """
        :param let: the letter to put (:keyword: S or :keyword: O)
        :param instance: needed for the kivy
        """
        self.let = let
        self.dist = dist
        self.instance = instance

    def take(self):
        """
        :return: puts on the board the selection of the computer
        """
        if self.let == S:
            App.get_running_app().game.board.currentturn.s()
        elif self.let == O:
            App.get_running_app().game.board.currentturn.o()
        App.get_running_app().game.board.on_release(self.instance)