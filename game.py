import pygame
import config
import state_table
import snake as s
from food import Food
from hamiltonian import Hamiltonian

pygame.init()
game_screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()


def game_loop():
    snake = s.Snake(config.SNAKE_INIT_X, config.SNAKE_INIT_Y)
    food = Food()
    tab = state_table.StateTable(snake, food)
    tab.make_state_table()
    tab.possibilities_of_move()
    print(tab.state)
    ham = Hamiltonian(tab)
    ham.hamiltonian_cycle()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    snake.direct = event.key

        game_screen.fill(config.BG_COLOR)
        food.render()
        snake.render()
        snake.collision(food)
        snake.update_snake()
        tab.make_state_table()
        pygame.display.update()
        clock.tick(config.CLOCK_TICK)


if __name__ == '__main__':
    game_loop()
