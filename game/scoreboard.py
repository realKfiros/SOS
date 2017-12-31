from kivy.app import App
from kivy.event import EventDispatcher
from kivy.properties import NumericProperty


class Scoreboard(EventDispatcher):
    player1points = NumericProperty(0)
    player2points = NumericProperty(0)
    def on_player1points(self, instace, value):
        app = App.get_running_app()
        app.game.player1points.text = str(value)

    def on_player2points(self, instace, value):
        app = App.get_running_app()
        app.game.player2points.text = str(value)
