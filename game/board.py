import os
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from player import Player
from scoreboard import Scoreboard
from turn import Turn
from turn import AITurn
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.lang.builder import Builder

NONE = 0
S = 1
O = 2


class SOSBoard(GridLayout):
    """
    The class for the board of the game with the graphics.
    """
    def __init__(self, player1, player2='CPU', cols=9, rows=9):
        """
        The constructor
        :param player1: the name of the first player
        :param player2: the name of the second player, default value to 'CPU', which means game against the computer
        :param cols: the number of the cols on the board, default value to 9
        :param rows: the number of the rows on the board, default value to 9
        """
        super(SOSBoard, self).__init__()
        self.ai = True if player2 == 'CPU' else False
        self.cols = cols
        self.rows = rows
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
        """
        :return: changes the selection of the current turn to S, or initializes it to S
        """
        self.currentturn.s()

    def o(self):
        """
        :return: changes the selection of the current turn to O, or initializes it to O
        """
        self.currentturn.o()

    def done(self, tile):
        """
        :param tile: needed for the on_release/on_press function
        :return: finishes the turn and resets the current selection
        """
        if self.currentturn.choice == NONE:
            return False
        elif tile.occupied:
            return False
        else:
            tile.text = self.on_done()
            return True

    def on_release(self, instance):
        '''
        does the turn when needed
        :param instance: needed for the kivy button
        :return: when the turn is over
        '''
        if App.get_running_app().game.board.currentturn.choice == NONE:
            return
        if instance.text:
            return None
        self.done(instance)
        instance.disabled = True
        instance.disabled_color = (1,1,1,1)
        instance.background_disabled_normal = ''
        # instace.background_color = (0.207, 0.635, 0.423, 0.9)
        instance.background_color = (0.1, 0.2, 0.3, 0.6)
        currentnum = self.currentturn.num
        if currentnum%2 == 1:
            toadd = self.scoreboard.player1points + self.addpoints(instance)
            self.scoreboard.player1points = toadd
        else:
            toadd = self.scoreboard.player2points + self.addpoints(instance)
            self.scoreboard.player2points = toadd
        self.currentturn = Turn(currentnum+1)
        App.get_running_app().game.s_btn.background_color = (1, 1, 1, 1)
        App.get_running_app().game.o_btn.background_color = (1, 1, 1, 1)
        if self.currentturn.num == (self.rows * self.cols) + 1:
            if self.scoreboard.player1points > self.scoreboard.player2points:
                winnerstr = App.get_running_app().game.player1name.text + ' is the winner!!!'
                gif = Image(source='assets/memes/playerwon.zip',
                            anim_delay=.1)
                gif.allow_stretch = True
                gif.keep_ratio = False
                popup = Popup(title=winnerstr, content=gif, size_hint=(None, None), size=(600, 600))
                popup.open()
            elif self.scoreboard.player1points < self.scoreboard.player2points:
                winnerstr = App.get_running_app().game.player2name.text + ' is the winner!!!'
                gif = Image(source='assets/memes/cpuwon.zip',
                            anim_delay=.1)
                gif.allow_stretch = True
                gif.keep_ratio = False
                popup = Popup(title=winnerstr, content=gif, size_hint=(None, None), size=(600, 600))
                popup.open()
            else:
                popup = Popup(title='Draw!!!', content=Label(text='[b]Gif? It\'s for losers! There\'s no loser!!![/b]', markup=True), size_hint=(None, None), size=(600, 600))
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
        """
        :return: finishes the turn and writes the selection on the player on the selected square.
        """
        if self.currentturn.choice == S:
            return "S"
        elif self.currentturn.choice == O:
            return "O"


    def addpoints(self, instance):
        """
        :param instace: for the on_release/on_press function
        :return: the number of the points to be added after the last turn (after checking all directions and painting the squares if they're part of an SOS pattern)
        """
        row, col = instance.r, instance.c
        points = 0
        GREEN = (0.207, 0.635, 0.423, 0.9)
        char = self.grid[row][col].text

        # all 8 directions
        directions_all = [
            (0, 1), (0, -1),
            (1, 0), (-1, 0),
            (1, 1), (-1, -1),
            (1, -1), (-1, 1),
        ]

        # half of the directions (right/down only) to prevent double counting when O is in the middle
        directions_half = [
            (0, 1),      # horizontal
            (1, 0),      # vertical
            (1, 1),     # main diagonal
            (1, -1),     # anti diagonal
        ]

        def in_bounds(r, c):
            return 0 <= r < len(self.grid) and 0 <= c < len(self.grid[0])

        def text(r, c):
            return self.grid[r][c].text if in_bounds(r, c) else None

        def highlight(cells):
            for r, c in cells:
                self.grid[r][c].background_color = GREEN

        # If the move was an S - check all directions for SOS starting from this S
        if char == "S":
            for dr, dc in directions_all:
                r1, c1 = row, col
                r2, c2 = row + dr, col + dc
                r3, c3 = row + 2*dr, col + 2*dc

                if in_bounds(r3, c3):
                    if text(r1, c1) == "S" and text(r2, c2) == "O" and text(r3, c3) == "S":
                        points += 1
                        highlight([(r1, c1), (r2, c2), (r3, c3)])

        # If the move was an O - check all directions for SOS centered at this O
        elif char == "O":
            for dr, dc in directions_half:
                r0, c0 = row - dr, col - dc
                r2, c2 = row + dr, col + dc

                if in_bounds(r0, c0) and in_bounds(r2, c2):
                    if text(r0, c0) == "S" and text(row, col) == "O" and text(r2, c2) == "S":
                        points += 1
                        highlight([(r0, c0), (row, col), (r2, c2)])
        
        return points


class SOSPoint(Button):
    """
    The class for squares on the board
    """
    def __init__(self, x, y):
        """
        The constructor
        :param x: the row number
        :param y: the col number
        """
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
        """
        :return: checks if the chosen square is occupied. returns True if occupied
        """
        if not self.occupied:
            self.text = "S"
            self.occupied = True
            return True
        return False

    def put_o(self):
        """
        :return: checks if the chosen square is occupied. returns True if occupied
        """
        if not self.occupied:
            self.text = "O"
            self.occupied = True
            return True
        return False