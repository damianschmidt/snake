import config
import pygame
from utils import add_text
from body import Body
import game


class Snake(object):
    def __init__(self, x, y):
        self.CLOCK_TICK = 10
        self.body_list = list()
        self.score = 0
        self.direct = pygame.K_RIGHT
        self.previous_direct = self.direct

        for i in range(config.SNAKE_INIT_LENGTH, 0, -1):
            self.body_list.append(Body(x - i * config.RECT_DIM, y))

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
        add_text('GAME OVER', 'Arial', 72, (255, 255, 255), config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2.2)
        add_text('YOUR SCORE: ' + str(self.score), 'Arial', 36, (255, 255, 255), config.SCREEN_WIDTH / 2,
                 config.SCREEN_HEIGHT / 1.8)

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
                pygame.draw.rect(game.game_screen, button_color_hover,
                                 (x_button, y_button, width_button, height_button))
                if click[0] == 1:
                    game.game_loop()
            else:
                pygame.draw.rect(game.game_screen, button_color, (x_button, y_button, width_button, height_button))

            add_text('RESTART', 'Arial', 24, (255, 255, 255), x_button + (width_button / 2),
                     y_button + (height_button / 2))

            pygame.display.update()
            game.clock.tick(self.CLOCK_TICK)

    def move_up(self):
        self.head.y -= config.RECT_DIM

    def move_down(self):
        self.head.y += config.RECT_DIM

    def move_left(self):
        self.head.x -= config.RECT_DIM

    def move_right(self):
        self.head.x += config.RECT_DIM

    def eat_food(self, food):
        food.reset(self)
        self.score += 1
        eat_part = self.head
        self.body_list.insert(0, eat_part)

    def collision(self, food):
        # with food
        if self.head.x == food.x and self.head.y == food.y:
            self.eat_food(food)

        # with itself
        for body_part in self.body_list:
            if body_part != self.body_list[-1] and body_part.x == self.head.x and body_part.y == self.head.y:
                self.game_over()

        # with map edges
        if not config.SCREEN_WIDTH > self.head.x >= 0 or not config.SCREEN_HEIGHT > self.head.y >= 0:
            self.game_over()

    def update_snake(self):
        self.body_list.pop(0)
        new_part = Body(self.body_list[-1].x, self.body_list[-1].y)
        self.body_list.insert(-1, new_part)
        self.change_direction()

    def change_direction(self):
        if self.direct == pygame.K_RIGHT and self.previous_direct == pygame.K_LEFT or self.direct == pygame.K_LEFT and self.previous_direct == pygame.K_RIGHT or self.direct == pygame.K_UP and self.previous_direct == pygame.K_DOWN or self.direct == pygame.K_DOWN and self.previous_direct == pygame.K_UP:
            self.directions[self.previous_direct]()
        else:
            self.directions[self.direct]()
            self.previous_direct = self.direct

    def render(self):
        for body_part in self.body_list:
            body_rect = pygame.Rect(body_part.x, body_part.y, config.RECT_DIM, config.RECT_DIM)
            pygame.draw.rect(game.game_screen, config.SNAKE_COLOR, body_rect)
