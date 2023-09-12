import numpy as np
import pyautogui

game_on =True

class board():
    def __init__(self):
        self.marks = np.full((3,3),9,dtype = np.int32)
        self.board = [[0]*5 for i in range(5)]

    def write_board(self):
        for i in range(5):
            for j in range(5):
                if i % 2 == 1:
                    if j < 4:
                        self.board[i][j] = "---"
                    else:
                        self.board[i][j] = str()
                elif i % 2 == 0 and j % 2 == 1:
                    self.board[i][j] = "|"
                else:
                    self.board[i][j] = "   "

    def show_board(self):
        for i in range(5):
            str_to_print = str()
            for j in range(5):
                if i%2 == 0 and j%2 == 0:
                    if self.marks[i//2][j//2] in [0,1]:
                        self.board[i][j] = ' X ' if self.marks[i//2][j//2] == 1 else ' O '
                str_to_print += self.board[i][j]
            print(str_to_print)

    def win_check(self):
        sign_to_check = 1 if player_1_turn else 0
        starting_positions = [
            [(0, 0), (0, 1), (0, 2)]
            , [(0, 0), (1, 0), (2, 0)]
            , [(0, 0)]
            , [(0, 2)]
        ]
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for item in directions:
            positions = directions.index(item)
            pos_x_direct = item[0]
            pos_y_direct = item[1]
            for item_y in starting_positions[positions]:
                win_condition = True
                current_pos_x = item_y[0]
                current_pos_y = item_y[1]
                for i in range(3):
                    if self.marks[current_pos_x][current_pos_y] != sign_to_check:
                        win_condition = False
                        break
                    current_pos_x += pos_x_direct
                    current_pos_y += pos_y_direct
                if win_condition:
                    return True
        return False


if __name__ == "__main__":
    new_board = board()
    new_board.write_board()
    player_1_turn = False
    while game_on:
        player_1_turn = not player_1_turn
        place_taken = True

        pyautogui.hotkey('ctrl', ';')
        new_board.show_board()
        print(f"Player {1 if player_1_turn else 2} Turn")
        while place_taken:
            try:
                x, y = map(int, input("Input x y positions separated by space: ").split())
                if new_board.marks[x][y] in [1,0]:
                    print("PLACE ON BOARD ALREADY TAKEN")
                    continue
            except IndexError:
                print("INDEX OUT OF SCOPE")
                continue
            except Exception as e:
                print(f"Error occurred : {e} Try again to input values")
                continue
            place_taken=False

        if player_1_turn:
            new_board.marks[x][y] = 1 #1 relates to X
        else:
            new_board.marks[x][y] = 0  #0 relates to O

        game_on = not new_board.win_check()

    pyautogui.hotkey('ctrl', ';')
    new_board.show_board()
    print(f"Player {1 if player_1_turn else 2} won!")












