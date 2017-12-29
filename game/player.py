class Player:
    def __init__(self, name):
        self.name = name
        self.points = 0

    def addpoints(self, n):
        self.points += n