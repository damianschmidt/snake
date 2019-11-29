from snake.base_game.config import Config
from snake.base_game.game import Game

if __name__ == '__main__':
    config = Config()
    game = Game(config)
    game.game_loop()
