######################################
# MAIN CREATURES OF HABBIT GAME FILE #
# Links to MainGame in screens to    #
# launch.                            #
######################################

from screens import *

def run_game():
    game = MainGame()
    game.controller()

if __name__ == "__main__":
    run_game()