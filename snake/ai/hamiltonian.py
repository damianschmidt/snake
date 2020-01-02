from snake.base_game.utils import print_solution


class Hamiltonian:
    def __init__(self, table):
        self.tab = table
        self.start = self.tab.get_head_id()
        self.vertices = self.tab.vertices
        self.graph = table.graph
        self.path = []
        self.path_counter = 0

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
        print_solution(self.path)
        return True

    def hamiltonian_move(self, snake):
        if self.path_counter == self.vertices - 1:
            self.last_move(snake)
        else:
            self.regular_move(snake)

    def regular_move(self, snake):
        if self.path[self.path_counter] == self.path[self.path_counter + 1] - 1:
            snake.move_right()
        elif self.path[self.path_counter] == self.path[self.path_counter + 1] + 1:
            snake.move_left()
        elif self.path[self.path_counter] < self.path[self.path_counter + 1] - 1:
            snake.move_down()
        elif self.path[self.path_counter] > self.path[self.path_counter + 1] + 1:
            snake.move_up()
        self.path_counter += 1

    def last_move(self, snake):
        if self.path[self.path_counter] == self.path[0] - 1:
            snake.move_right()
        elif self.path[self.path_counter] == self.path[0] + 1:
            snake.move_left()
        elif self.path[self.path_counter] < self.path[0] - 1:
            snake.move_down()
        elif self.path[self.path_counter] > self.path[0] + 1:
            snake.move_up()
        self.path_counter = 0
