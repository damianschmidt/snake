import pygame
import math
from random import randint

RECT_COLOR = (0, 220, 0)
BG_COLOR = (50, 50, 50)
RECT_DIM = 10
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SNAKE_INIT_LENGTH = 5
SNAKE_INIT_X = (SNAKE_INIT_LENGTH + 1) * RECT_DIM
SNAKE_INIT_Y = 300

pygame.init()
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()


class Snake(object):
    def __init__(self, x, y):
        self.body_list = list()
        self.score = 0
        self.direct = pygame.K_RIGHT

        for i in range(SNAKE_INIT_LENGTH, 0, -1):
            self.body_list.append(Body(x - i * RECT_DIM, y))

        self.directions = {
            pygame.K_UP: self.move_up,
            pygame.K_DOWN: self.move_down,
            pygame.K_LEFT: self.move_left,
            pygame.K_RIGHT: self.move_right
        }

    @property
    def head(self):
        return self.body_list[-1]

    def move_up(self):
        self.head.y -= RECT_DIM
        if self.head.y < 0:
            print('Out of area!')

    def move_down(self):
        self.head.y += RECT_DIM
        if self.head.y > SCREEN_HEIGHT:
            print('Out of area!')

    def move_left(self):
        self.head.x -= RECT_DIM
        if self.head.x < SCREEN_WIDTH:
            print('Out of area!')

    def move_right(self):
        self.head.x += RECT_DIM
        if self.head.x > SCREEN_WIDTH:
            print('Out of area!')

    def update_snake(self):
        self.body_list.pop(0)
        new_part = Body(self.body_list[-1].x, self.body_list[-1].y)
        self.body_list.insert(-1, new_part)

        self.directions[self.direct]()

    def render(self):
        for body_part in self.body_list:
            body_rect = pygame.Rect(body_part.x, body_part.y, RECT_DIM, RECT_DIM)
            pygame.draw.rect(game_screen, RECT_COLOR, body_rect)


class Body(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Food(object):
    def __init__(self):
        self.x = int(math.ceil((randint(0, SCREEN_WIDTH - RECT_DIM))) / 10.0) * 10
        self.y = int(math.ceil((randint(0, SCREEN_HEIGHT - RECT_DIM))) / 10.0) * 10
        self.food_rect = pygame.Rect(self.x, self.y, RECT_DIM, RECT_DIM)

    def render(self):
        pygame.draw.rect(game_screen, RECT_COLOR, self.food_rect)


def game_loop():
    snake = Snake(SNAKE_INIT_X, SNAKE_INIT_Y)
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game_screen.fill(BG_COLOR)
        food.render()
        snake.render()
        snake.update_snake()
        pygame.display.update()
        clock.tick(15)


if __name__ == '__main__':
    game_loop()
