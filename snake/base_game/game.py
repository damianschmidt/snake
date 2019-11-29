import pygame

from snake.base_game.food import Food
from snake.base_game.snakeobject import SnakeObject
from snake.base_game.utils import add_text

pygame.init()
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()


class Game:
    def __init__(self, config):
        self.config = config
        self.game_screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

    def game_over(self, score):
        max_score = ((self.config.SCREEN_HEIGHT * self.config.SCREEN_WIDTH) // pow(self.config.RECT_DIM,
                                                                                   2)) - self.config.SNAKE_INIT_LENGTH
        if score == max_score:
            add_text(self.game_screen, 'YOU WIN!', 'Arial', 72, (255, 255, 255), self.config.SCREEN_WIDTH / 2,
                     self.config.SCREEN_HEIGHT / 2.2)
            add_text(self.game_screen, 'YOUR SCORE: ' + str(score), 'Arial', 36, (255, 255, 255),
                     self.config.SCREEN_WIDTH / 2,
                     self.config.SCREEN_HEIGHT / 1.8)
        else:
            add_text(self.game_screen, 'GAME OVER', 'Arial', 72, (255, 255, 255), self.config.SCREEN_WIDTH / 2,
                     self.config.SCREEN_HEIGHT / 2.2)
            add_text(self.game_screen, 'YOUR SCORE: ' + str(score), 'Arial', 36, (255, 255, 255),
                     self.config.SCREEN_WIDTH / 2,
                     self.config.SCREEN_HEIGHT / 1.8)

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
                pygame.draw.rect(self.game_screen, button_color_hover,
                                 (x_button, y_button, width_button, height_button))
                if click[0] == 1:
                    self.game_loop()
            else:
                pygame.draw.rect(self.game_screen, button_color, (x_button, y_button, width_button, height_button))

            add_text(self.game_screen, 'RESTART', 'Arial', 24, (255, 255, 255), x_button + (width_button / 2),
                     y_button + (height_button / 2))

            pygame.display.update()
            clock.tick(self.config.CLOCK_TICK)

    def render(self, food, snake):
        snake.render(self.game_screen)
        food.render(self.game_screen)

    def game_loop(self):
        snake = SnakeObject(self.config)
        food = Food(self.config)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                        snake.direct = event.key

            self.game_screen.fill(self.config.BG_COLOR)
            self.render(food, snake)

            if snake.collision():
                self.game_over(snake.score)
            else:
                snake.eat_food(food)

            snake.update_snake()
            pygame.display.update()
            clock.tick(self.config.CLOCK_TICK)