###########################################
#                                         #
#   Python Project : A Tetris-Like Game   #
#   MEUNIER Antoine, BUDAR Maxime         #
#   EFREI, 2022                           #
#                                         #
###########################################

# This file serves as the starting point of the game.

from board import *

import os 
if os.name == "nt": CLS_COMMAND = "cls"
if os.name == "posix": CLS_COMMAND = "clear"

def main():

    while True:
        choice = 0
        path = ""
        pol = 2
        
        # Main Menu loop
        game_started = False
        while not game_started:
            choice = show_menu()

            if choice == 1: # Start Game
                path = select_board()
                if path == "":
                    continue
                os.system(CLS_COMMAND)
                pol = select_policy()
                if pol == 3:
                    continue

                game_started = True

            elif choice == 2: # Resume Game
                path = "save.txt"
                game_started = True

            elif choice == 3: # Show Rules
                show_rules()

            elif choice == 4: # Quit
                print("Thank you for playing !")
                return 0
            
            os.system(CLS_COMMAND)

        # Setup the game
        board = read_grid(path)
        current_block_list = get_block_list(path)

        if board == []: # Quit the game if the board doesn't exist
            return 1
        
        # Start of the game
        game(board, current_block_list, pol)    

if __name__=="__main__":
    main()
