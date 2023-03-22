###########################################
#                                         #
#   Python Project : A Tetris-Like Game   #
#   MEUNIER Antoine, BUDAR Maxime         #
#   EFREI, 2022                           #
#                                         #
###########################################

# This file contains every functions needed in the game.

from random import sample
from copy import deepcopy
from math import ceil
from os.path import isfile
from block_general import block_list

import os 
if os.name == "nt": CLS_COMMAND = "cls"
if os.name == "posix": CLS_COMMAND = "clear"

# Lists containing every block possible for each board type
circle_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
diamond_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,32,33,34,35,36,37,38,39,40,41,42,30,28,20]
triangle_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,44,45,46,47,48,49,50,51,52,53,54]
general_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]

# Convert a .txt file given by it's path to a 2D matrix of the board
# Returns a 2D matrix of the board if sucessful, 
def read_grid(path) -> list:
    try:
        board = open(path, 'r+')
    except FileNotFoundError:
        print(f"No grid exists at {path}.")
        return []

    lines = board.readlines()

    # Converts the lines gotten from the .readlines() function
    # to a 2D matrix.
    grid = []
    for line in lines:
        line = line .replace("\n", "") .split(" ")
        grid.append(line)

    board.close()
    return grid

# Convert a 2D matrix in a .txt file in the same format as the default board
# Returns a 0 if the file was saved sucessfuly, or a 1 if the file wasn't saved
def save_grid(path, grid) -> int:
    if isfile(path):
        print(f"File {path} alredy exists. Do you wish to overwrite ?\n    [Y/N] ", end="")
        c = input()
        if c.lower() == 'n':
            return 1
    
    new_board = open(path, 'w')
        
    for line in grid:
        for cell in line:
            new_board.write(cell + " ")
        new_board.write('\n')

    new_board.close()
    return 0

# Print the board to a readable format
def print_grid(grid) -> None:
    col_letters = "abcdefghijklmnopqrstuvwxyz"
    row_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    nb_col = len(grid[0])
    nb_row = len(grid)

    # Print the top letters
    print("    ", end="")
    for i in range(nb_col):
        print(col_letters[i%26], end=" ")
    print()

    # Print the top border of the board
    print("  ╔═", end="")
    for i in range(nb_col):
        print("══", end="")
    print("╗")

    # Print the middle of the board
    for i in range(nb_row):

        # Print the left letters and border of the board
        print(row_letters[i%26]+" ║ ", end="")

        for c in grid[i]:
            if c=='0': print(" ", end=" ")
            if c=='1': print("·", end=" ")
            if c=='2': print("■", end=" ")

        # Print the right border of the board
        print("║")

    # Print the bottom border of the board
    print("  ╚═", end="")
    for i in range(nb_col):
        print("══", end="")
    print("╝")

# Print the available blocks
# "blocs" is a list containing all the available blocks for this turn
# If pol = 2, then number the blocks 1, 2 and 3
# If pol = 1, show every block, with 10 blocks per line shown
def print_blocs(blocs, pol) -> None:
    if pol == 2 : 
        len_line = 3
    else: 
        len_line = 10

    # If there is a lot of available blocks (if pol=1), then allow 
    # blocks to be shown on multiple lines
    for az in range(ceil(len(blocs)/len_line)):
        for row in range(5):
            for bloc in blocs[len_line*az: len_line*(az+1)]:
                current_line = block_list[bloc][row]
                for cell in current_line:
                    if cell==0 : print(" ", end=" ")
                    if cell==1 : print("■", end=" ")
                print("   ", end="")
            print()
        print()
    
        for n in range(len_line*az, len_line*(az+1)):
            print("{:<13d}".format(n+1), end="")
        print("\n")

# Print the score
def print_score(score) -> None:
    print(f"""  ╔═══════════════════════════════════════╗
  ║  SCORE : {score:<29}║
  ╚═══════════════════════════════════════╝
    """)

# Return the list of blocks available
# If pol = 2, return a list containing 3 random block from the list
# If pol = 1, return the entire list
def select_bloc(list_of_blocs, pol) -> list:
    if pol == 1:
        return list_of_blocs
    if pol == 2:
        return sample(list_of_blocs, 3)

    return []

# Check if a block can be placed on the board at an (x,y) location
# (x,y) refers to the bottom-left corner of the block
# Return True if the block can be placed, False otherwise
def valid_position(grid, bloc, x, y) -> bool:
    nb_col = len(grid[0])

    if grid[y][x] == 0:
        return False
    
    # Go through every cell of the block
    # "y-(4-i)" is used to go through the y position of the block backward
    # because (x,y) correspond to the bottom-left corner of the block
    for i in range(5):
        for j in range(5):
            cell = bloc[i][j]

            # Ignore if cell is empty
            if cell == 0:
                continue

            if y-(4-i) < 0 or x+j >= nb_col:
                return False

            if grid[y-(4-i)][x+j] in ('0','2'):
                return False

    return True

# Place a block on the board at an (x,y) location
# (x,y) refers to the bottom-left corner of the block
# Return the board with the block placed
def place_bloc(grid, bloc, x, y) -> list:
    for i in range(5):
        for j in range(5):
            cell = bloc[i][j]

            # Ignore if cell is empty
            if cell == 0:
                continue

            grid[y-(4-i)][x+j] = '2'
            
    return grid

# Check if a row at index i is complete
# Return True if the row is complete, False otherwise
def row_state(grid, i) -> bool:
    return '1' not in grid[i]

# Clear a row at index i
# Return a tuple containing the new board and the score gained from this row 
# NOTE: This function does not modify the board given in its parameters
def row_clear(grid, i) -> tuple:
    temp_grid = deepcopy(grid)
    score = 0

    for c in range(len(temp_grid[i])):
        if temp_grid[i][c] != '0' :
            temp_grid[i][c] = '1'
            score += 1

    return temp_grid, score

# Check if a column at index j is complete
# Return True if the column is complete, False otherwise
def col_state(grid, j) -> bool:
    for c in range(len(grid)):
        if grid[c][j] == '1':
            return False

    return True

# Clear a column at index j
# Return a tuple containing the new board and the score gained from this column 
# NOTE: This function does not modify the board given in its parameters
def col_clear(grid, j) -> tuple:
    temp_grid = deepcopy(grid)
    score = 0

    for i in range(len(temp_grid)):
        if temp_grid[i][j] != '0':
            temp_grid[i][j] = '1'
            score += 1

    return temp_grid, score

# Make the row above the row at index i fall down 1 row
# Calls itself recursively to make every row above row at index i fall
# If i = 0, that is the top row, return itself, as there are no row above
# Return the new board
# NOTE: This function does not modify the board given in its parameters
def make_bloc_fall(grid, i):
    if i <= 0:
        return grid
    temp_grid = deepcopy(grid)

    for it, j in enumerate(grid[i-1]):
        if j == '0': continue
        if temp_grid[i][it] != '0':
            temp_grid[i][it] = temp_grid[i-1][it]
        temp_grid[i-1][it] = '1'

    temp_grid = make_bloc_fall(temp_grid, i-1)

    return temp_grid

# Check if any row and column are completed. If it is the case, clear them
# Return the new board
# NOTE: This function does not modify the board given in its parameters
def clear_rows_and_col(grid) -> tuple:
    temp_grid = deepcopy(grid)
    score = 0

    for i in range(len(grid)):
        if row_state(grid, i): 
            temp_grid, s = row_clear(temp_grid, i)
            temp_grid = make_bloc_fall(temp_grid, i)
            score += s

    for j in range(len(grid[0])):
        if col_state(grid, j): 
            temp_grid, s = col_clear(temp_grid, j)
            score += s

    return temp_grid, score

# Get the block list associated with a board
# "path" refers to the path to the file
# Return a list containing the blocks available
def get_block_list(path) -> list:
    if path == "board_shapes/circle.txt":
        return circle_list
    elif path == "board_shapes/diamond.txt":
        return diamond_list
    elif path == "board_shapes/triangle.txt":
        return triangle_list
    else:
        return general_list

# Menu Functions

# Print the main menu, and ask the user where to go next
# Return an integer, corresponding to where to go next
def show_menu() -> int:
    os.system(CLS_COMMAND)

    save = isfile("save.txt")
    if save: options = (1,2,3,4)
    else: options = (1,3,4)

    print(f"""
     ████████╗███████╗██████╗ ██████╗ ██╗███████╗
     ╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██║██╔════╝
        ██║   █████╗  ██████╔╝██████╔╝██║███████╗
        ██║   ██╔══╝  ██╔═══╝ ██╔══██╗██║╚════██║
        ██║   ███████╗██║     ██║  ██║██║███████║
        ╚═╝   ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝
                                              

    [1] Start Game
    [2] Resume Game {"(Not Available)" if not save else ""}
    [3] Show Rules
    [4] Exit
    """)

    choice = 0
    
    while choice not in options:
        choice = better_int_input("    [?] ")

    return choice

# Print the board selection menu, and ask the user what board to play on
# Return the path to the file containing the board
def select_board() -> str:
    os.system(CLS_COMMAND)
    path = ""
    options = (1,2,3,4,5,6)
    print("""╔════════════════════════════════════════════════════╗
║                  SELECT THE BOARD                  ║
╚════════════════════════════════════════════════════╝

    [1] Circle
    [2] Diamond
    [3] Triangle
    [4] Custom
    [5] Go Back
""")
    choice = 0
    
    while choice not in options:
        choice = better_int_input("    [?] ")

    if choice == 1:
        path = "board_shapes/circle.txt"
    elif choice == 2:
        path = "board_shapes/diamond.txt"
    elif choice == 3:
        path = "board_shapes/triangle.txt"
    elif choice == 4:
        print("    Enter the board name (in \"board_shape\" folder)")
        path = input("    > ")
        path = "board_shapes/" + path + ".txt"
    elif choice == 5:
        path = ""
    
    return path

# Print the policy selection menu, and ask the user what policy to use
# Return the policy to use
def select_policy() -> int:
    print("""╔════════════════════════════════════════════════════╗
║                  SELECT A POLICY                   ║
╚════════════════════════════════════════════════════╝

    [1] All blocks available
    [2] 3 random blocks each turn
    [3] Go Back
""")

    pol = 0
    while pol not in (1,2,3):
        pol = better_int_input("    [?] ")

    return pol

# Print the rules
def show_rules() -> None:
    os.system(CLS_COMMAND)
    print("""╔══════════════════════ RULES ═══════════════════════╗
║                                                    ║
║               █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█                 ║
║              █░▒▒▒▒▒▒▒▓▒▒▓▒▒▒▒▒▒▒░█                ║
║              █░▒▒▓▒▒▒▒▒▒▒▒▒▄▄▒▓▒▒░█░▄▄             ║
║         ▄▀▀▄▄█░▒▒▒▒▒▒▓▒▒▒▒█░░▀▄▄▄▄▄▀░░█            ║
║         █░░░░█░▒▒▒▒▒▒▒▒▒▒▒█░░░░░░░░░░░█            ║
║          ▀▀▄▄█░▒▒▒▒▓▒▒▒▓▒█░░░█▒░░░░█▒░░█           ║
║              █░▒▓▒▒▒▒▓▒▒▒█░░░░░░░▀░░░░░█           ║
║            ▄▄█░▒▒▒▓▒▒▒▒▒▒▒█░░█▄▄█▄▄█░░█            ║
║           █░░░█▄▄▄▄▄▄▄▄▄▄█░█▄▄▄▄▄▄▄▄▄█             ║
║           █▄▄█  █▄▄█      █▄▄█  █▄▄█               ║
║                      nyan                          ║
║                                                    ║
║ >>> Hello human ! Welcome to Tepris...             ║
║ >>> There are the instructions you may need        ║
║     in your epic journey                           ║
║                                                    ║
║     (press Enter to continue)                      ║
║                                                    ║
╚════════════════════════════════════════════════════╝
    """)
    input()
    os.system(CLS_COMMAND)
    print("""╔═════════════════ GETTING STARTED ══════════════════╗
║                                                    ║
║ >>> NEW GAME :                                     ║
║     To start a new game, enter 1 on your keyboard  ║
║                                                    ║
║ >>> SELECTING A BOARD :                            ║
║     To do so, enter the number corresponding to    ║
║     the shape your want to play on                 ║
║                                                    ║
║ >>> USING CUSTOM SHAPES :                          ║
║     To play on a custom shape, enter 4 on your     ║
║     keyboard. Then create a txt file with 1 as     ║
║     dots and 0 as empty space. Finally, enter the  ║
║     name of the file to import.                    ║
║                                                    ║
║     (press Enter to continue)                      ║
║                                                    ║
╚════════════════════════════════════════════════════╝
    """)
    input()
    os.system(CLS_COMMAND)
    print("""╔════════════════════ INTERFACE ═════════════════════╗
║                                                    ║
║ >>> BOARD :                                        ║
║     On the center of your screen is the board you  ║
║     will play on.                                  ║
║     It is made of columns and rows determined by   ║
║     lower case and upper case letters.             ║
║                                                    ║
║ >>> SCORE :                                        ║
║     At the top of the board is shown your current  ║
║     score. Further information in : GOAL           ║
║                                                    ║
║ >>> BLOCKS :                                       ║
║     Under the board are displayed the 3 blocks you ║
║     can select for your next move.                 ║
║     Further information in :                       ║
║     HOW TO PLAY > BLOCK SELECTION                  ║
║                                                    ║
║     (press Enter to continue)                      ║
║                                                    ║
╚════════════════════════════════════════════════════╝
    """)
    input()
    os.system(CLS_COMMAND)
    print("""╔══════════════════ HOW TO PLAY 1 ═══════════════════╗
║                                                    ║
║ >>> BLOCK SELECTION :                              ║
║     To select a block, type the number shown under ║
║     it, then press enter.                          ║
║                                                    ║
║ >>> PLACING BLOCKS :                               ║
║                                                    ║
║     1> Because blocks take more space than just    ║
║        one dot, they have a predefined origin      ║
║        point. This point is positionned at the     ║
║        bottom left of the blocks structure.        ║
║                                                    ║
║        e.g.                                        ║
║                                                    ║
║   ╔════════════════════════════════════════════╗   ║
║   ║                                            ║   ║
║   ║    · · · · ·     · · · · ·     · · · ■ ■   ║   ║
║   ║    · · · · ·     ■ ■ ■ ■ ·     · · ■ ■ ·   ║   ║
║   ║    · · · · ·     · · · ■ ·     · ■ ■ · ·   ║   ║
║   ║    · ■ ■ · ·     · · · ■ ·     ■ ■ · · ·   ║   ║
║   ║    ● ■ · · ·     ○ · · ■ ·     ● · · · ·   ║   ║
║   ║                                            ║   ║
║   ╚════════════════════════════════════════════╝   ║
║       ○ : empty origin                             ║
║       ● : full origin                              ║
║                                                    ║
║     (press Enter to continue)                      ║
║                                                    ║
╚════════════════════════════════════════════════════╝
""")
    input()
    os.system(CLS_COMMAND)
    print("""╔══════════════════ HOW TO PLAY 2 ═══════════════════╗
║                                                    ║
║     2> To place a block, enter the coordinates at  ║
║        witch you want to place it relative to the  ║
║        origin point :                              ║
║                                                    ║
║        1> Enter the letter of the corresponding    ║
║           column.                                  ║
║        2> Enter the letter of the desired row      ║
║        3> Both letters should be written on the    ║
║           same line, no space is needed.           ║
║           (e.g. : Am ; oG ; us)                    ║
║                                                    ║
║ >>> PAUSE MENU :                                   ║
║     To access the pause menu while in a game,      ║
║     enter "-1" in the blok selection. There, you   ║
║     can save and quit your game.                   ║
║                                                    ║
║     (press Enter to continue)                      ║
║                                                    ║
╚════════════════════════════════════════════════════╝
""")
    input()
    os.system(CLS_COMMAND)
    print("""╔═══════════════════════ GOAL ═══════════════════════╗
║                                                    ║
║ >>> Your objective is to get the highest score     ║
║     possible before you cant place any more blocks.║
║                                                    ║
║ >>> POINT SYSTEM :                                 ║
║     Every time you fill a row or a column with     ║
║     squares, it clears and gives you points :      ║
║                                                    ║
║     1> You get 1 point at every turn.              ║
║     2> Each cleared square gives you 1 point       ║
║                                                    ║
║     (press Enter to continue)                      ║
║                                                    ║
╚════════════════════════════════════════════════════╝  
""")
    input()
    
# Game functions

# Print the pause menu
# Return an integer corresponsding to what to do next
def pause_menu() -> int:
    os.system(CLS_COMMAND)
    print("""╔════════════════════════════════════════════════════╗
║                        PAUSE                       ║
╚════════════════════════════════════════════════════╝

    [1] Continue
    [2] Save
    [3] Quit
""")
    c = 0
    while c not in (1, 2, 3):
        c = better_int_input("    [?] ")

    return c

# Play the game
def game(board, bloc_list, pol) -> None:
    nb_col = len(board[0])
    nb_row = len(board)
    
    # Main Game Loop
    blocs = select_bloc(bloc_list, pol)
    score = 0

    attempts = 0
    while True:
        os.system(CLS_COMMAND)
        # Print elements to the screen
        print_score(score)
        print_grid(board)
        print_blocs(blocs, pol)

        c = -2
        blocs_available = list(range(1, len(blocs)+1))
        while (c not in blocs_available) and (c != -1):
            c = better_int_input("    [B] ")

        if c == -1:
            os.system(CLS_COMMAND)
            q = pause_menu()
            if q == 1:
                continue
            elif q == 2:
                save_grid("save.txt", board)
                break
            elif q == 3:
                end_screen(score)
                break
        
        c -= 1
        b = block_list[blocs[c]]

        correct_coord = False
        while not correct_coord:
            coord = ""
            while len(coord) <= 1:
                coord = input("    [Coord] ")

            coord = [coord[0], coord[-1]]
            try:
                coord = [e.lower() for e in coord]
            except:
                continue

            coord = [ord(e)-97 for e in coord]
            if not(coord[0] < 0 or coord[0] > nb_col or coord[1] < 0 or coord[1] > nb_row):
                correct_coord = True

        x, y = coord

        if attempts >= 3:
            end_screen(score)
            break
        if not valid_position(board, b, x, y):
            attempts += 1
            continue

        place_bloc(board, b, x, y)
        blocs = select_bloc(bloc_list, pol)
        attempts = 0
        score += 1

        points = -1
        while points != 0:
            board, points = clear_rows_and_col(board)
            score += points

# Print the score at the end of a game
def end_screen(score) -> None:
    os.system(CLS_COMMAND)
    print(f"""╔════════════════════════════════════════════════════╗
║                     GAME OVER                      ║
╚════════════════════════════════════════════════════╝

You finished with a score of {score} !
    """)
    input()

# General Utility functions

def better_int_input(prompt) -> int:
    p = input(prompt)

    try:
        p = int(p)
    except:
        p = 0

    return p
