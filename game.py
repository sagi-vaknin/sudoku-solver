import numpy as np
import requests

class Sudoku:
    def __init__(self):
        self.board = self.init_board()
        self.solve_mode = False

    def init_board(self):
        """ Retrieves a random board from the api """

        url = "https://sudoku-api.vercel.app/api/dosuku?query={newboard(limit:1){grids{value}}}"    
        response = requests.get(url)
        board = response.json()["newboard"]["grids"][0]["value"]
        return np.array(board)

    def print_board(self):
        """ Prints current board status """
        board_str = self.board.astype(str)
        row_sep = '-'*25

        for i in range(9):
            if i % 3 == 0:
                print(row_sep)

            row = board_str[i]
            print('| '+' '.join(row[0:3])+' | '+' '.join(row[3:6])+' | '+' '.join(row[6:])+' |')

        print(row_sep)

    def insert_number(self, number, position):
        """ inserts number into position at current board """
        x, y = position
        self.board[x, y] = number

    def validate_current_number(self, number, position):
        """ validates if the current input adheres game rules """
        row = self.board[position[0]]
        col = self.board[:, position[1]]

        subgrid_row = (position[0] // 3) * 3
        subgrid_col = (position[1] // 3) * 3
        subgrid = self.board[subgrid_row : subgrid_row + 3, subgrid_col : subgrid_col + 3]

        if number in row or number in col or number in subgrid:
            return False
        return True

    def add_value(self, number, position):
        """ tries to add value into position """
        if self.validate_current_number(number, position):
            self.insert_number(number, position)
            return True
        else:
            if not self.solve_mode:
                print("can not put desired value in this position")
            return False
        
    def find_empty_cell(self):
        """ finds the first empty cell in the current board """
        x, y = self.board.shape
        for i in range(x):
            for j in range(y):
                if self.board[i, j] == 0:
                    return (i, j)
        return None

    def solve(self):
        """ solves current board using backtracking algorithm """
        self.solve_mode = True
        
        if np.all(self.board != 0):
            return True
        else:
            pos = self.find_empty_cell()

            for num in range(1, 10):
                if self.add_value(num, pos):
                    if self.solve():
                        return True
                    else:
                        self.board[pos[0], pos[1]] = 0
            return False
    

def validate_user_input(user_input):
    """ validates user input is in correct format """
    input_parts = user_input.split(",")
    input_parts = [e.strip() for e in input_parts]
    
    valid_nums = list(range(1,10))
    valid_coords = list(range(0,9))

    if len(input_parts) != 3:
        return None
    try:
        num, row, col = int(input_parts[0]), int(input_parts[1]), int(input_parts[2])
        if num in valid_nums and row in valid_coords and col in valid_coords:
            return (num, row, col)
        return None
    except ValueError:
        return None

def play_game(game):
    """ command line game engine """
    while True:
        game.print_board()
        print("Press 'q' to quit.")

        user_input = input("Enter your choice: 'number, row, col'. ")
        if user_input.lower() == 'q':
            print("quitting")
            break
        res = validate_user_input(user_input)
        if res is None:
            print("invalid input format")
            continue

        num, x, y = res
        if game.add_value(num, (x,y)):
            print("number inserted, think about ur next move")
        
        if np.all(game.board != 0):
            print("Congrats, you've finished!")
            game.print_board()
            break