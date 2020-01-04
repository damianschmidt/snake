from pygame import Rect, draw
from math import ceil
from random import randint, choice


class Food:
    def __init__(self, config):
        self.config = config
        self.x = int(
            ceil((randint(0, config.SCREEN_WIDTH - config.RECT_DIM))) / float(config.RECT_DIM)) * config.RECT_DIM
        self.y = int(
            ceil((randint(0, config.SCREEN_HEIGHT - config.RECT_DIM))) / float(config.RECT_DIM)) * config.RECT_DIM
        self.food_rect = Rect(self.x, self.y, config.RECT_DIM, config.RECT_DIM)

    def reset(self, tab):
        y_dim, x_dim = tab.state.shape

        empty_fields = []
        for x in range(x_dim - 2):
            for y in range(y_dim - 2):
                if tab.state[y + 1, x + 1] == 0:
                    empty_fields.append((x, y))

        # choose one
        if empty_fields:
            food_field = choice(empty_fields)

            # find x and y of field
            self.x = food_field[0] * self.config.RECT_DIM
            self.y = food_field[1] * self.config.RECT_DIM
            self.food_rect = Rect(self.x + 1, self.y + 1, self.config.RECT_DIM - 2, self.config.RECT_DIM - 2)

    def render(self, game_screen):
        draw.rect(game_screen, self.config.FOOD_COLOR, self.food_rect)
