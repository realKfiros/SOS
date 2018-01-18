from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from player import Player
from scoreboard import Scoreboard
from turn import Turn
from turn import AITurn
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label

NONE = 0
S = 1
O = 2


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
        if self.currentturn.num == 82:
            if self.scoreboard.player1points > self.scoreboard.player2points:
                winnerstr = App.get_running_app().game.player1name.text + ' is the winner!!!'
                popup = Popup(title='Game over',content=Label(text=winnerstr),size_hint=(None, None), size=(400, 400))
                popup.open()
            elif self.scoreboard.player1points < self.scoreboard.player2points:
                winnerstr = App.get_running_app().game.player2name.text + ' is the winner!!!'
                popup = Popup(title='Game over', content=Label(text=winnerstr), size_hint=(None, None), size=(400, 400))
                popup.open()
            else:
                popup = Popup(title='Game over', content=Label(text='Draw'), size_hint=(None, None), size=(400, 400))
                popup.open()
            return
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


class SOSPoint(Button):
    def __init__(self, x, y):
        super(SOSPoint, self).__init__()
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