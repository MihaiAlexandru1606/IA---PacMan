from src.play import *
from src.strategy import random_strategy, min_max_iterative_deepening, monte_carlo_tree_search_normal, \
    monte_carlo_tree_search_bonus
import sys

if __name__ == '__main__':
    count_win = 0
    count_lose = 0
    strategy = []

    algo1 = None
    if sys.argv[1] == "random_strategy":
        algo1 = random_strategy
    elif sys.argv[1] == "min_max_iterative_deepening":
        algo1 = min_max_iterative_deepening
    elif sys.argv[1] == 'monte_carlo_tree_search_normal':
        algo1 = monte_carlo_tree_search_normal
    elif sys.argv[1] == 'monte_carlo_tree_search_bonus':
        algo1 = monte_carlo_tree_search_bonus

    algo2 = None
    if sys.argv[2] == "random_strategy":
        algo2 = random_strategy
    elif sys.argv[2] == "min_max_iterative_deepening":
        algo2 = min_max_iterative_deepening
    elif sys.argv[2] == 'monte_carlo_tree_search_normal':
        algo2 = monte_carlo_tree_search_normal
    elif sys.argv[2] == 'monte_carlo_tree_search_bonus':
        algo2 = monte_carlo_tree_search_bonus

    for i in range(15):
        game = Game(algo1, algo2, sys.argv[3])
        game.run()

        if game.map_game.win():
            count_win += 1
        else:
            count_lose += 1

    file_output = algo1.__name__ + "_" + algo2.__name__ + "_" + sys.argv[3]
    with open(file_output, 'a') as wFile:
        wFile.writelines("Win " + str(count_win) + '\n')
        wFile.writelines("Lose " + str(count_lose) + '\n')
