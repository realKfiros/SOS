import os
from game.StartScreen import StartScreen


if __name__ == "__main__":
    game = StartScreen(os.path)
    game.back.source = os.path.abspath('assets/startscrback.jpg')
    game.run()