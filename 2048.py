# 2048 game in Python with OOP logic
# Utku Elagoz 2024

import random
import os
import keyboard
import time
import re
import math

class Game_2048():

    def __init__(self) -> None:
        
        self.board= [[0]*4 for i in range(4)]
        self.move_made_flag = True
        self.end_game_flag = False

        while True:
            self.gameplay()

    def keyboard_arrow(self) -> str:
        
        while True:

            if keyboard.is_pressed('right'):
                return 'r'
            elif keyboard.is_pressed('left'):
                return 'l'
            elif keyboard.is_pressed('up'):
                return 'u'
            elif keyboard.is_pressed('down'):
                return 'd'
        
            time.sleep(0.1)

    def display_board(self, board):
        
        os.system('cls')
        def colorize_output(output):
            color_map = {
                0: '\033[0m',    # Reset color
                2: '\033[93m',   # Yellow
                4: '\033[94m',   # Blue
                8: '\033[91m',   # Red
                16: '\033[92m',  # Green
                32: '\033[96m',  # Cyan
                64: '\033[95m',  # Magenta
                128: '\033[38;5;208m', # Orange
                256: '\033[30;102m',  # Black on Green
                512: '\033[30;101m',  # Black on Red
                1024: '\033[30;103m', # Black on Yellow
                2048: '\033[30;45m',  # Black on Magenta
            }

            colored_output = ""
            lines = output.split('\n')

            for line in lines:
                for key, color_code in color_map.items():

                    line = re.sub(rf'(?<!\d){key}(?!\d)', f'{color_code}{key}\033[0m', line)
                colored_output += line + '\n'

            return colored_output


        output = "|-----|-----|-----|-----|\n"
        for i in range(4):
            for j in range(4):
                cell_value = str(board[i][j])
                padding = " " * (5 - len(cell_value))
                
                left_padding = " " * math.floor(len(padding) / 2)
                right_padding = " " * math.ceil(len(padding) / 2)
            
                output += f"|{left_padding}{cell_value}{right_padding}"
                
                if j == 3:
                    output += "|\n|-----|-----|-----|-----|\n"

        colored_output = colorize_output(output)
        print(colored_output)

    def make_move(self) -> bool:
        initial_board = self.board.copy()
        new_board = []
        board = self.board
        
        move = self.keyboard_arrow()

        def rotate_90_clockwise(board):
            return [list(row[::-1]) for row in zip(*board)]

        def rotate_90_counterclockwise(matrix):
            transposed_matrix = [list(row) for row in zip(*matrix)]
            rotated_matrix = transposed_matrix[::-1]
            return rotated_matrix

        def rotate_180(matrix):
            return [row[::-1] for row in matrix[::-1]]        

        def calculate_move(board):
            
            new_board = []
            for row in board:
                non_zeros = [x for x in row if x != 0]
                i=0
                new_row = []
                while i < len(non_zeros):
                    if i + 1 < len(non_zeros) and non_zeros[i] == non_zeros[i + 1]:
                        new_row.append(non_zeros[i]*2)
                        i = i + 2

                    else:
                        new_row.append(non_zeros[i])
                        i = i + 1
                
                row = new_row + [0]*(4-len(new_row))
                new_board.append(row)
            
            return new_board
        
        if move == 'l':

            new_board = calculate_move(board)

        elif move == 'r':

            turned_board = rotate_180(board)
            move_board = calculate_move(turned_board)
            new_board = rotate_180(move_board)

        elif move == 'd':

            turned_board = rotate_90_clockwise(board)
            move_board = calculate_move(turned_board)
            new_board = rotate_90_counterclockwise(move_board)

        elif move == 'u':

            turned_board = rotate_90_counterclockwise(board)
            move_board = calculate_move(turned_board)
            new_board = rotate_90_clockwise(move_board)

        if new_board == initial_board:
            self.move_made_flag = False
        else:
            self.move_made_flag = True

        self.board= new_board

        return self.move_made_flag
    
    def number_spawn(self) -> None:

        weights = [0.70, 0.28, 0.015, 0.005]
        new_number = random.choices([2,4,8,16], weights = weights)[0]

        weights_row = [0.72, 0.26, 0.015, 0.005]
        new_place_column = random.choice([0,1,2,3])
        new_place_row = random.choices([0,1,2,3], weights=weights_row)[0]
        

        #self.display_board()
        if self.board[new_place_row][new_place_column] == 0:
            self.board[new_place_row][new_place_column] = new_number
            self.display_board(self.board)
            return
        
        while self.board[new_place_row][new_place_column] != 0:
            new_place_column = random.choice([0,1,2,3])
            new_place_row = random.choices([0,1,2,3], weights=weights_row)[0]

        self.board[new_place_row][new_place_column] = new_number
        self.display_board(self.board)
        return

    def endgame_check(self) -> bool:
    
        for i in range(4):
            for j in range(4):
                if i-1 >= 0 and self.board[i][j] == self.board[i - 1][j]:    
                    return False
                if j - 1 >= 0 and self.board[i][j] == self.board[i][j - 1]:
                    return False
                            
        return True

    
    def gameplay(self):
        
        self.number_spawn()
        while self.end_game_flag == False:
            
            self.move_made_flag  = self.make_move()
            self.display_board(self.board)

            if self.move_made_flag == True:
                self.number_spawn()

            if all(0 not in row for row in self.board):
                self.end_game_flag = self.endgame_check()

            time.sleep(0.1)
        
        print(f"Your score is {max(max(row) for row in self.board)}!")
        print("Thank you for playing!")

if __name__ == "__main__":

    game = Game_2048()



    

