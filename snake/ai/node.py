class Node:
    def __init__(self, node_id, possibilities):
        self.id = node_id
        self.head = False
        self.left = True if str(possibilities)[0] == '1' else False
        self.up = True if str(possibilities)[1] == '1' else False
        self.right = True if str(possibilities)[2] == '1' else False
        self.down = True if str(possibilities)[3] == '1' else False

    def __str__(self):
        print(
            '\nid:', self.id,
            '\nhead:', self.head,
            '\nleft:', self.left,
            '\nup:', self.up,
            '\nright:', self.right,
            '\ndown:', self.down,
        )
