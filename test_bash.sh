#!/usr/bin/env bash

python3 src/test.py random_strategy random_strategy harta3-9.txt >> /dev/null &
python3 src/test.py random_strategy min_max_iterative_deepening harta3-9.txt >> /dev/null &
python3 src/test.py random_strategy monte_carlo_tree_search_normal harta3-9.txt >> /dev/null &
python3 src/test.py random_strategy monte_carlo_tree_search_bonus harta3-9.txt >> /dev/null &


python3 src/test.py random_strategy random_strategy harta3-30.txt >> /dev/null &
python3 src/test.py random_strategy min_max_iterative_deepening harta3-30.txt >> /dev/null &
python3 src/test.py random_strategy monte_carlo_tree_search_normal harta3-30.txt >> /dev/null &
python3 src/test.py random_strategy monte_carlo_tree_search_bonus harta3-30.txt >> /dev/null &


python3 src/test.py random_strategy random_strategy harta3-100.txt >> /dev/null &
python3 src/test.py random_strategy min_max_iterative_deepening harta3-100.txt >> /dev/null &
python3 src/test.py random_strategy monte_carlo_tree_search_normal harta3-100.txt >> /dev/null &
python3 src/test.py random_strategy monte_carlo_tree_search_bonus harta3-100.txt >> /dev/null &


#Test
python3 src/test.py min_max_iterative_deepening random_strategy harta3-9.txt >> /dev/null &
python3 src/test.py min_max_iterative_deepening min_max_iterative_deepening harta3-9.txt >> /dev/null &
python3 src/test.py min_max_iterative_deepening monte_carlo_tree_search_normal harta3-9.txt >> /dev/null &
python3 src/test.py min_max_iterative_deepening monte_carlo_tree_search_bonus harta3-9.txt >> /dev/null &


python3 src/test.py min_max_iterative_deepening random_strategy harta3-30.txt >> /dev/null &
python3 src/test.py min_max_iterative_deepening min_max_iterative_deepening harta3-30.txt >> /dev/null &
python3 src/test.py min_max_iterative_deepening monte_carlo_tree_search_normal harta3-30.txt >> /dev/null &
python3 src/test.py min_max_iterative_deepening monte_carlo_tree_search_bonus harta3-30.txt >> /dev/null &


python3 src/test.py min_max_iterative_deepening random_strategy harta3-100.txt >> /dev/null &
python3 src/test.py min_max_iterative_deepening min_max_iterative_deepening harta3-100.txt >> /dev/null &
python3 src/test.py min_max_iterative_deepening monte_carlo_tree_search_normal harta3-100.txt >> /dev/null &
python3 src/test.py min_max_iterative_deepening monte_carlo_tree_search_bonus harta3-100.txt >> /dev/null &


#Test
python3 src/test.py monte_carlo_tree_search_normal random_strategy harta3-9.txt >> /dev/null &
python3 src/test.py monte_carlo_tree_search_normal min_max_iterative_deepening harta3-9.txt >> /dev/null &
python3 src/test.py monte_carlo_tree_search_normal monte_carlo_tree_search_normal harta3-9.txt >> /dev/null &
python3 src/test.py monte_carlo_tree_search_normal monte_carlo_tree_search_bonus harta3-9.txt >> /dev/null &


python3 src/test.py monte_carlo_tree_search_normal random_strategy harta3-30.txt >> /dev/null &
python3 src/test.py monte_carlo_tree_search_normal min_max_iterative_deepening harta3-30.txt >> /dev/null &
python3 src/test.py monte_carlo_tree_search_normal monte_carlo_tree_search_normal harta3-30.txt >> /dev/null &
python3 src/test.py monte_carlo_tree_search_normal monte_carlo_tree_search_bonus harta3-30.txt >> /dev/null &


python3 src/test.py monte_carlo_tree_search_normal random_strategy harta3-100.txt >> /dev/null &
python3 src/test.py monte_carlo_tree_search_normal min_max_iterative_deepening harta3-100.txt >> /dev/null &
python3 src/test.py monte_carlo_tree_search_normal monte_carlo_tree_search_normal harta3-100.txt >> /dev/null &
python3 src/test.py monte_carlo_tree_search_normal monte_carlo_tree_search_bonus harta3-100.txt >> /dev/null &