class Node:
    def __init__(self, id, possibilities):
        self.id = id
        self.head = False
        self.left = True if str(possibilities)[0] == '1' else False
        self.up = True if str(possibilities)[1] == '1' else False
        self.right = True if str(possibilities)[2] == '1' else False
        self.down = True if str(possibilities)[3] == '1' else False


