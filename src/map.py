import sys
from src.ghost import Ghost
from src.pacman import PacMan
from copy import deepcopy
from src.utility import distant_euclid, distant_manhattan

STATE_WIN = 'win'
STATE_LOSE_GAME = 'lose-game'
STATE_LOSE_TURN = 'lose-turn'
STATE_PLAY = 'play'


class Map(object):

    def __init__(self, file_config=None):
        if file_config is not None:
            with open(file_config, 'r') as read_file:
                height, width, max_buget, max_depth = read_file.readline().strip().split()
                pac_man_x, pac_man_y = read_file.readline().strip().split()
                ghost_1_x, ghost_1_y = read_file.readline().strip().split()
                ghost_2_x, ghost_2_y = read_file.readline().strip().split()

                map_conf = []
                food_number = 0
                for line in read_file.readlines():
                    row_map = line.strip().split()
                    map_conf.append(row_map)
                    for c in row_map:
                        if c == '_':
                            food_number += 1

                map_conf[int(pac_man_x)][int(pac_man_y)] = '-'
                self.height = int(height)
                self.width = int(width)
                self.pac_man = PacMan(int(pac_man_x), int(pac_man_y))
                self.ghost1 = Ghost(int(ghost_1_x), int(ghost_1_y))
                self.ghost2 = Ghost(int(ghost_2_x), int(ghost_2_y))
                self.map_conf = map_conf
                self.food_number = food_number - 1
                self.max_win = food_number - 1
                self.state = STATE_PLAY
                self.factor = self.food_number / (self.width + self.height)
                self.max_buget = int(max_buget)
                self.max_depth = int(max_depth)

    def get_pac_man(self):
        return self.pac_man

    def get_ghost1(self):
        return self.ghost1

    def get_ghost2(self):
        return self.ghost2

    def win(self) -> bool:
        return self.state == STATE_WIN

    def lose_turn(self) -> bool:
        return self.state == STATE_LOSE_TURN

    def lose_game(self) -> bool:
        return self.state == STATE_LOSE_GAME

    def run_turn(self, move_pac_man, move_ghost_1, move_ghost_2):
        self.pac_man.update_position(move_pac_man, self.height, self.width)
        self.ghost1.update_position(move_ghost_1, self.height, self.width)
        self.ghost2.update_position(move_ghost_2, self.height, self.width)

        if self.map_conf[self.pac_man.position_x][self.pac_man.position_y] == '_':
            self.food_number -= 1
            self.pac_man.score += 1
            self.map_conf[self.pac_man.position_x][self.pac_man.position_y] = '-'

        if self.food_number == 0:
            self.state = STATE_WIN
            return

        # daca este lose turn si daca este lose general
        if self.pac_man.position_x == self.ghost1.position_x and self.pac_man.position_y == self.ghost1.position_y:
            self.pac_man.life -= 1
            if self.pac_man.life == 0:
                self.state = STATE_LOSE_GAME
            else:
                self.state = STATE_LOSE_TURN
            return

        if self.pac_man.position_x == self.ghost2.position_x and self.pac_man.position_y == self.ghost2.position_y:
            self.pac_man.life -= 1
            if self.pac_man.life == 0:
                self.state = STATE_LOSE_GAME
            else:
                self.state = STATE_LOSE_TURN
            return

    def check_move(self, position_x, position_y, delta) -> bool:
        new_pos_x = position_x + delta[0]
        new_pos_y = position_y + delta[1]


        if new_pos_x < 0:
            new_pos_x = self.height - 1
        elif new_pos_x == self.height:
            new_pos_x = 0

        if new_pos_y < 0:
            new_pos_y = self.width - 1
        elif new_pos_y == self.width:
            new_pos_y = 0

        if self.map_conf[new_pos_x][new_pos_y] == 'X':
            return False

        return True

    def reset_position(self):
        self.pac_man.reset_original()
        self.ghost1.reset_original()
        self.ghost2.reset_original()
        self.state = STATE_PLAY

    def generate_successors_pac_man(self):

        delta = [ (1, 0), (-1, 0), (0, 1), (0, -1)]
        successors = []

        for move_player in delta:
            if self.check_move(self.pac_man.position_x, self.pac_man.position_y, move_player):
                copy_map = deepcopy(self)
                copy_map.run_turn(move_player, (0, 0), (0, 0))
                successors.append((copy_map, move_player))

        return successors

    def generate_successors_ghosts(self):

        delta = [ (1, 0), (-1, 0), (0, 1), (0, -1)]
        successors = []

        for move_ghost1 in delta:
            if self.check_move(self.ghost1.position_x, self.ghost1.position_y, move_ghost1):
                for move_ghost2 in delta:
                    if self.check_move(self.ghost2.position_x, self.ghost2.position_y, move_ghost2):
                        copy_map = deepcopy(self)
                        copy_map.run_turn((0, 0), move_ghost1, move_ghost2)
                        successors.append((copy_map, (move_ghost1, move_ghost2)))

        return successors

    def generate_successors(self, player_type):
        if player_type == 0:
            return self.generate_successors_pac_man()
        elif player_type == 1:
            return self.generate_successors_ghosts()

    def evaluate_state(self):
        if self.state == STATE_WIN:
            return 5 * self.max_win + 2 * (self.height + self.width)
        elif self.state == STATE_LOSE_TURN or self.state == STATE_LOSE_GAME:
            # return -(5 * self.max_win + self.height + self.width)
            return 0

        return 5 * self.pac_man.score + \
               distant_manhattan(self.pac_man.position_x, self.pac_man.position_y, self.ghost1.position_x,
                                 self.ghost1.position_y) + \
               distant_manhattan(self.pac_man.position_x, self.pac_man.position_y, self.ghost1.position_x,
                                 self.ghost1.position_y)

    def complement_score(self, score):
        return 5 * self.max_win + 2 * (self.height + self.width) - score

    def get_available_actions(self, player_type):

        delta = delta = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]

        if player_type == 0:
            return list(filter(lambda x: self.check_move(self.pac_man.position_x, self.pac_man.position_y, x), delta))
        elif player_type == 1:
            valid_moves = []

            for move_ghost1 in delta:
                if self.check_move(self.ghost1.position_x, self.ghost1.position_y, move_ghost1):
                    for move_ghost2 in delta:
                        if self.check_move(self.ghost2.position_x, self.ghost2.position_y, move_ghost2):
                            valid_moves.append((move_ghost1, move_ghost2))

            return valid_moves

    def __str__(self):
        representation = ''
        for i in range(self.height):
            for j in range(self.width):
                representation += ' '

                if i == self.ghost1.position_x and j == self.ghost1.position_y:
                    representation += 'G'
                elif i == self.ghost2.position_x and j == self.ghost2.position_y:
                    representation += 'G'
                elif i == self.pac_man.position_x and j == self.pac_man.position_y:
                    representation += 'P'
                else:
                    representation += self.map_conf[i][j]

            representation += '\n'

        return representation
