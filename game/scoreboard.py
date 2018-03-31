from kivy.app import App
from kivy.event import EventDispatcher
from kivy.properties import NumericProperty


class Scoreboard(EventDispatcher):
    """
    The class of the points on the scoreboard.
    """
    player1points = NumericProperty(0) # The points of player 1, the value is 0 when the game starts
    player2points = NumericProperty(0) # the points of player 2, the value is 0 when the game starts
    def on_player1points(self, instance, value):
        """
        executed when the points of player 1 change
        :param instance: needed for the kivy
        :param value: the new value
        :return: changes the number of points in the graphics
        """
        app = App.get_running_app()
        app.game.player1points.text = str(value)

    def on_player2points(self, instance, value):
        """
        executed when the points of player 2 change
        :param instance: needed for the kivy
        :param value: the new value
        :return: changes the number of points in the graphics
        """
        app = App.get_running_app()
        app.game.player2points.text = str(value)
