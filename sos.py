from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from game.board import SOSBoard
from main import SOS


NONE = 0
S = 1
O = 2


class Game(GridLayout):
    """
    The class for the SOS game and for the graphics of the game.
    """
    def __init__(self, root, player1='CPU', player2='CPU', darkmode=False, rows=9, cols=9):
        """
        The constructor
        :param root:
        :param player1: the name of the first player
        :param player2: the name of the second player, default value to 'CPU' which means game against the computer
        :param darkmode: True if the darkmode is enabled, default value to False.
        :param rows: The number of the rows on the game board, default value to 9
        :param cols: The number of the cols on the game board, default value to 9
        """
        super(Game, self).__init__()
        self.textcolor = (1, 1, 1, 1)
        if darkmode:
            self.textcolor = (0, 0, 0, 1)
        self.rows = rows
        self.cols = cols
        self.board = SOSBoard(player1, player2, self.rows, self.cols)
        self.add_widget(self.board)
        self.flay = FloatLayout()
        self.compatition = Label(text='SOS!',
                                 font_size=100,
                                 size_hint=(.15, .1),
                                 pos_hint={'center_x': .5, 'center_y': .7},
                                 color=self.textcolor)
        if player1 != 'CPU':
            self.s_btn = Button(text='S',
                                font_size=50,
                                size_hint=(.15, .1),
                                pos_hint={'center_x': .3, 'center_y': .5})
            self.o_btn = Button(text='O',
                                font_size=50,
                                size_hint=(.15, .1),
                                pos_hint={'center_x': .7, 'center_y': .5})
        self.player1name = Label(text=self.board.player1.name,
                                 font_size=60,
                                 pos_hint={'center_x': .3, 'center_y': .3},
                                 color=(0, 0, 1, 1))
        self.player2name = Label(text=self.board.player2.name,
                                 font_size=60,
                                 pos_hint={'center_x': .7, 'center_y': .3},
                                 color=(1, 0, 0, 1))
        self.player1points = Label(text=str(self.board.scoreboard.player1points),
                                   font_size=45,
                                   pos_hint={'center_x': .3, 'center_y': .2},
                                   color=self.textcolor)
        self.player2points = Label(text=str(self.board.scoreboard.player2points),
                                   font_size=45,
                                   pos_hint={'center_x': .7, 'center_y': .2},
                                   color=self.textcolor)
        self.whoplay = Label(text=str('{self.player1name.text}`s turn'.format(**locals())),
                             font_size=45,
                             pos_hint={'center_x': .5, 'center_y': .1},
                             color=(0, 0, 1, 1))
        if self.player2name.text != 'CPU':
            self.flay.add_widget(self.whoplay)
        self.backbtn = Button(text='Back',
                              font_size=50,
                              size_hint=(.15, .1),
                              pos_hint={'center_x': .9, 'center_y': .9},
                              on_release=self.on_popup_dismiss)
        self.flay.add_widget(self.s_btn)
        self.flay.add_widget(self.o_btn)
        self.flay.add_widget(self.player1name)
        self.flay.add_widget(self.player2name)
        self.flay.add_widget(self.player1points)
        self.flay.add_widget(self.player2points)
        self.flay.add_widget(self.compatition)
        self.flay.add_widget(self.backbtn)
        self.add_widget(self.flay)
        self.s_btn.bind(on_release=lambda x:self.on_s_pressed())
        self.o_btn.bind(on_release=lambda x:self.on_o_pressed())

    def on_s_pressed(self):
        """
        :return: Changes the selection for the current turn to S, when the 's_btn' is pressed
        """
        self.board.currentturn.s()
        self.s_btn.background_color = (0, 0, 1, 1)
        self.o_btn.background_color = (1, 1, 1, 1)

    def on_o_pressed(self):
        """
        :return: Changes the selection for the current turn to O, when the 'o_btn' is pressed
        """
        self.board.currentturn.o()
        self.s_btn.background_color = (1, 1, 1, 1)
        self.o_btn.background_color = (0, 0, 1, 1)

    def add_display_points(self):
        """
        :return: Adds points if needed. Called after every turn...
        """
        if self.board.currentturn.num%2 == 1:
            self.player1points = Label(text=str(self.board.scoreboard.player1points), font_size=45,
                                       pos_hint={'center_x': .3, 'center_y': .2},
                                       color=(0, 0, 0, 1))
        else:
            self.player2points = Label(text=str(self.board.scoreboard.player2points), font_size=45,
                                       pos_hint={'center_x': .7, 'center_y': .2},
                                       color=(0, 0, 0, 1))

    def on_popup_dismiss(self, instance):
        self.remove_widget(self.board)
        self.remove_widget(self.flay)
        self.add_widget(SOS())