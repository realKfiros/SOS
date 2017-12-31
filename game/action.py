from kivy.app import App

NONE = 0
S = 1
O = 2


class Action:
    def __init__(self, let, dist, instace):
        self.let = let
        self.dist = dist
        self.instace = instace

    def take(self):
        if self.let == S:
            App.get_running_app().game.board.currentturn.s()
        elif self.let == O:
            App.get_running_app().game.board.currentturn.o()
        App.get_running_app().game.board.on_release(self.instace)