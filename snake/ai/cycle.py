import sys


class Cycle:
    def __init__(self, config):
        self.moves = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        self.x_size = int(config.SCREEN_WIDTH / config.RECT_DIM)
        self.y_size = int(config.SCREEN_HEIGHT / config.RECT_DIM)
        self.init_x = 0
        self.init_y = 0
        self.board = []
        self.stack = []
        self.init_board()

    def init_board(self):
        if self.x_size * self.y_size % 2 == 0:
            self.board = [[0] * self.y_size for _ in range(self.x_size)]
            for i in range(self.x_size):
                for j in range(self.y_size):
                    self.board[i][j] = -len(self.valid_moves(i, j))
        else:
            print('Solution does not exist. Try grid with even number of fields.')
            sys.exit()

    def valid_moves(self, x, y):
        moves = []
        for move in self.moves:
            _x = x + move[0]
            _y = y + move[1]
            if 0 <= _x < self.x_size and 0 <= _y < self.y_size and self.board[_x][_y] < 1:
                moves.append((_x, _y))
        return moves

    def prioritise(self, moves):
        weights = map(lambda x: self.board[x[0]][x[1]], moves)
        _list = (list(zip(*sorted(list(zip(weights, moves))))))
        return _list[1]

    def update(self, moves, amount):
        for move in moves:
            self.board[move[0]][move[1]] += amount

    def current(self):
        return self.stack[-1][1][self.stack[-1][0]]

    def next(self):
        if not self.stack[-1][0]:
            return ()

        self.stack[-1][0] -= 1
        return self.current()

    def find_cycle(self):
        depth = 1
        self.board[self.init_x][self.init_y] = depth

        moves = self.prioritise(self.valid_moves(self.init_x, self.init_y))
        self.update(moves, 1)
        self.stack.append([len(moves), moves])

        while True:
            move = self.next()
            if move and self.valid_moves(self.init_x, self.init_y):
                depth += 1
                self.board[move[0]][move[1]] = depth
                if depth == self.x_size * self.y_size:
                    return self.get_path()
                moves = self.prioritise(self.valid_moves(move[0], move[1]))
                self.update(moves, 1)
                self.stack.append([len(moves), moves])
            else:
                moves = self.stack.pop()[1]
                if not self.stack:
                    return False
                undo = self.current()
                self.board[undo[0]][undo[1]] = -len(moves)
                self.update(moves, -1)
                depth -= 1

    def get_path(self):
        path = list(range(self.x_size * self.y_size))
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                field_id = y * len(self.board[0]) + x
                path[self.board[y][x] - 1] = field_id
        return path
