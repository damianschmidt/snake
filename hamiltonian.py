class Hamiltonian:
    def __init__(self, table):
        self.tab = table
        self.start = self.tab.get_head_id()
        self.vertices = self.tab.vertices
        self.graph = table.graph

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
            return True

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
        for i in range(34):
            print(i, self.graph[i])

        path = [-1] * self.vertices

        path[0] = self.start

        if not self.hamiltonian_utils(path, 1):
            print('Solution does not exist')
            return False

        self.print_solution(path)
        return True

    def print_solution(self, path):
        print('Solution Exists: Following is one Hamiltonian Path')
        print('Head:', self.start)
        for vertex in path:
            print(vertex, end=' ')
        print()
