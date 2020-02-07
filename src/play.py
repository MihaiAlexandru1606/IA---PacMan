from src.map import *
from src.strategy import PAC_MAM, GHOSTS
from src.utility import MemoryMCTS


class Game(object):
    def __init__(self, strategy_pac_man, strategy_ghosts, init_config):
        self.map_game = Map(init_config)
        self.strategy_pac_man = strategy_pac_man
        self.strategy_ghosts = strategy_ghosts
        self.turn = 0

    def run(self):
        MemoryMCTS.reset()

        while True:

            if self.map_game.win():
                print("Win Game")
                return

            if self.map_game.lose_turn():
                self.map_game.reset_position()
                print("++++++++++++++++++++++ Lose Turn ++++++++++++++++++++++")
                MemoryMCTS.last_action_ghosts = None
                MemoryMCTS.memory_pac_man = None
                print(self.map_game)

            if self.map_game.lose_game():
                print("Lose Game")
                return

            move_pac_man = self.strategy_pac_man(self.map_game, PAC_MAM)
            move_ghost1, move_ghost2 = self.strategy_ghosts(self.map_game, GHOSTS)

            self.turn += 1
            print(move_pac_man)
            print(move_ghost1)
            print(move_ghost2)
            self.map_game.run_turn(move_pac_man, move_ghost1, move_ghost2)
            print('*****************************************************')
            print("\t\tIn Turn ", end='')
            print(self.turn)
            print("\t\tLife player : {}".format(self.map_game.get_pac_man().life))
            print("\t\tMap configuration:")
            print(self.map_game)
            print('*****************************************************')
            print("\n\n")
