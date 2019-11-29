from pygame import Rect, draw
from math import ceil
from random import randint


class Food:
    def __init__(self, config):
        self.config = config
        self.x = int(
            ceil((randint(0, config.SCREEN_WIDTH - config.RECT_DIM))) / float(config.RECT_DIM)) * config.RECT_DIM
        self.y = int(
            ceil((randint(0, config.SCREEN_HEIGHT - config.RECT_DIM))) / float(config.RECT_DIM)) * config.RECT_DIM
        self.food_rect = Rect(self.x, self.y, config.RECT_DIM, config.RECT_DIM)

    def reset(self, snake):
        self.x = int(ceil((randint(0, self.config.SCREEN_WIDTH - self.config.RECT_DIM))) / float(
            self.config.RECT_DIM)) * self.config.RECT_DIM
        self.y = int(ceil((randint(0, self.config.SCREEN_HEIGHT - self.config.RECT_DIM))) / float(
            self.config.RECT_DIM)) * self.config.RECT_DIM

        for body_part in snake.body_list:
            if self.x == body_part.x and self.y == body_part.y:
                self.reset(snake)

        self.food_rect = Rect(self.x, self.y, self.config.RECT_DIM, self.config.RECT_DIM)

    def render(self, game_screen):
        draw.rect(game_screen, self.config.FOOD_COLOR, self.food_rect)
