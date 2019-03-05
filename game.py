import pygame
from math import ceil
from random import randint

FOOD_COLOR = (220, 0, 0)
SNAKE_COLOR = (0, 220, 0)
BG_COLOR = (50, 50, 50)
RECT_DIM = 30
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SNAKE_INIT_LENGTH = 5
SNAKE_INIT_X = (SNAKE_INIT_LENGTH + 1) * RECT_DIM
SNAKE_INIT_Y = 300

pygame.init()
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()


def add_text(text, font, size, color, width, height):
    font = pygame.font.SysFont(font, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (width, height)
    game_screen.blit(text_surface, text_rect)


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

    def game_over(self):
        add_text('GAME OVER', 'Arial', 72, (255, 255, 255), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.2)
        add_text('YOUR SCORE: ' + str(self.score), 'Arial', 36, (255, 255, 255), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.8)

        x_button = 200
        y_button = 380
        width_button = 200
        height_button = 50
        button_color = (0, 0, 200)
        button_color_hover = (0, 0, 240)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if x_button + width_button > mouse[0] > x_button and y_button + height_button > mouse[1] > y_button:
                pygame.draw.rect(game_screen, button_color_hover, (x_button, y_button, width_button, height_button))
                if click[0] == 1:
                    game_loop()
            else:
                pygame.draw.rect(game_screen, button_color, (x_button, y_button, width_button, height_button))

            add_text('RESTART', 'Arial', 24, (255, 255, 255), x_button + (width_button / 2),
                     y_button + (height_button / 2))

            pygame.display.update()
            clock.tick(15)

    def move_up(self):
        self.head.y -= RECT_DIM
        if self.head.y < 0:
            self.game_over()

    def move_down(self):
        self.head.y += RECT_DIM
        if self.head.y > SCREEN_HEIGHT:
            self.game_over()

    def move_left(self):
        self.head.x -= RECT_DIM
        if self.head.x < 0:
            self.game_over()

    def move_right(self):
        self.head.x += RECT_DIM
        if self.head.x > SCREEN_WIDTH:
            self.game_over()

    def eat_food(self, food):
        food.reset(self)
        self.score += 1
        eat_part = self.head
        self.body_list.insert(0, eat_part)

    def collision(self, food):
        # with food
        if self.head.x == food.x and self.head.y == food.y:
            self.eat_food(food)

    def update_snake(self):
        self.body_list.pop(0)
        new_part = Body(self.body_list[-1].x, self.body_list[-1].y)
        self.body_list.insert(-1, new_part)
        self.directions[self.direct]()

    def change_direct(self, direct):
        if direct is not self.direct:
            self.direct = direct

    def render(self):
        for body_part in self.body_list:
            body_rect = pygame.Rect(body_part.x, body_part.y, RECT_DIM, RECT_DIM)
            pygame.draw.rect(game_screen, SNAKE_COLOR, body_rect)


class Body(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Food(object):
    def __init__(self):
        self.x = int(ceil((randint(0, SCREEN_WIDTH - RECT_DIM))) / float(RECT_DIM)) * RECT_DIM
        self.y = int(ceil((randint(0, SCREEN_HEIGHT - RECT_DIM))) / float(RECT_DIM)) * RECT_DIM
        self.food_rect = pygame.Rect(self.x, self.y, RECT_DIM, RECT_DIM)

    def reset(self, snake):
        self.x = int(ceil((randint(0, SCREEN_WIDTH - RECT_DIM))) / float(RECT_DIM)) * RECT_DIM
        self.y = int(ceil((randint(0, SCREEN_HEIGHT - RECT_DIM))) / float(RECT_DIM)) * RECT_DIM

        for body_part in snake.body_list:
            if self.x == body_part.x and self.y == body_part.y:
                self.reset(snake)

        self.food_rect = pygame.Rect(self.x, self.y, RECT_DIM, RECT_DIM)

    def render(self):
        pygame.draw.rect(game_screen, FOOD_COLOR, self.food_rect)


def game_loop():
    snake = Snake(SNAKE_INIT_X, SNAKE_INIT_Y)
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    snake.direct = event.key

        game_screen.fill(BG_COLOR)
        food.render()
        snake.render()
        snake.collision(food)
        snake.update_snake()
        pygame.display.update()
        clock.tick(15)


if __name__ == '__main__':
    game_loop()
