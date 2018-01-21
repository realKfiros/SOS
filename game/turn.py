import random
from kivy.app import App
from action import Action

NONE = 0
S = 1
O = 2


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
                            if grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'S':
                                    self.defendo[(row, col)] = 1
                            if grid[row][col + 1].text == '':
                               if grid[row][col + 2].text == 'S':
                                   if self.defendo.has_key((row, col)):
                                       self.defendo[(row, col)] += 1
                                   else:
                                       self.defendo[(row, col)] = 1
                            if grid[row + 1][col + 1].text == '':
                               if grid[row + 2][col + 2].text == 'S':
                                   if self.defendo.has_key((row, col)):
                                       self.defendo[(row, col)] += 1
                                   else:
                                       self.defendo[(row, col)] = 1
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
                            if grid[row][col + 1].text == '':
                                if grid[row][col + 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                elif grid[row][col + 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                elif grid[row + 2][col].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row + 1][col + 1].text == '':
                                if grid[row + 2][col + 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                elif grid[row + 2][col + 2].text == 'O':
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
                            if grid[row][col - 1].text == '':
                                if grid[row][col - 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                elif grid[row][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row + 1][col - 1].text == '':
                                if grid[row + 2][col - 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                elif grid[row + 2][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row][col + 1].text == '':
                                if grid[row][col + 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                elif grid[row][col + 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                elif grid[row + 2][col].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row + 1][col + 1].text == '':
                                if grid[row + 2][col + 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                elif grid[row + 2][col + 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
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
                            if grid[row][col - 1].text == '':
                                if grid[row][col - 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                elif grid[row][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                elif grid[row + 2][col].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row + 1][col - 1].text == '':
                                if grid[row + 2][col - 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                elif grid[row + 2][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
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
                            if grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'S':
                                    self.defendo[(row, col)] = 1
                            if grid[row][col - 1].text == '':
                               if grid[row][col - 2].text == 'S':
                                   if self.defendo.has_key((row, col)):
                                       self.defendo[(row, col)] += 1
                                   else:
                                       self.defendo[(row, col)] = 1
                            if grid[row + 1][col - 1].text == '':
                               if grid[row + 2][col - 2].text == 'S':
                                   if self.defendo.has_key((row, col)):
                                       self.defendo[(row, col)] += 1
                                   else:
                                       self.defendo[(row, col)] = 1
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
                            if grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'S':
                                    self.defendo[(row, col)] = 1
                            if grid[row][col + 1].text == '':
                               if grid[row][col + 2].text == 'S':
                                   if self.defendo.has_key((row, col)):
                                       self.defendo[(row, col)] += 1
                                   else:
                                       self.defendo[(row, col)] = 1
                            if grid[row + 1][col + 1].text == '':
                               if grid[row + 2][col + 2].text == 'S':
                                   if self.defendo.has_key((row, col)):
                                       self.defendo[(row, col)] += 1
                                   else:
                                       self.defendo[(row, col)] = 1
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
                            if grid[row][col + 1].text == '':
                                if grid[row][col + 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                elif grid[row][col + 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                elif grid[row + 2][col].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row + 1][col + 1].text == '':
                                if grid[row + 2][col + 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                elif grid[row + 2][col + 2].text == 'O':
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
                            if grid[row][col - 1].text == '':
                                if grid[row][col - 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                elif grid[row][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row + 1][col - 1].text == '':
                                if grid[row + 2][col - 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                elif grid[row + 2][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row][col + 1].text == '':
                                if grid[row][col + 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                elif grid[row][col + 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                elif grid[row + 2][col].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row + 1][col + 1].text == '':
                                if grid[row + 2][col + 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                elif grid[row + 2][col + 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
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
                            if grid[row][col - 1].text == '':
                                if grid[row][col - 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                elif grid[row][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                elif grid[row + 2][col].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row + 1][col - 1].text == '':
                                if grid[row + 2][col - 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                elif grid[row + 2][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
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
                            if grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'S':
                                    self.defendo[(row, col)] = 1
                            if grid[row][col - 1].text == '':
                               if grid[row][col - 2].text == 'S':
                                   if self.defendo.has_key((row, col)):
                                       self.defendo[(row, col)] += 1
                                   else:
                                       self.defendo[(row, col)] = 1
                            if grid[row + 1][col - 1].text == '':
                               if grid[row + 2][col - 2].text == 'S':
                                   if self.defendo.has_key((row, col)):
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
                            if grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                if grid[row - 2][col].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                if grid[row + 2][col].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row][col + 1].text == '':
                                if grid[row][col + 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                if grid[row][col + 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row - 1][col + 1].text == '':
                                if grid[row - 2][col + 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                if grid[row - 2][col + 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row + 1][col + 1].text == '':
                                if grid[row + 2][col + 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                if grid[row + 2][col + 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
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
                            if grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                if grid[row - 2][col].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                if grid[row + 2][col].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row][col + 1].text == '':
                                if grid[row][col + 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                if grid[row][col + 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row - 1][col + 1].text == '':
                                if grid[row - 2][col + 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                if grid[row - 2][col + 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row + 1][col + 1].text == '':
                                if grid[row + 2][col + 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                                if grid[row + 2][col + 2].text == 'O':
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
                            elif grid[row - 1][col - 1].text == '':
                                if grid[row - 2][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col - 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
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
                            elif grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col].text == 'S':
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
                            elif grid[row - 1][col + 1].text == '':
                                if grid[row - 2][col + 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col + 2].text == 'S':
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
                            elif grid[row][col + 1].text == '':
                                if grid[row][col + 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row][col + 2].text == 'S':
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
                            elif grid[row + 1][col + 1].text == '':
                                if grid[row + 2][col + 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row + 2][col + 2].text == 'S':
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
                            elif grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row + 2][col].text == 'S':
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
                            elif grid[row + 1][col - 1].text == '':
                                if grid[row + 2][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row + 2][col - 2].text == 'S':
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
                            elif grid[row][col - 1].text == '':
                                if grid[row][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row][col - 2].text == 'S':
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
                            elif grid[row - 1][col - 1].text == '':
                                if grid[row - 2][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col - 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
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
                            elif grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col].text == 'S':
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
                            elif grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row + 2][col].text == 'S':
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
                            elif grid[row + 1][col - 1].text == '':
                                if grid[row + 2][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row + 2][col - 2].text == 'S':
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
                            elif grid[row - 1][col].text == '':
                                if grid[row][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row][col - 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defendo[(row, col)] = 1
                        else: pass
                    elif col == 8:
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
                            elif grid[row - 1][col - 1].text == '':
                                if grid[row - 2][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col - 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
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
                            elif grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col].text == 'S':
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
                            elif grid[row + 1][col].text == '':
                                if grid[row + 2][col].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row + 2][col].text == 'S':
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
                            elif grid[row + 1][col - 1].text == '':
                                if grid[row + 2][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row + 2][col - 2].text == 'S':
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
                            elif grid[row][col - 1].text == '':
                                if grid[row][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row][col - 2].text == 'S':
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
                            elif grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'S':
                                    self.defendo[(row, col)] = 1
                                elif grid[row - 2][col].text == 'O':
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
                            elif grid[row - 1][col + 1].text == '':
                                if grid[row - 2][col + 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            elif grid[row - 2][col + 2].text == 'O':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            if grid[row][col + 1].text == 'O':
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
                            elif grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
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
                            elif grid[row - 1][col + 1].text == '':
                                if grid[row - 2][col + 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col + 2].text == 'O':
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
                            elif grid[row][col + 1].text == '':
                                if grid[row][col + 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row][col + 2].text == 'O':
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
                            elif grid[row - 1][col - 1].text == '':
                                if grid[row - 2][col - 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
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
                            elif grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
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
                            elif grid[row - 1][col + 1].text == '':
                                if grid[row - 2][col + 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col + 2].text == 'O':
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
                            elif grid[row][col].text == '':
                                if grid[row][col + 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row][col + 2].text == 'O':
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
                                if self.defendo.has_key((row, col)):
                                    self.defendo[(row, col)] += 1
                                else:
                                    self.defendo[(row, col)] = 1
                            elif grid[row][col - 1].text == '':
                                if grid[row][col - 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
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
                            elif grid[row - 1][col - 1].text == '':
                                if grid[row - 2][col - 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
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
                            elif grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col].text == 'O':
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
                            elif grid[row][col - 1].text == '':
                                if grid[row][col - 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row][col - 2].text == 'O':
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
                            elif grid[row - 1][col - 1].text == '':
                                if grid[row - 2][col - 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
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
                            elif grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col].text == 'O':
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
                            elif grid[row][col - 1].text == '':
                                if grid[row][col - 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
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
                            elif grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row - 1][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row - 1][col + 1].text == '':
                                if grid[row - 2][col + 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col + 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                            if grid[row][col + 1].text == 'S':
                                if self.defends.has_key((row, col)):
                                    self.defends[(row, col)] += 1
                                else:
                                    self.defends[(row, col)] = 1
                            elif grid[row][col + 1].text == '':
                                if grid[row][col + 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row][col + 2].text == 'O':
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
                            elif grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
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
                            elif grid[row - 1][col + 1].text == '':
                                if grid[row - 2][col + 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col + 2].text == 'O':
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
                            elif grid[row][col + 1].text == '':
                                if grid[row][col + 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row][col + 2].text == 'O':
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
                            elif grid[row - 1][col - 1].text == '':
                                if grid[row - 2][col - 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col -2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
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
                            elif grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
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
                            elif grid[row - 1][col + 1].text == '':
                                if grid[row - 2][col + 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col + 2].text == 'O':
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
                            elif grid[row][col + 1].text == '':
                                if grid[row][col + 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row][col + 2].text == 'O':
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
                            elif grid[row][col - 1].text == '':
                                if grid[row][col - 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
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
                            elif grid[row - 1][col - 1].text == '':
                                if grid[row - 2][col - 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
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
                            elif grid[row - 1][col].text == '':
                                if grid[row - 2][col].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
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
                            elif grid[row][col - 1].text == '':
                                if grid[row - 2][col - 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
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
                            elif grid[row - 1][col - 1].text == '':
                                if grid[row - 2][col - 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
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
                            elif grid[row - 1][col - 1].text == '':
                                if grid[row - 2][col - 2].text == 'S':
                                    if self.defendo.has_key((row, col)):
                                        self.defendo[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
                                elif grid[row - 2][col - 2].text == 'O':
                                    if self.defends.has_key((row, col)):
                                        self.defends[(row, col)] += 1
                                    else:
                                        self.defends[(row, col)] = 1
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