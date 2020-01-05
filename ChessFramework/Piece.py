from enum import Enum
from Position import Position
from Move import Movement

class Player(Enum):
    WHITE = 1  # up
    BLACK = 2  # down


class Piece():
    player: Player
    position: Position

    name = ""
    id = ""

    movements = []

    def __init__(self, name, id):
        self.movements = []
        self.name = name
        self.id = id

    def __str__(self):
        data = "Position: " + str(self.position) + "\n"
        data += "Name: " + self.name + "\n"
        data += "Id: " + self.id + "\n"
        data += "Moves: " + str(self.moves) + "\n"
        data += "Attacks: " + str(self.attacks) + "\n"

        return data

    def set_position(self, position: Position):
        self.position = position

    def set_player(self, player: Player):
        self.player = player


    def add_movement(self, movement):
        if isinstance(movement, Movement):
            self.movements.append(movement)
            return

        print('Tried to attach something that is not a movement to the piece:' + str(movement))
