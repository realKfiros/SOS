# SOS

**SOS** is a simple yet strategic pencil-and-paper game implemented in Python using the Kivy framework.  
This project was originally built in 2018 as a school assignment, inspired by a friend's idea to bring a lesser-known game to life.

## Requirements

To run this project, you need **Python 2.7**

## Setup the environment
1. Make sure you're using **Python 2.7**, I highly suggest using a [virtual environment](https://pypi.org/project/virtualenv/).
2. Install the required libraries with ```pip install -r requirements.txt```

## Run the game
```bash
python main.py
```

## The rules of the game
1. Number of players: 2
2. Board size: 9x9
3. Number of turns: 81 turns, 41 for the first player and 40 for the second
4. In each turn the player needs to choose a character: 'S' or 'O'
5. The player gets point if he made an 'SOS' streak in his turn: row, column or slant. Theoretically you can get a maximum of 12 points.
6. The game is over when all of the squares in the board are occupied (after 81 turns)
7. The winner is the player who has more points.
