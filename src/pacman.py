class PacMan(object):

    def __init__(self, position_x, position_y):
        self.original_position_x = position_x
        self.original_position_y = position_y
        self.position_x = position_x
        self.position_y = position_y
        self.life = 3
        self.score = 0

    # se bazea pe faptul ca exista o corespondenta
    def update_position(self, delta, height, width):
        self.position_x += delta[0]
        self.position_y += delta[1]

        if self.position_x < 0:
            self.position_x = height - 1
        elif self.position_x == height:
            self.position_x = 0

        if self.position_y < 0:
            self.position_y = width - 1
        elif self.position_y == width:
            self.position_y = 0

    def reset_original(self):
        self.position_x = self.original_position_x
        self.position_y = self.original_position_y
