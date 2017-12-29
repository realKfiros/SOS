import os
import firebase_admin
from firebase_admin import credentials
from game import Game

cred = credentials.Certificate(os.path.abspath('service-key.json'))
firebase_admin.initialize_app(cred)


class FirebaseGame(Game):
    def __init__(self, uid1, uid2):
        super(FirebaseGame, self).__init__(uid1, uid2)
