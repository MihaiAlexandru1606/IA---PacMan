from src.play import Game
from src.strategy import random_strategy, min_max_iterative_deepening, monte_carlo_tree_search_normal, \
    monte_carlo_tree_search_bonus
import sys

if __name__ == '__main__':

    game = Game(min_max_iterative_deepening, monte_carlo_tree_search_normal, sys.argv[1])
    game.run()

