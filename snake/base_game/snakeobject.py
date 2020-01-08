import pygame

from snake.base_game.body import Body


class SnakeObject:
    def __init__(self, config):
        self.config = config
        self.body_list = list()
        self.score = 0
        self.direct = pygame.K_DOWN
        self.previous_direct = self.direct

        for i in range(config.SNAKE_INIT_LENGTH, 0, -1):
            self.body_list.append(Body(0, config.SNAKE_INIT_Y - i * config.RECT_DIM))

        self.directions = {
            pygame.K_UP: self.move_up,
            pygame.K_DOWN: self.move_down,
            pygame.K_LEFT: self.move_left,
            pygame.K_RIGHT: self.move_right
        }

    @property
    def head(self):
        return self.body_list[-1]

    @property
    def tail(self):
        return self.body_list[0]

    def move_up(self):
        self.head.y -= self.config.RECT_DIM

    def move_down(self):
        self.head.y += self.config.RECT_DIM

    def move_left(self):
        self.head.x -= self.config.RECT_DIM

    def move_right(self):
        self.head.x += self.config.RECT_DIM

    def eat_food(self, food):
        if self.head.x == food.x and self.head.y == food.y:
            self.score += 1
            eat_part = self.head
            self.body_list.insert(0, eat_part)
            return True
        else:
            return False

    def collision(self):
        # with itself
        for body_part in self.body_list:
            if body_part != self.body_list[-1] and body_part.x == self.head.x and body_part.y == self.head.y:
                return True

        # with map edges
        if not self.config.SCREEN_WIDTH > self.head.x >= 0 or not self.config.SCREEN_HEIGHT > self.head.y >= 0:
            return True
        else:
            return False

    def update_snake(self):
        self.body_list.pop(0)
        new_part = Body(self.body_list[-1].x, self.body_list[-1].y)
        self.body_list.insert(-1, new_part)
        if not self.config.AI:
            self.change_direction()

    def change_direction(self):
        if self.direct == pygame.K_RIGHT and self.previous_direct == pygame.K_LEFT or self.direct == pygame.K_LEFT and self.previous_direct == pygame.K_RIGHT or self.direct == pygame.K_UP and self.previous_direct == pygame.K_DOWN or self.direct == pygame.K_DOWN and self.previous_direct == pygame.K_UP:
            self.directions[self.previous_direct]()
        else:
            self.directions[self.direct]()
            self.previous_direct = self.direct

    def render(self, game_screen):
        for body_part in self.body_list:
            body_rect = pygame.Rect(body_part.x + 1, body_part.y + 1, self.config.RECT_DIM - 2,
                                    self.config.RECT_DIM - 2)
            if body_part == self.head:
                pygame.draw.rect(game_screen, self.config.HEAD_COLOR, body_rect)
            else:
                pygame.draw.rect(game_screen, self.config.SNAKE_COLOR, body_rect)
