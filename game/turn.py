import random
from kivy.app import App
from action import Action

NONE = 0
S = 1
O = 2


class Turn:
    """
    The class for turns
    """
    def __init__(self, num):
        """
        The constructor
        :param num: Turn number in the game
        """
        self.choice = NONE
        self.done = False
        self.num = num

    def s(self):
        """
        :return: Changes the choice to S
        """
        self.choice = S

    def o(self):
        """
        :return: Changes the choice to O
        """
        self.choice = O

    def put(self):
        """
        :return: Used to mark that the player has finished his turn
        """
        self.done = True


class AITurn(Turn):
    """
    The class for the turns that are fons by the computer
    """
    def __init__(self, num):
        """
        The constructor
        :param num: the number of the turn in the game
        """
        Turn.__init__(self,num)
        self.defends = dict()
        self.defendo = dict()
        self.attacks = dict()
        self.attacko = dict()

    def doPriorityMove(self):
        grid = App.get_running_app().game.board.grid
        for r in range(9):
            for c in range(9):
                if grid[r][c].text == '':
                    self.attacks[(r, c)] = 0
                    self.attacko[(r, c)] = 0
                    self.defends[(r, c)] = 0
                    self.defendo[(r, c)] = 0
        for row in range(9):
            for col in range(9):
                if row == 0:
                    if col == 0:
                        if grid[row][col].text == '':
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row + 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row + 1][col + 1] == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                            if grid[row][col + 1].text == '':
                               if grid[row][col + 2].text == 'S':
                                   self.defendo[(row, col)] += 1
                            if grid[row + 1][col + 1].text == '':
                               if grid[row + 2][col + 2].text == 'S':
                                   self.defendo[(row, col)] += 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == '':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == '':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == '':
                                self.defends[(row, col)] -= 1
                            if grid[row][col + 1].text == '' and grid[row][col + 2].text == 'S':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col].text == '' and grid[row + 2][col].text == 'S':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col + 1].text == '' and grid[row + 2][col + 2].text == 'S':
                                self.defends[(row, col)] -= 1
                        else: pass
                    elif col == 1:
                        if grid[row][col].text == '':
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row + 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row + 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row + 1][col].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row + 1][col + 1].text == 'S':
                                self.defendo[(row, col)] += 1
                            if grid[row][col + 1].text == '':
                                if grid[row][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row + 2][col].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row + 1][col + 1].text == '':
                                if grid[row + 2][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row + 2][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row][col - 1].text == '' and grid[row][col + 1].text == 'S':
                                self.defendo[(row, col)] -= 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col].text == '' and grid[row + 2][col].text == 'S':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col + 1].text == '' and grid[row + 2][col + 2].text == 'S':
                                self.defends[(row, col)] -= 1
                        else: pass
                    elif 1 < col < 7:
                        if grid[row][col].text == '':
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col] == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'O' and grid[row + 2][col - 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row + 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row + 1][col].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row + 1][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row + 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row + 1][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row][col - 1].text == '':
                                if grid[row][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row + 1][col - 1].text == '':
                                if grid[row + 2][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row + 2][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row][col + 1].text == '':
                                if grid[row][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row + 2][col].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row + 1][col + 1].text == '':
                                if grid[row + 2][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row + 2][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row][col - 2].text == '' and grid[row][col - 1].text == 'O':
                                self.defends[(row, col)] -= 1
                            elif grid[row][col - 2].text == 'S' and grid[row][col - 1].text == '':
                                self.defends[(row, col)] -= 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row][col - 1].text == '' and grid[row][col + 1].text == 'S':
                                self.defendo[(row, col)] -= 1
                            if grid[row][col + 1].text == '' and grid[row][col + 2].text == 'S':
                                self.defends[(row, col)] -= 1
                            elif grid[row][col + 1].text == 'O' and grid[row][col + 2].text == '':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col - 1].text == 'O' and grid[row + 2][col - 2].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col - 1].text == '' and grid[row + 2][col - 2].text == 'S':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col].text == '' and grid[row + 2][col].text == 'S':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col + 1].text == '' and grid[row + 2][col + 2].text == 'S':
                                self.defends[(row, col)] -= 1
                        else: pass
                    elif col == 7:
                        if grid[row][col].text == '':
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'O' and grid[row + 2][col - 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row + 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row + 1][col].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row + 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row + 1][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row][col - 1].text == '':
                                if grid[row][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row + 2][col].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row + 1][col - 1].text == '':
                                if grid[row + 2][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row + 2][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row][col - 2].text == '' and grid[row][col - 1].text == 'O':
                                self.defends[(row, col)] -= 1
                            elif grid[row][col - 2].text == 'S' and grid[row][col - 1].text == '':
                                self.defends[(row, col)] -= 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row][col - 1].text == '' and grid[row][col + 1].text == 'S':
                                self.defendo[(row, col)] -= 1
                            if grid[row + 1][col - 1].text == 'O' and grid[row + 2][col - 2].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col - 1].text == '' and grid[row + 2][col - 2].text == 'S':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col].text == '' and grid[row + 2][col].text == 'S':
                                self.defends[(row, col)] -= 1
                        else: pass
                    elif col == 8:
                        if grid[row][col].text == '':
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'O' and grid[row + 2][col - 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                            if grid[row][col - 1].text == '':
                               if grid[row][col - 2].text == 'S':
                                   self.defendo[(row, col)] += 1
                            if grid[row + 1][col - 1].text == '':
                               if grid[row + 2][col - 2].text == 'S':
                                   self.defendo[(row, col)] += 1
                            if grid[row][col - 2].text == '' and grid[row][col - 1].text == 'O':
                                self.defends[(row, col)] -= 1
                            elif grid[row][col - 2].text == 'S' and grid[row][col - 1].text == '':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col - 1].text == 'O' and grid[row + 2][col - 2].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col - 1].text == '' and grid[row + 2][col - 2].text == 'S':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col].text == '' and grid[row + 2][col].text == 'S':
                                self.defends[(row, col)] -= 1
                        else: pass
                elif row == 1:
                    if col == 0:
                        if grid[row][col].text == '':
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row + 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row + 1][col + 1].text == 'O':
                                self.defends[(row, col)] += 1
                            if grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                            if grid[row][col + 1].text == '':
                               if grid[row][col + 2].text == 'S':
                                   self.defendo[(row, col)] += 1
                            if grid[row + 1][col + 1].text == '':
                               if grid[row + 2][col + 2].text == 'S':
                                   self.defendo[(row, col)] += 1
                            if grid[row - 1][col].text == '' and grid[row + 1][col].text == 'S':
                                self.defendo[(row, col)] -= 1
                            elif grid[row - 1][col].text == 'S' and grid[row + 1][col].text == '':
                                self.defendo[(row, col)] -= 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == '':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == '':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == '':
                                self.defends[(row, col)] -= 1
                            if grid[row][col + 1].text == '' and grid[row][col + 2].text == 'S':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col].text == '' and grid[row + 2][col].text == 'S':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col + 1].text == '' and grid[row + 2][col + 2].text == 'S':
                                self.defends[(row, col)] -= 1
                        else: pass
                    if col == 1:
                        if grid[row][col].text == '':
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'S' and grid[row - 1][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row - 1][col - 1].text == 'S' and grid[row + 1][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row - 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row + 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row + 1][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row + 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row + 1][col].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row][col + 1].text == '':
                                if grid[row][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row + 2][col].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row + 1][col + 1].text == '':
                                if grid[row + 2][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row + 2][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row - 1][col].text == '' and grid[row + 1][col].text == 'S':
                                self.defendo[(row, col)] -= 1
                            elif grid[row - 1][col].text == 'S' and grid[row + 1][col].text == '':
                                self.defendo[(row, col)] -= 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row][col - 1].text == '' and grid[row][col + 1].text == 'S':
                                self.defendo[(row, col)] -= 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col].text == '' and grid[row + 2][col].text == 'S':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col + 1].text == '' and grid[row + 2][col + 2].text == 'S':
                                self.defends[(row, col)] -= 1
                        else: pass
                    elif 1 < col < 7:
                        if grid[row][col].text == '':
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col - 1].text == 'S' and grid[row + 1][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'S' and grid[row - 1][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'O' and grid[row + 2][col - 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row - 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row + 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row + 1][col].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row + 1][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row][col - 1].text == '':
                                if grid[row][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row + 1][col - 1].text == '':
                                if grid[row + 2][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row + 2][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row][col + 1].text == '':
                                if grid[row][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row + 2][col].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row + 1][col + 1].text == '':
                                if grid[row + 2][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row + 2][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row - 1][col].text == '' and grid[row + 1][col].text == 'S':
                                self.defendo[(row, col)] -= 1
                            elif grid[row - 1][col].text == 'S' and grid[row + 1][col].text == '':
                                self.defendo[(row, col)] -= 1
                            if grid[row][col - 2].text == '' and grid[row][col - 1].text == 'O':
                                self.defends[(row, col)] -= 1
                            elif grid[row][col - 2].text == 'S' and grid[row][col - 1].text == '':
                                self.defends[(row, col)] -= 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row][col - 1].text == '' and grid[row][col + 1].text == 'S':
                                self.defendo[(row, col)] -= 1
                            if grid[row][col + 1].text == '' and grid[row][col + 2].text == 'S':
                                self.defends[(row, col)] -= 1
                            elif grid[row][col + 1].text == 'O' and grid[row][col + 2].text == '':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col - 1].text == 'O' and grid[row + 2][col - 2].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col - 1].text == '' and grid[row + 2][col - 2].text == 'S':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col].text == '' and grid[row + 2][col].text == 'S':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col + 1].text == '' and grid[row + 2][col + 2].text == 'S':
                                self.defends[(row, col)] -= 1
                        else: pass
                    elif col == 7:
                        if grid[row][col].text == '':
                            if grid[row - 1][col - 1].text == 'S' and grid[row + 1][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col + 1].text == 'S' and grid[row + 1][col - 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'O' and grid[row + 2][col - 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row][col - 2].text == 'S' and grid[row][col - 2].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row - 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row + 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row + 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row + 1][col].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row + 1][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row][col - 1].text == '':
                                if grid[row][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row + 2][col].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row + 1][col - 1].text == '':
                                if grid[row + 2][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row + 2][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row - 1][col].text == '' and grid[row + 1][col].text == 'S':
                                self.defendo[(row, col)] -= 1
                            elif grid[row - 1][col].text == 'S' and grid[row + 1][col].text == '':
                                self.defendo[(row, col)] -= 1
                            if grid[row][col - 2].text == '' and grid[row][col - 1].text == 'O':
                                self.defends[(row, col)] -= 1
                            elif grid[row][col - 2].text == 'S' and grid[row][col - 1].text == '':
                                self.defends[(row, col)] -= 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row][col - 1].text == '' and grid[row][col + 1].text == 'S':
                                self.defendo[(row, col)] -= 1
                            if grid[row + 1][col - 1].text == 'O' and grid[row + 2][col - 2].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col - 1].text == '' and grid[row + 2][col - 2].text == 'S':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col].text == '' and grid[row + 2][col].text == 'S':
                                self.defends[(row, col)] -= 1
                        else: pass
                    elif col == 8:
                        if grid[row][col].text == '':
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'O' and grid[row + 2][col - 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col - 1].text == 'O':
                                self.defendo[row, col] += 1
                            if grid[row + 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row + 1][col].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                            if grid[row][col - 1].text == '':
                               if grid[row][col - 2].text == 'S':
                                   self.defendo[(row, col)] += 1
                            if grid[row + 1][col - 1].text == '':
                               if grid[row + 2][col - 2].text == 'S':
                                   self.defendo[(row, col)] += 1
                            if grid[row - 1][col].text == '' and grid[row + 1][col].text == 'S':
                                self.defendo[(row, col)] -= 1
                            elif grid[row - 1][col].text == 'S' and grid[row + 1][col].text == '':
                                self.defendo[(row, col)] -= 1
                            if grid[row][col - 2].text == '' and grid[row][col - 1].text == 'O':
                                self.defends[(row, col)] -= 1
                            elif grid[row][col - 2].text == 'S' and grid[row][col - 1].text == '':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col - 1].text == 'O' and grid[row + 2][col - 2].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col - 1].text == '' and grid[row + 2][col - 2].text == 'S':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col].text == '' and grid[row + 2][col].text == 'S':
                                self.defends[(row, col)] -= 1
                        else: pass
                elif 1 < row < 7:
                    if col == 0:
                        if grid[row][col].text == '':
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col + 1].text == 'O' and grid[row - 2][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row - 1][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row + 1][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row + 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row + 1][col].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                                if grid[row - 2][col].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                                if grid[row + 2][col].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row][col + 1].text == '':
                                if grid[row][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                if grid[row][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row - 1][col + 1].text == '':
                                if grid[row - 2][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                if grid[row - 2][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row + 1][col + 1].text == '':
                                if grid[row + 2][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                if grid[row + 2][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            # relevant for all
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col].text == '' and grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] -= 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col].text == '' and grid[row][col + 2].text == 'S':
                                self.defends[(row, col)] -= 1
                            # relevant also from 7
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row - 1][col].text == '' and grid[row + 1][col].text == 'S':
                                self.defendo[(row, col)] -= 1
                            # relevant only here
                            if grid[row - 2][col + 2].text == 'S' and grid[row - 1][col + 2].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col + 2].text == '' and grid[row - 1][col + 2].text == 'S':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col + 1].text == '' and grid[row + 2][col + 2].text == 'S':
                                self.defends[(row, col)] -= 1
                        else: pass
                    elif col == 1:
                        if grid[row][col].text == '':
                            if grid[row - 1][col - 1].text == 'S' and grid[row + 1][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col + 1].text == 'S' and grid[row + 1][col - 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row - 1][col + 1].text == 'O' and grid[row - 2][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row - 1][col].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row - 1][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row + 1][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row + 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row + 1][col].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row + 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                                if grid[row - 2][col].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                                if grid[row + 2][col].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row][col + 1].text == '':
                                if grid[row][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                if grid[row][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row - 1][col + 1].text == '':
                                if grid[row - 2][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                if grid[row - 2][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row + 1][col + 1].text == '':
                                if grid[row + 2][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                if grid[row + 2][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            # relevant for all
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col].text == '' and grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] -= 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row][col - 1].text == '' and grid[row][col + 1].text == 'S':
                                self.defendo[(row, col)] -= 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col].text == '' and grid[row][col + 2].text == 'S':
                                self.defends[(row, col)] -= 1
                            # relevant also from 7
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row - 1][col].text == '' and grid[row + 1][col].text == 'S':
                                self.defendo[(row, col)] -= 1
                            if grid[row - 1][col - 1].text == 'S' and grid[row + 1][col + 1].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row - 1][col - 1].text == '' and grid[row + 1][col + 1].text == 'S':
                                self.defendo[(row, col)] -= 1
                            if grid[row - 1][col + 1].text == 'S' and grid[row + 1][col - 1].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row - 1][col + 1].text == '' and grid[row + 1][col - 1].text == 'S':
                                self.defendo[(row, col)] -= 1
                            # relevant only here
                            if grid[row - 2][col + 2].text == 'S' and grid[row - 1][col + 2].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col + 2].text == '' and grid[row - 1][col + 2].text == 'S':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col + 1].text == '' and grid[row + 2][col + 2].text == 'S':
                                self.defends[(row, col)] -= 1
                        else: pass
                    elif 1 < col < 7:
                        if grid[row][col].text == '':
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col - 1].text == 'S' and grid[row + 1][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 2][col + 2].text == 'S' and grid[row - 1][col + 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col + 1].text == 'S' and grid[row + 1][col - 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'O' and grid[row + 2][col - 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col - 1].text == '':
                                if grid[row - 2][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                                elif grid[row - 2][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                            if grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'O':
                                    self.defends[(row, col)] += 1
                                elif grid[row - 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                            if grid[row - 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col + 1].text == '':
                                if grid[row - 2][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                                elif grid[row - 2][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                            if grid[row][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row][col + 1].text == '':
                                if grid[row][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                                elif grid[row][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                            if grid[row + 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row + 1][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row + 1][col + 1].text == '':
                                if grid[row + 2][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                                elif grid[row + 2][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                            if grid[row + 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row + 1][col].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'O':
                                    self.defends[(row, col)] += 1
                                elif grid[row + 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row + 1][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row + 1][col - 1].text == '':
                                if grid[row + 2][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                                elif grid[row + 2][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                            if grid[row][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row][col - 1].text == '':
                                if grid[row][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                                elif grid[row][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                            # relevant for all
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row][col - 2].text == '' and grid[row][col - 1].text == 'O':
                                self.defends[(row, col)] -= 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row][col - 1].text == '' and grid[row][col + 1].text == 'S':
                                self.defendo[(row, col)] -= 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row][col + 1].text == '' and grid[row][col  + 2].text == 'S':
                                self.defends[(row, col)] -= 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col - 2].text == '' and grid[row - 2][col - 1].text == 'O':
                                self.defends[(row, col)] -= 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col].text == '' and grid[row - 1][col].text == 'O':
                                self.defends[(row, col)] -= 1
                            if grid[row - 2][col + 2].text == 'S' and grid[row - 1][col + 1].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col + 2].text == '' and grid[row - 1][col + 1].text == 'O':
                                self.defends[(row, col)] -= 1
                            # relevant also for 7
                            if grid[row - 1][col - 1].text == 'S' and grid[row + 1][col + 1].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row - 1][col - 1].text == '' and grid[row + 1][col + 1].text == 'S':
                                self.defendo[(row, col)] -= 1
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row - 1][col].text == '' and grid[row + 1][col].text == 'S':
                                self.defendo[(row, col)] -= 1
                            if grid[row + 1][col - 1].text == 'S' and grid[row - 1][col + 1].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row + 1][col - 1].text == '' and grid[row - 1][col + 1].text == 'S':
                                self.defendo[(row, col)] -= 1
                            # relevant only here
                            if grid[row + 1][col - 1].text == '' and grid[row + 2][col - 2].text == 'S':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col - 1].text == 'O' and grid[row + 2][col - 2].text == '':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col].text == '' and grid[row + 2][col].text == 'S':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col].text == 'O' and grid[row + 2][col].text == '':
                                self.defends[(row, col)] -= 1
                            if grid[row + 1][col + 1].text == '' and grid[row + 2][col + 2].text == 'S':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col + 1].text == 'O' and grid[row + 2][col + 2].text == '':
                                self.defends[(row, col)] -= 1
                        else: pass
                    elif col == 7:
                        if grid[row][col].text == '':
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row + 1][col].text == 'O' and grid[row + 2][col].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col - 1].text == 'S' and grid[row + 1][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row + 2][col - 2].text == 'S' and grid[row + 1][col - 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'S' and grid[row - 1][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col - 1].text == '':
                                if grid[row - 2][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                                elif grid[row - 2][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                            if grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'O':
                                    self.defends[(row, col)] += 1
                                elif grid[row - 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                            if grid[row - 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row + 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row + 1][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row + 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row + 1][col].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'O':
                                    self.defends[(row, col)] += 1
                                elif grid[row + 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row + 1][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row + 1][col - 1].text == '':
                                if grid[row + 2][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                                elif grid[row + 2][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                            if grid[row][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col].text == '':
                                if grid[row][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                                elif grid[row][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                            # relevant for all
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row][col - 1].text == '' and grid[row][col + 1].text == 'S':
                                self.defendo[(row, col)] -= 1
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row][col - 2].text == '' and grid[row][col - 1].text == 'O':
                                self.defends[(row, col)] -= 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col - 2].text == '' and grid[row - 1][col - 1].text == 'O':
                                self.defends[(row, col)] -= 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col].text == '' and grid[row - 1][col].text == 'O':
                                self.defends[(row, col)] -= 1
                            # relevant also for 7
                            if grid[row - 1][col - 1].text == 'S' and grid[row + 1][col + 1].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row - 1][col - 1].text == '' and grid[row + 1][col + 1].text == 'S':
                                self.defendo[(row, col)] -= 1
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row - 1][col].text == '' and grid[row + 1][col].text == 'S':
                                self.defendo[(row, col)] -= 1
                            if grid[row + 1][col - 1].text == 'S' and grid[row - 1][col + 1].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row + 1][col - 1].text == '' and grid[row - 1][col + 1].text == 'S':
                                self.defendo[(row, col)] -= 1
                            # relevant only here
                            if grid[row + 2][col].text == 'S' and grid[row + 1][col].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 2][col].text == '' and grid[row + 1][col].text == 'O':
                                self.defends[(row, col)] -= 1
                            if grid[row + 2][col - 2].text == 'S' and grid[row + 1][col - 1].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 2][col - 2].text == '' and grid[row + 1][col - 1].text == 'O':
                                self.defends[(row, col)] -= 1
                        else: pass
                    elif col == 8:
                        if grid[row][col] == '':
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                self.attacks[(row, col)] += 1
                            elif grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row + 2][col - 2].text == 'S' and grid[row + 1][col - 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col - 1].text == '':
                                if grid[row - 2][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                                elif grid[row - 2][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                            if grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'O':
                                    self.defends[(row, col)] += 1
                                elif grid[row - 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                            if grid[row + 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row + 1][col].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'O':
                                    self.defends[(row, col)] += 1
                                elif grid[row + 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row + 1][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row + 1][col - 1].text == '':
                                if grid[row + 2][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                                elif grid[row + 2][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                            if grid[row][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row][col - 1].text == '':
                                if grid[row][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                                elif grid[row][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                            # relevant for all
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col].text == '' and grid[row - 1][col].text == 'O':
                                self.defends[(row, col)] -= 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col - 2].text == '' and grid[row - 1][col - 1].text == 'O':
                                self.defends[(row, col)] -= 1
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row][col - 2].text == '' and grid[row][col - 1].text == 'O':
                                self.defends[(row, col)] -= 1
                            # relevant also for 7
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row - 1][col].text == '' and grid[row  + 1][col].text == 'S':
                                self.defendo[(row, col)] -= 1
                            # relevant only here
                            if grid[row + 2][col].text == 'S' and grid[row + 1][col].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 2][col].text == '' and grid[row + 1][col].text == 'O':
                                self.defends[(row, col)] -= 1
                        else: pass
                elif row == 7:
                    if col == 0:
                        if grid[row][col].text == '':
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row - 1][col + 1].text == 'O' and grid[row - 2][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row - 2][col].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row - 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col + 1].text == '':
                                if grid[row - 2][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                            elif grid[row - 2][col + 2].text == 'O':
                                self.defends[(row, col)] += 1
                            if grid[row][col + 1].text == 'O':
                                self.defends[(row, col)] += 1
                            # relevant for all
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col].text == '' and grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] -= 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col].text == '' and grid[row][col + 2].text == 'S':
                                self.defends[(row, col)] -= 1
                            # relevant also from 7
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row - 1][col].text == '' and grid[row + 1][col].text == 'S':
                                self.defendo[(row, col)] -= 1
                        else: pass
                    elif col == 1:
                        if grid[row][col].text == '':
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row - 1][col - 1].text == 'S' and grid[row + 1][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'S' and grid[row - 1][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row - 1][col + 1].text == 'O' and grid[row - 2][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row - 2][col].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row - 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col + 1].text == '':
                                if grid[row - 2][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row - 2][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row][col + 1].text == '':
                                if grid[row][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row + 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row + 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            # relevant for all
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col].text == '' and grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] -= 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row][col - 1].text == '' and grid[row][col + 1].text == 'S':
                                self.defendo[(row, col)] -= 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row + 1][col].text == '' and grid[row][col + 2].text == 'S':
                                self.defends[(row, col)] -= 1
                            # relevant also from 7
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row - 1][col].text == '' and grid[row + 1][col].text == 'S':
                                self.defendo[(row, col)] -= 1
                            if grid[row - 1][col - 1].text == 'S' and grid[row + 1][col + 1].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row - 1][col - 1].text == '' and grid[row + 1][col + 1].text == 'S':
                                self.defendo[(row, col)] -= 1
                            if grid[row - 1][col + 1].text == 'S' and grid[row + 1][col - 1].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row - 1][col + 1].text == '' and grid[row + 1][col - 1].text == 'S':
                                self.defendo[(row, col)] -= 1
                        else: pass
                    elif 1 < col < 7:
                        if grid[row][col].text == '':
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col - 1].text == 'S' and grid[row + 1][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row - 1][col + 1].text == 'O' and grid[row - 2][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'S' and grid[row - 1][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col - 1].text == '':
                                if grid[row - 2][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row - 2][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row - 2][col].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row - 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col + 1].text == '':
                                if grid[row - 2][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row - 2][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row][col].text == '':
                                if grid[row][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row + 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row + 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row][col - 1].text == '':
                                if grid[row][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                                # relevant for all
                                if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == '':
                                    self.defends[(row, col)] -= 1
                                elif grid[row][col - 2].text == '' and grid[row][col - 1].text == 'O':
                                    self.defends[(row, col)] -= 1
                                if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == '':
                                    self.defendo[(row, col)] -= 1
                                elif grid[row][col - 1].text == '' and grid[row][col + 1].text == 'S':
                                    self.defendo[(row, col)] -= 1
                                if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == '':
                                    self.defends[(row, col)] -= 1
                                elif grid[row][col + 1].text == '' and grid[row][col + 2].text == 'S':
                                    self.defends[(row, col)] -= 1
                                if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == '':
                                    self.defends[(row, col)] -= 1
                                elif grid[row - 2][col - 2].text == '' and grid[row - 2][col - 1].text == 'O':
                                    self.defends[(row, col)] -= 1
                                if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == '':
                                    self.defends[(row, col)] -= 1
                                elif grid[row - 2][col].text == '' and grid[row - 1][col].text == 'O':
                                    self.defends[(row, col)] -= 1
                                if grid[row - 2][col + 2].text == 'S' and grid[row - 1][col + 1].text == '':
                                    self.defends[(row, col)] -= 1
                                elif grid[row - 2][col + 2].text == '' and grid[row - 1][col + 1].text == 'O':
                                    self.defends[(row, col)] -= 1
                                # relevant also for 7
                                if grid[row - 1][col - 1].text == 'S' and grid[row + 1][col + 1].text == '':
                                    self.defendo[(row, col)] -= 1
                                elif grid[row - 1][col - 1].text == '' and grid[row + 1][col + 1].text == 'S':
                                    self.defendo[(row, col)] -= 1
                                if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == '':
                                    self.defendo[(row, col)] -= 1
                                elif grid[row - 1][col].text == '' and grid[row + 1][col].text == 'S':
                                    self.defendo[(row, col)] -= 1
                                if grid[row + 1][col - 1].text == 'S' and grid[row - 1][col + 1].text == '':
                                    self.defendo[(row, col)] -= 1
                                elif grid[row + 1][col - 1].text == '' and grid[row - 1][col + 1].text == 'S':
                                    self.defendo[(row, col)] -= 1
                        else: pass
                    elif col == 7:
                        if grid[row][col].text == '':
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col - 1].text == 'S' and grid[row + 1][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'S' and grid[row - 1][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col - 1].text == '':
                                if grid[row - 2][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row - 2][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col].text == 'O':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row - 2][col].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row - 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row + 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row + 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col - 1].text == 'O':
                                self.defends[(row, col)] += 1
                            elif grid[row][col - 1].text == '':
                                if grid[row][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            # relevant for all
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row][col - 1].text == '' and grid[row][col + 1].text == 'S':
                                self.defendo[(row, col)] -= 1
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row][col - 2].text == '' and grid[row][col - 1].text == 'O':
                                self.defends[(row, col)] -= 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col - 2].text == '' and grid[row - 1][col - 1].text == 'O':
                                self.defends[(row, col)] -= 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col].text == '' and grid[row - 1][col].text == 'O':
                                self.defends[(row, col)] -= 1
                            # relevant also for 7
                            if grid[row - 1][col - 1].text == 'S' and grid[row + 1][col + 1].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row - 1][col - 1].text == '' and grid[row + 1][col + 1].text == 'S':
                                self.defendo[(row, col)] -= 1
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row - 1][col].text == '' and grid[row + 1][col].text == 'S':
                                self.defendo[(row, col)] -= 1
                            if grid[row + 1][col - 1].text == 'S' and grid[row - 1][col + 1].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row + 1][col - 1].text == '' and grid[row - 1][col + 1].text == 'S':
                                self.defendo[(row, col)] -= 1
                        else: pass
                    elif col == 8:
                        if grid[row][col].text == '':
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col - 1].text == '':
                                if grid[row - 2][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row - 2][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row - 2][col].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row + 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row + 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            if grid[row][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row][col - 1].text == '':
                                if grid[row][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            # relevant for all
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col].text == '' and grid[row - 1][col].text == 'O':
                                self.defends[(row, col)] -= 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col - 2].text == '' and grid[row - 1][col - 1].text == 'O':
                                self.defends[(row, col)] -= 1
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row][col - 2].text == '' and grid[row][col - 1].text == 'O':
                                self.defends[(row, col)] -= 1
                            # relevant also for 7
                            if grid[row - 1][col].text == 'S' and grid[row + 1][col].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row - 1][col].text == '' and grid[row + 1][col].text == 'S':
                                self.defendo[(row, col)] -= 1
                        else: pass
                elif row == 8:
                    if col == 0:
                        if grid[row][col].text == '':
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col + 1].text == 'O' and grid[row - 2][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row - 2][col].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row - 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col + 1].text == '':
                                if grid[row - 2][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row - 2][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col + 1].text == '':
                                if grid[row][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col].text == '' and grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] -= 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row][col + 1].text == '' and grid[row][col + 2].text == 'S':
                                self.defends[(row, col)] -= 1
                        else: pass
                    elif col == 1:
                        if grid[row][col].text == '':
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            elif grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col + 1].text == 'O' and grid[row - 2][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row - 2][col].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row - 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col + 1].text == '':
                                if grid[row - 2][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row - 2][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row][col + 1].text == '':
                                if grid[row][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col].text == '' and grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] -= 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row][col - 1].text == '' and grid[row][col + 1].text == 'S':
                                self.defendo[(row, col)] -= 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row][col + 1].text == '' and grid[row][col + 2].text == 'S':
                                self.defends[(row, col)] -= 1
                        else: pass
                    elif 1 < col < 7:
                        if grid[row][col].text == '':
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == 'S':
                                self.attacks[(row, col)] += 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 2][col + 2].text == 'S' and grid[row - 1][col + 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col - 1].text == '':
                                if grid[row - 2][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row - 2][col -2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row - 2][col].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row - 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col + 1].text == '':
                                if grid[row - 2][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row - 2][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row][col + 1].text == '':
                                if grid[row][col + 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row][col + 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row][col - 1].text == '':
                                if grid[row][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row][col - 2].text == '' and grid[row][col - 1].text == 'O':
                                self.defends[(row, col)] -= 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row][col - 1].text == '' and grid[row][col + 1].text == 'S':
                                self.defendo[(row, col)] -= 1
                            if grid[row][col + 1].text == 'O' and grid[row][col + 2].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row][col + 1].text == '' and grid[row][col + 2].text == 'S':
                                self.defends[(row, col)] -= 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col - 2].text == '' and grid[row - 2][col - 1].text == 'O':
                                self.defends[(row, col)] -= 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col].text == '' and grid[row - 1][col].text == 'O':
                                self.defends[(row, col)] -= 1
                            if grid[row - 2][col + 2].text == 'S' and grid[row - 1][col + 1].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col + 2].text == '' and grid[row - 1][col + 1].text == 'O':
                                self.defends[(row, col)] -= 1
                        else: pass
                    elif col == 7:
                        if grid[row][col].text == '':
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == 'S':
                                self.attacko[(row, col)] += 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col - 1].text == '':
                                if grid[row - 2][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row - 2][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row - 2][col].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row - 1][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row][col + 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col + 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            if grid[row][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row][col - 1].text == '':
                                if grid[row - 2][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row][col - 1].text == 'S' and grid[row][col + 1].text == '':
                                self.defendo[(row, col)] -= 1
                            elif grid[row][col - 1].text == '' and grid[row][col + 1].text == 'S':
                                self.defendo[(row, col)] -= 1
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row][col - 2].text == '' and grid[row][col - 1].text == 'O':
                                self.defends[(row, col)] -= 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col - 2].text == '' and grid[row - 1][col - 1].text == 'O':
                                self.defends[(row, col)] -= 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col].text == '' and grid[row - 1][col].text == 'O':
                                self.defends[(row, col)] -= 1
                        else: pass
                    elif col == 8:
                        if grid[row][col].text == '':
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == 'O':
                                self.attacks[(row, col)] += 1
                            if grid[row - 1][col - 1].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col - 1].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col - 1].text == '':
                                if grid[row - 2][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row - 2][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row - 1][col].text == 'S':
                                self.defends[(row, col)] += 1
                            elif grid[row - 1][col].text == 'O':
                                self.defendo[(row, col)] += 1
                            elif grid[row - 1][col - 1].text == '':
                                if grid[row - 2][col - 2].text == 'S':
                                    self.defendo[(row, col)] += 1
                                elif grid[row - 2][col - 2].text == 'O':
                                    self.defends[(row, col)] += 1
                            if grid[row - 2][col].text == 'S' and grid[row - 1][col].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col].text == '' and grid[row - 1][col].text == 'O':
                                self.defends[(row, col)] -= 1
                            if grid[row - 2][col - 2].text == 'S' and grid[row - 1][col - 1].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row - 2][col - 2].text == '' and grid[row - 1][col - 1].text == 'O':
                                self.defends[(row, col)] -= 1
                            if grid[row][col - 2].text == 'S' and grid[row][col - 1].text == '':
                                self.defends[(row, col)] -= 1
                            elif grid[row][col - 2].text == '' and grid[row][col - 1].text == 'O':
                                self.defends[(row, col)] -= 1
                        else: pass
        maxatt = 0
        maxattlist = list()
        maxdef = 0
        maxdeflist = list()
        defaultlist = list()
        for current in self.attacks:
            if self.attacks[current] > maxatt:
                maxatt = self.attacks[current]
        for current in self.attacko:
            if self.attacko[current] > maxatt:
                maxatt = self.attacko[current]
        for i in self.attacks:
            if self.attacks[i] == maxatt:
                maxattlist.append(Action(S, i, App.get_running_app().game.board.grid[i[0]][i[1]]))
        for i in self.attacko:
            if self.attacko[i] == maxatt:
                maxattlist.append(Action(O, i, App.get_running_app().game.board.grid[i[0]][i[1]]))
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
        if len(maxattlist) != 0:
            num = random.randint(1, len(maxattlist)) - 1
            chosen1 = maxattlist[num]
        elif len(maxattlist) == 0 and len(maxdeflist) != 0:
            num = random.randint(1, len(maxdeflist)) - 1
            chosen1 = maxdeflist[num]
        else:
            for i in range(9):
                for j in range(9):
                    if grid[i][j].text == '':
                        defaultlist.append(Action(S, i, App.get_running_app().game.board.grid[i][j]))
                        defaultlist.append(Action(O, i, App.get_running_app().game.board.grid[i][j]))
            num = random.randint(1, len(defaultlist)) - 1
            chosen1 = defaultlist[num]
        chosen1.take()