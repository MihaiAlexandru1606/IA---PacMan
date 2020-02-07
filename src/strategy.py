import random
import sys
from src.map import Map
from math import sqrt, log
from copy import deepcopy
from functools import reduce
import operator
from src.utility import MemoryMCTS

PAC_MAM = 0
GHOSTS = 1


def random_strategy(map_game: Map, player_type: int):
    delta = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]

    if player_type == PAC_MAM:
        player = map_game.get_pac_man()
        return random.choice(
            list(filter(lambda x: map_game.check_move(player.position_x, player.position_y, x), delta)))
    elif player_type == GHOSTS:
        player = map_game.get_ghost1()

        valid_move = []
        for d1 in delta:
            if map_game.check_move(map_game.get_ghost1().position_x, map_game.get_ghost1().position_y, d1):
                for d2 in delta:
                    if map_game.check_move(map_game.get_ghost2().position_x, map_game.get_ghost2().position_y, d2):
                        valid_move.append((d1, d2))

        return random.choice(valid_move)


def min_max_alpha_beta(map_game: Map, depth, alpha, beta, player, buget: list):
    if depth == 0 or map_game.win() or map_game.lose_game() or map_game.lose_turn():
        return map_game.evaluate_state()

    # pentru maxim
    if player == 0:
        max_current = -sys.maxsize

        for new_map, move_pac_man in map_game.generate_successors_pac_man():
            buget[0] += 1
            MemoryMCTS.current_buget += 1
            ret_val = min_max_alpha_beta(new_map, depth - 1, alpha, beta, 1 - player, buget)
            max_current = max(ret_val, max_current)
            alpha = max(max_current, alpha)
            if beta <= alpha:
                break

        return max_current
    else:
        min_current = sys.maxsize

        for new_map, move_ghosts in map_game.generate_successors_ghosts():
            buget[0] += 1
            MemoryMCTS.current_buget += 1
            ret_val = min_max_alpha_beta(new_map, depth - 1, alpha, beta, 1 - player, buget)

            min_current = min(min_current, ret_val)
            beta = min(beta, min_current)
            if beta <= alpha:
                break

        return min_current


def min_max_iterative_deepening(map_game: Map, player_type: int):
    buget = [-20 * map_game.max_buget]
    score_current = None
    current_move = (0, 0)

    if player_type == 0:
        score_current = -sys.maxsize
    elif player_type == 1:
        score_current = sys.maxsize

    for depth in range(map_game.max_depth):
        if buget[0] >= map_game.max_buget:
            break

        for new_map, move_player in map_game.generate_successors(player_type):
            if buget[0] >= map_game.max_buget:
                break

            ret_val = min_max_alpha_beta(new_map, depth, -sys.maxsize, sys.maxsize, player_type, buget)
            if player_type == 0:
                if ret_val > score_current:
                    current_move = move_player
                    score_current = ret_val
            elif player_type == 1:
                if ret_val < score_current:
                    current_move = move_player
                    score_current = ret_val

    return current_move


########################################################################################################################
#                                       Monte Carlo Tree Search
########################################################################################################################

# Constante
N = 'N'
Q = 'Q'
PARENT = 'parent'
ACTIONS = 'actions'
CURRENT_PLAYER = 'current-player'
CURRENT_STATE = 'current-state'
INVALID_ACTION = -1
CP = 1.0 / sqrt(2.0)


def select_action(node, c=CP):
    # Se caută acțiunea a care maximizează expresia:
    # Q_a / N_a  +  c * sqrt(2 * log(N_node) / N_a)

    if node[ACTIONS]:
        return max(list(map(
            lambda x: (x, node[ACTIONS][x][Q] / node[ACTIONS][x][N] + c * sqrt(2 * log(node[N]) / node[ACTIONS][x][N])),
            node[ACTIONS])), key=operator.itemgetter(1))[0]
    else:
        return INVALID_ACTION


def create_root_monte_carlo_tree_search(map_gamne: Map, player: int):
    return {N: 0, Q: 0, PARENT: None, ACTIONS: {}, CURRENT_PLAYER: player, CURRENT_STATE: map_gamne}


def create_node_monte_carlo_tree_search(map_gamne: Map, parent: Map, player: int):
    return {N: 0, Q: 0, PARENT: parent, ACTIONS: {}, CURRENT_PLAYER: player, CURRENT_STATE: map_gamne}


def apply_action(state: Map, action, player_type: int):
    copy_state = deepcopy(state)
    if player_type == PAC_MAM:
        copy_state.run_turn(action, (0, 0), (0, 0))
    elif player_type == GHOSTS:
        copy_state.run_turn((0, 0), action[0], action[1])

    return copy_state


def rollout(state: Map, strategy):
    move_pac_man = strategy(state, PAC_MAM)
    move_ghost1, move_ghost2 = strategy(state, GHOSTS)

    state.run_turn(move_pac_man, move_ghost1, move_ghost2)
    return state


def monte_carlo_tree_search(map_game: Map, player_type: int, strategy, state0: Map, budget, tree,
                            opponent_s_action=None):
    # DACĂ există un arbore construit anterior ȘI
    #   acesta are un copil ce corespunde ultimei acțiuni a adversarului,
    # ATUNCI acel copil va deveni nodul de început pentru algoritm.
    # ALTFEL, arborele de start este un nod gol.

    if tree is not None and opponent_s_action in tree[ACTIONS]:
        tree = tree[ACTIONS][opponent_s_action]
    else:
        tree = create_root_monte_carlo_tree_search(map_game, player_type)

    # ---------------------------------------------------------------

    for x in range(budget):
        # Punctul de start al simulării va fi rădăcina de start
        state = state0
        node = tree

        # Coborâm în arbore până când ajungem la o stare finală
        # sau la un nod cu acțiuni neexplorate.
        # Variabilele state și node se 'mută' împreună.
        while not (state.win() or state.lose_turn() or state.lose_game()) and node[ACTIONS] and \
                all(elem in node[ACTIONS] for elem in state.get_available_actions(player_type=player_type)):
            action_now = select_action(node)
            node = node[ACTIONS][action_now]
            state = apply_action(state, action_now, player_type)

        # Dacă am ajuns într-un nod care nu este final și din care nu s-au
        # `încercat` toate acțiunile, construim un nod nou., se alege random
        if not (state.win() or state.lose_turn() or state.lose_game()):
            all_actions = state.get_available_actions(player_type)
            unused_action = list(set(all_actions) - set(node[ACTIONS].keys()))

            if unused_action:
                action_now = random.choice(unused_action)
                new_node = create_node_monte_carlo_tree_search(map_game, node, player_type)

                node[ACTIONS][action_now] = new_node
                node = new_node
                state = apply_action(state, action_now, player_type)

        # Se simulează o desfășurare a jocului până la ajungerea într-o
        # starea finală. Se evaluează recompensa în acea stare.
        MemoryMCTS.current_buget = 0
        while not (state.win() or state.lose_turn() or state.lose_game()) and state.max_buget >= MemoryMCTS.current_buget:
            state = rollout(state, strategy)

        reward = state.evaluate_state()
        if player_type == GHOSTS:
            reward = state.complement_score(reward)

        # Se actualizează toate nodurile de la node către rădăcină:
        #  - se incrementează valoarea N din fiecare nod
        #  - se adaugă recompensa la valoarea Q
        while node:
            node[N] += 1
            node[Q] += reward
            node = node[PARENT]

    if tree:
        final_action = select_action(tree, 0.0)
        return final_action, tree[ACTIONS][final_action]


def monte_carlo_tree_search_api(map_game: Map, player_type: int, strategy):
    tree = None
    opponent_action = None

    if player_type == 0:
        tree = MemoryMCTS.memory_pac_man
        opponent_action = MemoryMCTS.last_action_ghosts
    elif player_type == 1:
        tree = MemoryMCTS.memory_ghosts
        opponent_action = MemoryMCTS.last_action_pac_man

    action, memory = monte_carlo_tree_search(map_game, player_type, strategy, map_game, map_game.max_buget, tree,
                                             opponent_action)

    return action


def monte_carlo_tree_search_normal(map_game: Map, player_type: int):
    return monte_carlo_tree_search_api(map_game, player_type, random_strategy)


def monte_carlo_tree_search_bonus(map_game: Map, player_type: int):
    return monte_carlo_tree_search_api(map_game, player_type, min_max_iterative_deepening)
