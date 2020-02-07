from math import sqrt


def distant_euclid(pos_x_1, pos_y_1, pos_x_2, pos_y_2):
    return sqrt((pos_x_2 - pos_x_1) * (pos_x_2 - pos_x_1) + (pos_y_2 - pos_y_1) * (pos_y_2 - pos_y_1))


def distant_manhattan(pos_x_1, pos_y_1, pos_x_2, pos_y_2):
    return abs(pos_x_1 - pos_x_2) + abs(pos_y_1 - pos_y_2)


class MemoryMCTS(object):
    last_action_pac_man = None
    last_action_ghosts = None
    memory_pac_man = None
    memory_ghosts = None
    current_buget = 0

    @staticmethod
    def reset():
        MemoryMCTS.last_action_ghosts = None
        MemoryMCTS.last_action_pac_man = None
        MemoryMCTS.memory_pac_man = None
        MemoryMCTS.memory_ghosts = None
        MemoryMCTS.current_buget = 0