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
    
    def in_bounds(self, r, c):
        return 0 <= r < 9 and 0 <= c < 9

    def calculate_immediate_attack(self, grid, r, c, char_to_place):
        """
        returns the number of SOS lines created immediately by placing char_to_place at (r, c).

        :param grid: the board
        :param r, c: coordinates of the cell
        :param char_to_place: 'S' or 'O'
        :returns: the number of SOS lines created
        """

        # 4 directions to check: horizontal, vertical, 2 diagonals.
        DIRECTIONS = [
            (0, 1),  # right
            (1, 0),  # down
            (1, 1),  # diagonal down-right
            (1, -1)  # diagonal down-left
        ]
        
        attacks = 0
        
        for dr, dc in DIRECTIONS:
            # --- checking for 'O' in the center: S O S ---
            if char_to_place == 'O':
                # looking for S (r-dr, c-dc) + O(r,c) + S(r+dr, c+dc)
                r_s1, c_s1 = r - dr, c - dc
                r_s2, c_s2 = r + dr, c + dc
                
                if self.in_bounds(r_s1, c_s1) and self.in_bounds(r_s2, c_s2):
                    if grid[r_s1][c_s1].text == 'S' and grid[r_s2][c_s2].text == 'S':
                        attacks += 1

            # --- checking for 'S' at the edges: S O S ---
            if char_to_place == 'S':
                # 1. looking for S(r,c) + O(r+dr, c+dc) + S(r+2dr, c+2dc)
                r_o1, c_o1 = r + dr, c + dc
                r_s2, c_s2 = r + 2 * dr, c + 2 * dc
                
                if self.in_bounds(r_o1, c_o1) and self.in_bounds(r_s2, c_s2):
                    if grid[r_o1][c_o1].text == 'O' and grid[r_s2][c_s2].text == 'S':
                        attacks += 1

                # 2. looking for S(r-2dr, c-2dc) + O(r-dr, c-dc) + S(r,c)
                r_s1, c_s1 = r - 2 * dr, c - 2 * dc
                r_o2, c_o2 = r - dr, c - dc
                
                if self.in_bounds(r_s1, c_s1) and self.in_bounds(r_o2, c_o2):
                    if grid[r_s1][c_s1].text == 'S' and grid[r_o2][c_o2].text == 'O':
                        attacks += 1
                        
        return attacks

    def doPriorityMove(self):
        grid = App.get_running_app().game.board.grid
        best_score = -float('inf') # best score found
        best_moves = []
        
        possible_moves = []
        for r in range(9):
            for c in range(9):
                if grid[r][c].text == '':
                    # all possible moves: (row, column, 'S' or 'O')
                    possible_moves.append((r, c, 'S'))
                    possible_moves.append((r, c, 'O'))

        # If there are no available moves (the board is full)
        if not possible_moves:
            return

        for r, c, char in possible_moves:

            # 1. Calculate the offensive score (O_Score)
            offensive_score = self.calculate_immediate_attack(grid, r, c, char)

            # Prepare the board for simulating the opponent's move
            original_text = grid[r][c].text # Expected to be ''
            grid[r][c].text = char # Temporarily place my move

            # 2. Calculate the maximum attack potential of the opponent after my move (D_Score)
            # The opponent will try to maximize their score in the next turn.
            max_opponent_attack = 0

            # Find all empty cells after my move
            opponent_possible_moves = []
            for r_op in range(9):
                for c_op in range(9):
                    if grid[r_op][c_op].text == '':
                        opponent_possible_moves.append((r_op, c_op, 'S'))
                        opponent_possible_moves.append((r_op, c_op, 'O'))

            # Simulate the opponent's best move
            for r_op, c_op, char_op in opponent_possible_moves:
                opponent_attack = self.calculate_immediate_attack(grid, r_op, c_op, char_op)
                max_opponent_attack = max(max_opponent_attack, opponent_attack)

            # 3. Restore the board state
            grid[r][c].text = original_text # Expected to be ''

            # 4. Calculate the total score (Total Score)
            # The total score: immediate gain minus potential loss
            total_score = offensive_score - max_opponent_attack

            # 5. Update the list of best moves
            if total_score > best_score:
                best_score = total_score
                # Reset and add the current best move
                chosen_char = S if char == 'S' else O
                best_moves = [Action(chosen_char, (r, c), grid[r][c])]
            elif total_score == best_score:
                # Add to the list of equally good moves
                chosen_char = S if char == 'S' else O
                best_moves.append(Action(chosen_char, (r, c), grid[r][c]))

        # --- Final Step: Make the Decision ---

        # Random choice among the moves with the highest score
        chosen1 = random.choice(best_moves)

        # Execute the chosen move
        chosen1.take()
        # chosen1.cell.text = chosen1.let
        self.put()
        # You can remove the following dictionaries: self.attacks, self.attacko, self.defends, self.defendo
        # since they are no longer in use
        self.attacks.clear()
        self.attacko.clear()
        self.defends.clear()
        self.defendo.clear()