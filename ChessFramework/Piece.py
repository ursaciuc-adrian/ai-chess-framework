from enum import Enum
from Position import Position


class Player(Enum):
    WHITE = 1  # up
    BLACK = 2  # down


class Piece():
    player: Player
    position: Position

    name = ""
    id = ""

    # defines how the pice can move
    # for horse: 3left1up = (1, -3), 1up3left (1, -3), 1up3right, (1, 3) ...
    moves = []

    # defines how the piece can attack
    # for pawn: 1lu (1 position to upper left = (1, -1)), 1ru = (1, 1))
    attacks = []

    def __init__(self, name, id):
        self.moves = []
        self.attacks = []
        self.name = name
        self.id = id
        self.attackWhileMoves = False

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

    def addMove(self, move):
        if isinstance(move, list):
            self.moves += move
        elif isinstance(move, Move):
            self.moves += Move.moves  
        else:
            self.moves.append(move)

    def addAttack(self, attack):
        if isinstance(attack, list):
            self.attacks = attack
        elif isinstance(attack, Move):
            self.attacks += Move.attacks
        else:
            self.attacks.append(attack)
