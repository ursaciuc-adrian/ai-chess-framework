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
        if self.id == 'P':
            self.value = 10
        elif self.id == 'H':
            self.value = 20
        elif self.id == 'B':
            self.value = 30
        elif self.id == 'R':
            self.value = 40
        elif self.id == 'Q':
            self.value = 50
        elif self.id == 'K':
            self.value = 100

    def __str__(self):
        data = "Position: " + str(self.position) + "\n"
        data += "Name: " + self.name + "\n"
        data += "Id: " + self.id + "\n"
        data += "Moves: "

        for m in self.movements:
            data += m.__class__.__name__ + ", "

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
