import config
from node import Node
import numpy as np


class StateTable:
    def __init__(self, snake, food):
        self.food_cord = [food.x, food.y]
        self.snake_cord = snake.body_list
        self.state = np.zeros(
            ((config.SCREEN_HEIGHT // config.RECT_DIM) + 2, (config.SCREEN_WIDTH // config.RECT_DIM) + 2))
        self.vertices = ((config.SCREEN_WIDTH // config.RECT_DIM) * (config.SCREEN_HEIGHT // config.RECT_DIM)) - (
                len(self.snake_cord) - 1)
        self.node_tab = np.empty((config.SCREEN_WIDTH // config.RECT_DIM, config.SCREEN_HEIGHT // config.RECT_DIM),
                                 dtype=object)
        self.graph = [[0 for column in range(self.vertices)] for row in range(self.vertices)]

    # empty - 0, edge - 1, snake - 2, food - 3, head - 4
    def make_state_table(self):
        # clear
        self.state = np.zeros(
            ((config.SCREEN_HEIGHT // config.RECT_DIM) + 2, (config.SCREEN_WIDTH // config.RECT_DIM) + 2))
        # edges
        self.state[0], self.state[-1], self.state[:, 0], self.state[:, -1] = 1, 1, 1, 1
        # food
        self.state[(self.food_cord[1] // config.RECT_DIM) + 1, (self.food_cord[0] // config.RECT_DIM) + 1] = 3
        # snake
        for snake_part in self.snake_cord:
            self.state[(int(snake_part.y) // config.RECT_DIM) + 1, (int(snake_part.x) // config.RECT_DIM) + 1] = 2
        # head
        self.state[(int(self.snake_cord[-1].y) // config.RECT_DIM) + 1, (
                int(self.snake_cord[-1].x) // config.RECT_DIM) + 1] = 4

    def possibilities_of_move(self):
        id = 0
        self.vertices = ((config.SCREEN_WIDTH // config.RECT_DIM) * (config.SCREEN_HEIGHT // config.RECT_DIM)) - (
                len(self.snake_cord) - 1)
        # possibilities_graph = [[0 for column in range(self.vertices)] for row in range(self.vertices)]

        for x in range(len(self.state)):
            for y in range(len(self.state)):
                if self.state[y, x] == 0 or self.state[y, x] == 3 or self.state[y, x] == 4:
                    possibilities = ''
                    possibilities += '1' if self.state[y, x - 1] != 1 and self.state[y, x - 1] != 2 else '0'
                    possibilities += '1' if self.state[y - 1, x] != 1 and self.state[y - 1, x] != 2 else '0'
                    possibilities += '1' if self.state[y, x + 1] != 1 and self.state[y, x + 1] != 2 else '0'
                    possibilities += '1' if self.state[y + 1, x] != 1 and self.state[y + 1, x] != 2 else '0'

                    new_node = Node(id, possibilities)
                    if self.state[y, x] == 4:
                        new_node.head = True

                    self.node_tab[x - 1, y - 1] = new_node
                    id += 1

        for x in range(len(self.node_tab)):
            for y in range(len(self.node_tab)):
                if self.node_tab[x, y] is not None:
                    if self.node_tab[x, y].left:
                        self.graph[self.node_tab[x, y].id][self.node_tab[x - 1, y].id] = 1
                    if self.node_tab[x, y].right:
                        self.graph[self.node_tab[x, y].id][self.node_tab[x + 1, y].id] = 1
                    if self.node_tab[x, y].up:
                        self.graph[self.node_tab[x, y].id][self.node_tab[x, y - 1].id] = 1
                    if self.node_tab[x, y].down:
                        self.graph[self.node_tab[x, y].id][self.node_tab[x, y + 1].id] = 1

    def get_head_id(self):
        for node_row in self.node_tab:
            for node in node_row:
                if node != None and node.head:
                    return node.id
