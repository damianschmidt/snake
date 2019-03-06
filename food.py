import config
from pygame import Rect, draw
from math import ceil
from random import randint
import game


class Food(object):
    def __init__(self):
        self.x = int(ceil((randint(0, config.SCREEN_WIDTH - config.RECT_DIM))) / float(config.RECT_DIM)) * config.RECT_DIM
        self.y = int(ceil((randint(0, config.SCREEN_HEIGHT - config.RECT_DIM))) / float(config.RECT_DIM)) * config.RECT_DIM
        self.food_rect = Rect(self.x, self.y, config.RECT_DIM, config.RECT_DIM)

    def reset(self, snake):
        self.x = int(ceil((randint(0, config.SCREEN_WIDTH - config.RECT_DIM))) / float(config.RECT_DIM)) * config.RECT_DIM
        self.y = int(ceil((randint(0, config.SCREEN_HEIGHT - config.RECT_DIM))) / float(config.RECT_DIM)) * config.RECT_DIM

        for body_part in snake.body_list:
            if self.x == body_part.x and self.y == body_part.y:
                self.reset(snake)

        self.food_rect = Rect(self.x, self.y, config.RECT_DIM, config.RECT_DIM)

    def render(self):
        draw.rect(game.game_screen, config.FOOD_COLOR, self.food_rect)
