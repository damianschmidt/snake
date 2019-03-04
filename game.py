import pygame
from random import randint

pygame.init()

RECT_COLOR = (0, 220, 0)
BG_COLOR = (50, 50, 50)
RECT_DIM = 10
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()


class Snake(object):
    def __init__(self, x, y):
        self.body_list = list()
        self.score = 0


class Body(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Food(object):
    def __init__(self):
        # TODO: random number has to be % 10 == 0
        self.x = randint(RECT_DIM, SCREEN_WIDTH - 2 * RECT_DIM)
        self.y = randint(RECT_DIM, SCREEN_HEIGHT - 2 * RECT_DIM)
        self.food_rect = pygame.Rect(self.x, self.y, RECT_DIM, RECT_DIM)

    def render(self):
        pygame.draw.rect(game_screen, RECT_COLOR, self.food_rect)


def game_loop():
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game_screen.fill(BG_COLOR)
        food.render()
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    game_loop()
