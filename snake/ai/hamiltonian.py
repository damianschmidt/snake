import operator


class Hamiltonian:
    def __init__(self, table, config):
        self.tab = table
        self.start = self.tab.get_head_id()
        self.vertices = self.tab.vertices
        self.graph = table.graph
        self.path = []
        self.path_counter = 0
        self.hamiltonian_cycle()
        self.config = config

    def is_safe(self, v, pos, path):
        if self.graph[path[pos - 1]][v] == 0:
            return False

        # Check if current vertex not already in path
        for vertex in path:
            if vertex == v:
                return False
        return True

    def hamiltonian_utils(self, path, pos):
        if pos == self.vertices:
            if self.graph[path[pos - 1]][path[0]] == 1:
                return True
            else:
                return False

        for v in range(0, self.vertices):
            if self.is_safe(v, pos, path):
                path[pos] = v

                if self.hamiltonian_utils(path, pos + 1):
                    return True

                # Remove current vertex if it doesn't
                # lead to a solution
                path[pos] = -1
        return False

    def hamiltonian_cycle(self):
        path = [-1] * self.vertices
        path[0] = self.start

        if not self.hamiltonian_utils(path, 1):
            print('Solution does not exist')
            return False

        self.path = path
        self.print_solution()
        return True

    def hamiltonian_move(self, snake, food):
        current_position, shortcut = self.take_shortcut(food, snake)

        if shortcut is not None and shortcut != self.path_counter + 1:
            self.shortcut_move(current_position, shortcut, snake)
        elif self.path_counter == self.vertices - 1:
            self.last_move(snake)
        else:
            self.regular_move(snake)

    def take_shortcut(self, food, snake):
        head_x, head_y = int(snake.head.x / self.config.RECT_DIM), int(snake.head.y / self.config.RECT_DIM)
        food_position, head_position, tail_position = self.get_food_and_snake_position(food, snake)

        head_index = self.path.index(head_position)
        tail_index = self.path.index(tail_position)
        food_index = self.path.index(food_position)

        indexes = self.indexes_of_possible_moves(head_x, head_y)
        index_with_distance = self.distance_to_food(food_index, indexes)

        shortcut = None
        shortcut = self.get_shortcut_if_safe(head_index, index_with_distance, shortcut, tail_index)
        return head_position, shortcut

    def get_shortcut_if_safe(self, head_index, index_with_distance, shortcut, tail_index):
        for index, _ in index_with_distance:
            if head_index > tail_index and (
                    index < tail_index - self.config.SAFE_FIELD_SPACE or index > head_index):
                shortcut = index
                break
            elif head_index < tail_index and (head_index < index < tail_index - self.config.SAFE_FIELD_SPACE):
                shortcut = index
                break
        return shortcut

    def distance_to_food(self, food_index, indexes):
        index_with_distance = []
        for index in indexes:
            if index <= food_index:
                distance = food_index - index
            else:
                distance = len(self.path) - 1 - index + food_index
            index_with_distance.append((index, distance))
        index_with_distance.sort(key=operator.itemgetter(1))
        return index_with_distance

    def indexes_of_possible_moves(self, head_x, head_y):
        x_edge, y_edge = self.tab.node_tab.shape
        up_position = self.tab.node_tab[head_x, head_y - 1].id if head_y - 1 >= 0 else None
        down_position = self.tab.node_tab[head_x, head_y + 1].id if head_y + 1 < y_edge else None
        left_position = self.tab.node_tab[head_x - 1, head_y].id if head_x - 1 >= 0 else None
        right_position = self.tab.node_tab[head_x + 1, head_y].id if head_x + 1 < x_edge else None

        # find index in cycle
        up_index = self.path.index(up_position) if up_position is not None else up_position
        down_index = self.path.index(down_position) if down_position is not None else down_position
        left_index = self.path.index(left_position) if left_position is not None else left_position
        right_index = self.path.index(right_position) if right_position is not None else right_position

        return [x for x in [up_index, down_index, left_index, right_index] if x is not None]

    def get_food_and_snake_position(self, food, snake):
        food_x, food_y = int(food.x / self.config.RECT_DIM), int(food.y / self.config.RECT_DIM)
        head_x, head_y = int(snake.head.x / self.config.RECT_DIM), int(snake.head.y / self.config.RECT_DIM)
        tail_x, tail_y = int(snake.tail.x / self.config.RECT_DIM), int(snake.tail.y / self.config.RECT_DIM)

        head_position = self.tab.node_tab[head_x, head_y].id
        tail_position = self.tab.node_tab[tail_x, tail_y].id
        food_position = self.tab.node_tab[food_x, food_y].id
        return food_position, head_position, tail_position

    def shortcut_move(self, current_position, shortcut, snake):
        self.move(snake, current_position, self.path[shortcut])
        self.path_counter = self.path.index(self.path[shortcut])

    @staticmethod
    def move(snake, current_position, next_position):
        if current_position == next_position - 1:
            snake.move_right()
        elif current_position == next_position + 1:
            snake.move_left()
        elif current_position < next_position - 1:
            snake.move_down()
        elif current_position > next_position + 1:
            snake.move_up()

    def regular_move(self, snake):
        self.move(snake, self.path[self.path_counter], self.path[self.path_counter + 1])
        self.path_counter += 1

    def last_move(self, snake):
        self.move(snake, self.path[self.path_counter], self.path[0])
        self.path_counter = 0

    def print_solution(self):
        print('Solution Exists: Following is one Hamiltonian Path')
        for vertex in self.path:
            print(vertex, end=' ')
        print()
