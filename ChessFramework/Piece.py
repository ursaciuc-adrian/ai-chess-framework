from enum import Enum
from Position import Position

class Player(Enum):
	WHITE = 1 # up
	BLACK = 2 # down

class Piece():
	player: Player
	position: Position

	name = ""
	id = ""

	# defines how the pice can move
	# for horse: 3left1up, 1up3left, 1up3right ... 
	moves = []

	# defines how the piece can attack
	# for pawn: 1lu (1 position to upper left), 1ru
	attacks = []

	def __init__(self, name, id):
		self.moves = []
		self.attacks = []
		self.name = name
		self.id = id

	def __str__(self):
		data = "Position: " + str(self.position)+ "\n"
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
			self.moves = move
		else:
			self.moves.append(move)

	def addAttack(self, attack):
		if isinstance(attack, list):
			self.attacks = attack
		else:
			self.attacks.append(attack)
