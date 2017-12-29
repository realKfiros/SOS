import random
import os
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.event import EventDispatcher
from kivy.properties import NumericProperty


NONE = 0
S = 1
O = 2


class Player:
    def __init__(self, name, first):
        self.name = name
        self.starter = first
        self.now = True if self.starter else False


class Scoreboard(EventDispatcher):
    player1points = NumericProperty(0)
    player2points = NumericProperty(0)
    def on_player1points(self, instace, value):
        app = App.get_running_app()
        app.game.player1points.text = str(value)

    def on_player2points(self, instace, value):
        app = App.get_running_app()
        app.game.player2points.text = str(value)


class Turn:
    def __init__(self, num):
        self.choice = NONE
        self.done = False
        self.num = num

    def s(self):
        self.choice = S

    def o(self):
        self.choice = O

    def put(self):
        self.done = True


class SOSPoint(Button):
    def __init__(self, x, y):
        super(Button, self).__init__()
        self.x = x
        self.y = y
        self.r = x
        self.c = y
        self.points = 0
        self.text = ""
        self.occupied = False
        self.font_size = 50

    def put_s(self):
        if not self.occupied:
            self.text = "s"
            self.occupied = True
            return True
        return False

    def put_o(self):
        if not self.occupied:
            self.text = "o"
            self.occupied = True
            return True
        return False


class SOSBoard(GridLayout):

    def __init__(self, player1, player2='CPU'):
        super(SOSBoard, self).__init__()

        self.ai = True if player2 == 'CPU' else False
        self.cols = 9
        self.rows = 9
        self.player1 = Player(player1, True)
        self.player2 = Player(player2, False)
        self.scoreboard = Scoreboard()
        self.grid = [[None for col in range(self.cols)] for row in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                tile = SOSPoint(row, col)
                self.grid[row][col] = tile
                tile.bind(on_release=self.on_release)
                self.add_widget(tile)
        self.currentturn=Turn(1)

    def s(self):
        self.currentturn.s()

    def o(self):
        self.currentturn.o()

    def done(self, tile):
        if self.currentturn.choice == NONE:
            return False
        elif tile.occupied:
            return False
        else:
            tile.text = self.on_done()
            return True

    def on_release(self, instace):
        if App.get_running_app().game.board.currentturn.choice == NONE:
            return
        if instace.text:
            return None
        self.done(instace)
        instace.disabled = True
        instace.disabled_color = (1,1,1,1)
        instace.background_disabled_normal = ''
        # instace.background_color = (0.207, 0.635, 0.423, 0.9)
        instace.background_color = (0.1, 0.2, 0.3, 0.6)
        currentnum = self.currentturn.num
        if currentnum%2 == 1:
            toadd = self.scoreboard.player1points + self.addpoints(instace)
            self.scoreboard.player1points = toadd
        else:
            toadd = self.scoreboard.player2points + self.addpoints(instace)
            self.scoreboard.player2points = toadd
        self.currentturn = Turn(currentnum+1)
        App.get_running_app().game.s_btn.background_color = (1, 1, 1, 1)
        App.get_running_app().game.o_btn.background_color = (1, 1, 1, 1)
        if self.ai and self.currentturn.num%2 == 0:
            turn = AITurn(self.currentturn.num)
            turn.doPriorityMove()
        if not self.ai:
            if self.currentturn.num % 2 == 0:
                App.get_running_app().game.whoplay.text = '{}`s turn'.format(App.get_running_app().game.player2name.text)
                App.get_running_app().game.whoplay.color = (1, 0, 0, 1)
            else:
                App.get_running_app().game.whoplay.text = '{}`s turn'.format(App.get_running_app().game.player1name.text)
                App.get_running_app().game.whoplay.color = (0, 0, 1, 1)

    def on_done(self):
        if self.currentturn.choice == S:
            return "S"
        elif self.currentturn.choice == O:
            return "O"

    def addpoints(self, instace):
        points = 0
        row = instace.r
        col = instace.c
        if row == 0 and col == 0:
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row+1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row+2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col+1].text == "O" and self.grid[row+2][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 0 and col == 1:
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col+1].text == "O" and self.grid[row+2][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 0 and 1 < col < 7:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col-1].text == "O" and self.grid[row+2][col-2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col+1].text == "O" and self.grid[row+2][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 0 and col == 7:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col-1].text == "O" and self.grid[row+2][col-2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 0 and col == 8:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col-1].text == "O" and self.grid[row+2][col-2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 1 and col == 0:
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col+1].text == "O" and self.grid[row+2][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 1 and col == 1:
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col+1].text == "S":
                points += 1
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col+1].text == "O" and self.grid[row+2][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row+1][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row-1][col+1].text == "S":
                points += 1
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 1 and 1 < col < 7:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col+1].text == "S":
                points += 1
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col+1].text == "O" and self.grid[row+2][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col+1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col-1].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col-1].text == "O" and self.grid[row+2][col-2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 1 and col == 7:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col+1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col-1].text == "S":
                points += 1
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col-1].text == "O" and self.grid[row+2][col-2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 1 and col == 8:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col-1].text == "O" and self.grid[row+2][col-2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
        elif 1 < row < 7 and col == 0:
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row-1][col+1].text == "O" and self.grid[row-2][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col+1].text == "O" and self.grid[row+2][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
        elif 1 < row < 7 and col == 1:
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row+1][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row-1][col+1].text == "S":
                points += 1
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row-1][col+1].text == "O" and self.grid[row-2][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col+1].text == "S":
                points += 1
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col+1].text == "O" and self.grid[row+2][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
        elif 1 < row < 7 and 1 < col < 7:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col-2].text == "S" and self.grid[row-1][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col+1].text == "S":
                points += 1
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col+1].text == "O" and self.grid[row+2][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col+2].text == "S" and self.grid[row-1][col+1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col+1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col-1].text == "S":
                points += 1
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col-1].text == "O" and self.grid[row+2][col-2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
        elif 1 < row < 7 and col == 7:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col-2].text == "S" and self.grid[row-1][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col+1].text == "S":
                points += 1
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col+1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col-1].text == "S":
                points += 1
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col-1].text == "O" and self.grid[row+2][col-2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
        elif 1 < row < 7 and col == 8:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row+1][col].text == "O" and self.grid[row+2][col].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col-2].text == "S" and self.grid[row-1][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row+2][col-2].text == "S" and self.grid[row+1][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row + 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 7 and col == 0:
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col+2].text == "S" and self.grid[row-1][col+1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 7 and col == 1:
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col+1].text == "S":
                points += 1
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col+2].text == "S" and self.grid[row-1][col+1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col+1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col-1].text == "S":
                points += 1
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 7 and 1 < col < 7:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col-2].text == "S" and self.grid[row-1][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col+1].text == "S":
                points += 1
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col+2].text == "S" and self.grid[row-1][col+1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col+1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col-1].text == "S":
                points += 1
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 7 and col == 7:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col-2].text == "S" and self.grid[row-1][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col+1].text == "S":
                points += 1
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row+1][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row-1][col+1].text == "S":
                points += 1
                self.grid[row + 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 7 and col == 8:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-1][col].text == "S" and self.grid[row][col].text == "O" and self.grid[row+1][col].text == "S":
                points += 1
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row + 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col-2].text == "S" and self.grid[row-1][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 8 and col == 0:
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col+2].text == "S" and self.grid[row-1][col+1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 8 and col == 1:
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col+2].text == "S" and self.grid[row-1][col+1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 8 and 1 < col < 7:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col].text == "S" and self.grid[row][col+1].text == "O" and self.grid[row][col+2].text == "S":
                points += 1
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col-2].text == "S" and self.grid[row-1][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col+2].text == "S" and self.grid[row-1][col+1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col + 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 8 and col == 7:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row][col-1].text == "S" and self.grid[row][col].text == "O" and self.grid[row][col+1].text == "S":
                points += 1
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col + 1].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col-2].text == "S" and self.grid[row-1][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
        elif row == 8 and col == 8:
            if self.grid[row][col-2].text == "S" and self.grid[row][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col].text == "S" and self.grid[row-1][col].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
            if self.grid[row-2][col-2].text == "S" and self.grid[row-1][col-1].text == "O" and self.grid[row][col].text == "S":
                points += 1
                self.grid[row - 2][col - 2].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row - 1][col - 1].background_color = (0.207, 0.635, 0.423, 0.9)
                self.grid[row][col].background_color = (0.207, 0.635, 0.423, 0.9)
        return points


class Game(GridLayout):
    def __init__(self, root, player1, player2='CPU'):
        super(Game, self).__init__()
        self.rows = 9
        self.cols = 9
        self.board = SOSBoard(player1, player2)
        self.add_widget(self.board)
        self.flay = FloatLayout()
        self.compatition = Label(text='SOS!', font_size=100, size_hint=(.15, .1), pos_hint={'center_x': .5, 'center_y': .7}, color=(0,0,0,1))
        self.s_btn = Button(text='S', font_size=50, size_hint=(.15, .1), pos_hint={'center_x': .3, 'center_y': .5})
        self.o_btn = Button(text='O', font_size=50, size_hint=(.15, .1), pos_hint={'center_x': .7, 'center_y': .5})
        self.player1name = Label(text=self.board.player1.name, font_size=60, pos_hint={'center_x': .3, 'center_y': .3}, color=(0,0,1,1))
        self.player2name = Label(text=self.board.player2.name, font_size=60, pos_hint={'center_x': .7, 'center_y': .3}, color=(1,0,0,1))
        self.player1points = Label(text=str(self.board.scoreboard.player1points), font_size=45, pos_hint={'center_x': .3, 'center_y': .2}, color=(0,0,0,1))
        self.player2points = Label(text=str(self.board.scoreboard.player2points), font_size=45, pos_hint={'center_x': .7, 'center_y': .2}, color=(0,0,0,1))
        self.whoplay = Label(text=str('{self.player1name.text}`s turn'.format(**locals())), font_size=45, pos_hint={'center_x': .5, 'center_y': .1}, color=(0,0,1,1))
        if self.player2name.text != 'CPU':
            self.flay.add_widget(self.whoplay)
        self.flay.add_widget(self.s_btn)
        self.flay.add_widget(self.o_btn)
        self.flay.add_widget(self.player1name)
        self.flay.add_widget(self.player2name)
        self.flay.add_widget(self.player1points)
        self.flay.add_widget(self.player2points)
        self.flay.add_widget(self.compatition)
        self.add_widget(self.flay)
        self.s_btn.bind(on_release=lambda x:self.on_s_pressed())
        self.o_btn.bind(on_release=lambda x:self.on_o_pressed())

    def on_s_pressed(self):
        self.board.currentturn.s()
        self.s_btn.background_color = (0, 0, 1, 1)
        self.o_btn.background_color = (1, 1, 1, 1)

    def on_o_pressed(self):
        self.board.currentturn.o()
        self.s_btn.background_color = (1, 1, 1, 1)
        self.o_btn.background_color = (0, 0, 1, 1)

    def add_display_points(self):
        if self.board.currentturn.num%2 == 1:
            self.player1points = Label(text=str(self.board.scoreboard.player1points), font_size=45,
                                       pos_hint={'center_x': .3, 'center_y': .2}, color=(0, 0, 0, 1))
        else:
            self.player2points = Label(text=str(self.board.scoreboard.player2points), font_size=45,
                                       pos_hint={'center_x': .7, 'center_y': .2}, color=(0, 0, 0, 1))


class SOSApp(App):
    def __init__(self, root, player1, player2='CPU'):
        super(SOSApp, self).__init__()
        self.player1name = player1
        self.player2name = player2
        if player2 == 'CPU':
            self.game = Game(root, self.player1name)
        else:
            self.game = Game(root, self.player1name, self.player2name)

    def build(self):
        return self.game


class AITurn(Turn):
    def __init__(self, num):
        Turn.__init__(self,num)
        self.defends = dict()
        self.defendo = dict()
        self.attacks = dict()
        self.attacko = dict()

    def doPriorityMove(self):
        grid = App.get_running_app().game.board.grid
        for row in range(9):
            for col in range(9):
                if row == 0:
                    if col == 0:
                        if grid[row][col].text == '':
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                self.attacks[(row, col)] = 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row][col + 1].text == 'S':
                                self.defends[(row, col)] = 1
                            if grid[row + 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row + 1][col + 1] == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                        else: pass
                    elif col == 1:
                        if grid[row][col].text == '':
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] = 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                self.attacks[(row, col)] = 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row][col - 1].text == 'S':
                                self.defends[(row, col)] = 1
                            if grid[row + 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row + 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row + 1][col].text == 'O':
                                self.defendo[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row + 1][col + 1].text == 'S':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                        else: pass
                    elif 1 < col < 7:
                        if grid[row][col].text == '':
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] = 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                self.attacks[(row, col)] = 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col] == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'O' and grid[row + 2][col - 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row][col - 1].text == 'S':
                                self.defends[(row, col)] = 1
                            elif grid[row][col - 1].text == 'O':
                                self.defendo[(row, col)] = 1
                            if grid[row][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row + 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row + 1][col].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row + 1][col - 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row + 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row + 1][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                        else: pass
                    elif col == 7:
                        if grid[row][col].text == '':
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] = 1
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] = 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'O' and grid[row + 2][col - 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row][col - 1].text == 'S':
                                self.defends[(row, col)] = 1
                            elif grid[row][col - 1].text == 'O':
                                self.defendo[(row, col)] = 1
                            if grid[row][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row + 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row + 1][col].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row + 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row + 1][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                        else: pass
                    elif col == 8:
                        if grid[row][col].text == '':
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] = 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'O' and grid[row + 2][col - 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                        else: pass
                elif row == 1:
                    if col == 0:
                        if grid[row][col].text == '':
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                self.attacko[(row, col)] = 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                self.attacks[(row, col)] = 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row][col + 1].text == 'S':
                                self.defends[(row, col)] = 1
                            elif grid[row][col + 1].text == 'O':
                                self.defendo[(row, col)] = 1
                            if grid[row - 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row + 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row + 1][col + 1].text == 'O':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                        else: pass
                    if col == 1:
                        if grid[row][col].text == '':
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] = 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                self.attacks[(row, col)] = 1
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'S' and grid[row - 1][col + 1].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row - 1][col - 1].text == 'S' and grid[row + 1][col + 1].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] = 1
                            if grid[row - 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row][col + 1].text == 'O':
                                self.defendo[(row, col)] = 1
                            if grid[row + 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row + 1][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row + 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row + 1][col].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                        else: pass
                    elif 1 < col < 7:
                        if grid[row][col].text == '':
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] = 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] = 1
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col - 1].text == 'S' and grid[row + 1][col + 1].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'S' and grid[row - 1][col + 1].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'O' and grid[row + 2][col - 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] = 1
                            if grid[row - 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row][col + 1].text == 'O':
                                self.defendo[(row, col)] = 1
                            if grid[row + 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row + 1][col].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row + 1][col - 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row][col - 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                        else: pass
                    elif col == 7:
                        if grid[row][col].text == '':
                            if grid[row - 1][col - 1].text == 'S' and grid[row + 1][col + 1].text == 'S':
                                self.attacko[(row, col)] = 1
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'S':
                                self.attacks[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'S' and grid[row + 1][col - 1].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'O' and grid[row + 2][col - 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row][col - 2].text == 'S' and grid[row][col - 2].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] = 1
                            if grid[row - 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row + 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row + 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row + 1][col].text == 'O':
                                self.defendo[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row + 1][col - 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row][col - 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                        else: pass
                    elif col == 8:
                        if grid[row][col].text == '':
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                self.attacko[(row, col)] = 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'S':
                                self.attacks[(row, col)] = 1
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'O' and grid[row + 2][col - 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] = 1
                            if grid[row][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row][col - 1].text == 'O':
                                self.defendo[row, col] = 1
                            if grid[row + 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row + 1][col].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'O':
                                if self.defends.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                        else: pass
                elif 1 < row < 7:
                    if col == 0:
                        if grid[row][col].text == '':
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                self.attacks[(row, col)] = 1
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                self.attacko[(row, col)] = 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'O' and grid[row - 2][col + 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] = 1
                            elif grid[row - 1][col].text == 'O':
                                self.defendo[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row + 1][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row + 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row + 1][col].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                        else: pass
                    elif col == 1:
                        if grid[row][col].text == '':
                            if grid[row - 1][col - 1].text == 'S' and grid[row + 1][col + 1].text == 'S':
                                self.attacko[(row, col)] = 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == 'S':
                                self.attacks[(row, col)] = 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'S' and grid[row + 1][col - 1].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'O' and grid[row - 2][col + 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] = 1
                            if grid[row - 1][col].text == 'O':
                                self.defendo[(row, col)] = 1
                            elif grid[row - 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            elif grid[row - 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            elif grid[row][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row + 1][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            elif grid[row + 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row + 1][col].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            elif grid[row + 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                        else: pass
                    elif 1 < col < 7:
                        if grid[row][col].text == '':
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] = 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] = 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col - 1].text == 'S' and grid[row + 1][col + 1].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 2][col + 2].text == 'S' and grid[row - 1][col + 1].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'S' and grid[row + 1][col - 1].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'O' and grid[row + 2][col - 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] = 1
                            elif grid[row - 1][col - 1].text == 'O':
                                self.defendo[(row, col)] = 1
                            if grid[row - 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row - 1][col].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row - 1][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row + 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row + 1][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row + 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row + 1][col].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row + 1][col - 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row][col - 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                        else: pass
                    elif col == 7:
                        if grid[row][col].text == '':
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] = 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] = 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col - 1].text == 'S' and grid[row + 1][col + 1].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row + 2][col - 2].text == 'S' and grid[row + 1][col - 1].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'S' and grid[row - 1][col + 1].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] = 1
                            elif grid[row - 1][col - 1].text == 'O':
                                self.defendo[(row, col)] = 1
                            if grid[row - 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row - 1][col].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row - 1][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row + 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row + 1][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row + 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row + 1][col].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row + 1][col - 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row][col - 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                        else: pass
                    elif col == 8:  # TODO fix
                        if grid[row][col] == '':
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] = 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            elif grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                self.attacko[(row, col)] = 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row + 2][col - 2].text == 'S' and grid[row + 1][col - 1].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] = 1
                            elif grid[row - 1][col - 1].text == 'O':
                                self.defendo[(row, col)] = 1
                            if grid[row - 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row - 1][col].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row + 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row + 1][col].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row + 1][col - 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row][col - 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                        else: pass
                elif row == 7:
                    if col == 0:
                        if grid[row][col].text == '':
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                self.attacks[(row, col)] = 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'O' and grid[row - 2][col + 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] = 1
                            elif grid[row - 1][col].text == 'O':
                                self.defendo[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row - 1][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row][col + 1].text == 'O':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                        else: pass
                    elif col == 1:
                        if grid[row][col].text == '':
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] = 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                self.attacks[(row, col)] = 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row - 1][col - 1].text == 'S' and grid[row + 1][col + 1].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'S' and grid[row - 1][col + 1].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'O' and grid[row - 2][col + 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] = 1
                            if grid[row - 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row - 1][col].text == 'O':
                                self.defendo[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row - 1][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row + 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row + 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                        else: pass
                    elif 1 < col < 7:
                        if grid[row][col].text == '':
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] = 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] = 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col - 1].text == 'S' and grid[row + 1][col + 1].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'O' and grid[row - 2][col + 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'S' and grid[row - 1][col + 1].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] = 1
                            elif grid[row - 1][col - 1].text == 'O':
                                self.defendo[(row, col)] = 1
                            if grid[row - 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row - 1][col].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row - 1][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row + 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row + 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row][col - 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                        else: pass
                    elif col == 7:
                        if grid[row][col].text == '':
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] = 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] = 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col - 1].text == 'S' and grid[row + 1][col + 1].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'S' and grid[row - 1][col + 1].text == 'S':
                                if self.attacko.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] = 1
                            elif grid[row - 1][col - 1].text == 'O':
                                self.defendo[(row, col)] = 1
                            if grid[row - 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row - 1][col].text == 'O':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row + 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row + 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row][col - 1].text == 'O':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                        else: pass
                    elif col == 8:
                        if grid[row][col].text == '':
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] = 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                self.attacko[(row, col)] = 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] = 1
                            elif grid[row - 1][col - 1].text == 'O':
                                self.defendo[(row, col)] = 1
                            if grid[row - 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row - 1][col].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row + 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row + 1][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row][col - 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                        else: pass
                elif row == 8:
                    if col == 0:
                        if grid[row][col].text == '':
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                self.attacks[(row, col)] = 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'O' and grid[row - 2][col + 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                        else: pass
                    elif col == 1:
                        if grid[row][col].text == '':
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] = 1
                            elif grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                self.attacks[(row, col)] = 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'O' and grid[row - 2][col + 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row - 1][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                        else: pass
                    elif 1 < col < 7:
                        if grid[row][col].text == '':
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] = 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] = 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 2][col + 2].text == 'S' and grid[row - 1][col + 1].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] = 1
                            elif grid[row - 1][col - 1].text == 'O':
                                self.defendo[(row, col)] = 1
                            if grid[row - 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row - 1][col].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row - 1][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row][col - 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                        else: pass
                    elif col == 7:
                        if grid[row][col].text == '':
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] = 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] = 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacko[(row, col)] += 1
                                else:
                                    self.attacko[(row, col)] = 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] = 1
                            elif grid[row - 1][col - 1].text == 'O':
                                self.defendo[(row, col)] = 1
                            if grid[row - 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row - 1][col].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row - 1][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row][col + 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            if grid[row][col - 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row][col - 1].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                        else: pass
                    elif col == 8:
                        if grid[row][col].text == '':
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                self.attacks[(row, col)] = 1
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == 'O':
                                if self.attacks.has_key((row, col)):
                                    self.attacks[(row, col)] += 1
                                else:
                                    self.attacks[(row, col)] = 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] = 1
                            elif grid[row - 1][col - 1].text == 'O':
                                self.defendo[(row, col)] = 1
                            if grid[row - 1][col].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row - 1][col].text == 'O':
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                        else: pass
        maxatt = 0
        maxattlist = list()
        maxdef = 0
        maxdeflist = list()
        for current in self.attacks:
            if self.attacks[current] > maxatt:
                maxatt = self.attacks[current]
        for current in self.attacko:
            if self.attacko[current] > maxatt:
                maxatt = self.attacko[current]
        if maxatt != 0:
            for i in self.attacks:
                if self.attacks[i] == maxatt:
                    maxattlist.append(Action(S, i, App.get_running_app().game.board.grid[i[0]][i[1]]))
            for i in self.attacko:
                if self.attacko[i] == maxatt:
                    maxattlist.append(Action(O, i, App.get_running_app().game.board.grid[i[0]][i[1]]))
            chosen1 = random.choice(maxattlist)
            chosen1.take()
        else:
            for current in self.defends:
                if self.defends[current] > maxdef:
                    maxdef = self.defends[current]
            for current in self.defendo:
                if self.defendo[current] > maxdef:
                    maxdef = self.defendo[current]
            for i in self.defends:
                if self.defends[i] == maxdef:
                    maxdeflist.append(Action(S, i, App.get_running_app().game.board.grid[i[0]][i[1]]))
            for i in self.defendo:
                if self.defendo[i] == maxdef:
                    maxdeflist.append(Action(O, i, App.get_running_app().game.board.grid[i[0]][i[1]]))
            chosen1 = random.choice(maxdeflist)
            chosen1.take()


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