import numpy as np

from snake.ai.node import Node


class StateTable:
    def __init__(self, snake, config):
        self.config = config
        self.snake_cord = snake.body_list[-1]
        self.state = np.zeros(
            ((config.SCREEN_HEIGHT // config.RECT_DIM) + 2, (config.SCREEN_WIDTH // config.RECT_DIM) + 2))
        self.vertices = ((config.SCREEN_WIDTH // config.RECT_DIM) * (config.SCREEN_HEIGHT // config.RECT_DIM))
        self.node_tab = np.empty((config.SCREEN_WIDTH // config.RECT_DIM, config.SCREEN_HEIGHT // config.RECT_DIM),
                                 dtype=object)
        self.graph = [[0 for column in range(self.vertices)] for row in range(self.vertices)]

    # empty - 0, edge - 1, head - 2
    def make_state_table(self):
        # clear
        self.state = np.zeros(
            ((self.config.SCREEN_HEIGHT // self.config.RECT_DIM) + 2,
             (self.config.SCREEN_WIDTH // self.config.RECT_DIM) + 2))
        # edges
        self.state[0], self.state[-1], self.state[:, 0], self.state[:, -1] = 1, 1, 1, 1
        # head
        self.state[(int(self.snake_cord.y) // self.config.RECT_DIM) + 1, (
                int(self.snake_cord.x) // self.config.RECT_DIM) + 1] = 2

    def possibilities_of_move(self):
        node_id = 0

        for x in range(len(self.state)):
            for y in range(len(self.state)):
                if self.state[x, y] == 0 or self.state[x, y] == 2:
                    possibilities = ''
                    possibilities += '1' if self.state[x, y - 1] != 1 else '0'
                    possibilities += '1' if self.state[x - 1, y] != 1 else '0'
                    possibilities += '1' if self.state[x, y + 1] != 1 else '0'
                    possibilities += '1' if self.state[x + 1, y] != 1 else '0'

                    new_node = Node(node_id, possibilities)
                    if self.state[x, y] == 2:
                        new_node.head = True

                    self.node_tab[y - 1, x - 1] = new_node
                    node_id += 1

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
                if node is not None and node.head:
                    return node.id
