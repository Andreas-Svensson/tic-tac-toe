import numpy as np
import os

class Game():
    def __init__(self, board_size = 3) -> None:
        self.is_running = True
        self.winner = None
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size))
        self.max_turns = board_size * board_size # turns before board is full
        self.turns_played = 1
        self.turn = np.random.randint(1, 3) # initial value decides which player goes first
        self.win_sequence = [np.array([1] * board_size), np.array([2] * board_size)] # sequence to be found on board to win game


    def input_placement(self):
        placement = input(f"Player {self.turn}: Make your move")
        return placement


    def extract_numbers(self, player_input):
        numbers = []
        for char in player_input:
            if char.isdigit():
                numbers.append(int(char))
                if len(numbers) == 2:
                    break
        if len(numbers) == 2:
            return numbers[0], numbers[1]
        else:
            return None, None


    def check_placement(self, x, y):

        # check if no numerical values were entered
        if x == None and y == None:
            return "No values entered for placement"
        if x == None:
            return "No value entered for x-position"
        if y == None:
            return "No value entered for y-position"

        # check if integer was entered (redundant)
        if type(x) != int:
            return "X-position must be a whole number"
        if type(y) != int:
            return "Y-position must be a whole number"
        
        # check if value larger than board size was entered
        if x > self.board_size - 1 or y > self.board_size - 1:
            return "Placement falls outside board. Too large value entered"
        if x < 0 or y < 0:
            return "Placement falls outside board. Too small value entered"

        # check if negative value was entered
        if self.board[x, y] != 0:
            return "Invalid placement, that position is already taken"

        return      


    def place(self, x, y):
        self.board[x, y] = self.turn


    def check_winner(self):
        # Check if the win sequence is present in any row
        if any(np.all(row == self.win_sequence[self.turn - 1]) for row in self.board):
            print("Win sequence found in a row")
            self.winner = self.turn

        # Check if the win sequence is present in any column
        if any(np.all(col == self.win_sequence[self.turn - 1]) for col in self.board.T):
            print("Win sequence found in a column")
            self.winner = self.turn

        # Check if the win sequence is present in the diagonal
        if np.all(np.diag(self.board) == self.win_sequence[self.turn - 1]) or np.all(np.diag(self.board[::-1]) == self.win_sequence[self.turn - 1]):
            print("Win sequence found in a diagonal")
            self.winner = self.turn

        if self.winner:
            self.is_running = False
            return f"Player {self.turn} wins!"

        return


    def check_draw(self):
        if self.turns_played == self.max_turns:
            self.is_running == False
            return "No more available spaces. It's a draw!"


    def next_turn(self):
        self.turns_played += 1
        if self.turn == 1:
            return 2
        return 1

# ######################################################################################

if __name__ == "__main__":
    game = Game()
    os.system("cls") # clear console
    print(game.board) # print board

    while game.is_running == True:

        player_input = game.input_placement() # allow player to make a move

        x, y = game.extract_numbers(player_input) # pick out 2 numerical values

        # invalid placement gets a value if no valid placement for x, y was found
        invalid_placement = game.check_placement(x, y)
        if invalid_placement:
            print(invalid_placement)
            continue # go back to start of the game loop

        game.place(x, y) # update board values

        os.system("cls") # clear console

        print(game.board) 

        win = game.check_winner()
        if win:
            print(win)
        
        draw = game.check_draw()
        if draw:
            print(draw)
        
        game.turn = game.next_turn()

        