from Piece import Piece, Player
from Position import Position
from Guard import Guard

from copy import copy
import re

class Board(object):
	SIZE = 8

	board = []

	def init_board(self):
		self.board = [[None for j in range(self.SIZE)] for i in range(self.SIZE)]

		piece = Piece("Pawn", "P")
		piece.addMove(["1u", "2u"])
		piece.addAttack(["1ur", "1ul"])

		for i in range(self.SIZE):
			self.add_piece(piece, Position(1, i), Player.WHITE)

		for i in range(self.SIZE):
			self.add_piece(piece, Position(6, i), Player.BLACK)

		piece = Piece("Horse", "H")
		piece.addMove(["1l2u", "1r2u"])
		piece.addAttack(["1l2u", "1r2u"])

		self.add_piece(piece, Position(0, 1), Player.BLACK)
		self.add_piece(piece, Position(0, 6), Player.BLACK)

		self.add_piece(piece, Position(7, 1), Player.BLACK)
		self.add_piece(piece, Position(7, 6), Player.BLACK)

	def add_piece(self, piece: Piece, position: Position, player: Player):
		Guard.check_position(position, self.SIZE)

		piece.set_position(position)
		piece.set_player(player)
		self.board[piece.position.x][piece.position.y] = copy(piece)

	def display_pieces(self):
		for i in range(self.SIZE):
			for j in range(self.SIZE):
				if self.board[i][j] is not None:
					print(self.board[i][j])
			print()

	def display_board(self):
		for i in range(self.SIZE):
			for j in range(self.SIZE):
				if self.board[i][j] is not None:
					print(self.board[i][j].id + " ", end="")
				else:
					print("0 ", end="")
			print()
		print()
	
	def split(self, s):
		r = re.compile("([0-9]+)([a-zA-Z]+)")
		return r.findall(s)

	def available_moves(self, piece: Piece, eat = False):
		positions = []
		
		p_or = 1 if piece.player == Player.WHITE else -1
		it_moves = piece.moves if eat == False else piece.attacks

		for move_str in it_moves:
			moves = self.split(move_str)
			x = piece.position.x
			y = piece.position.y
			for move in moves:
				if move[1] == 'u':
					x += p_or * int(move[0])
				if move[1] == 'd':
					x -= p_or * int(move[0])
				if move[1] == 'r':
					y += int(move[0])
				if move[1] == 'l':
					y -= int(move[0])

				if move[1] == 'ul':
					x += p_or * int(move[0])
					y -= int(move[0])
				if move[1] == 'bl':
					x -= p_or * int(move[0])
					y -= int(move[0])
				if move[1] == 'ur':
					x += p_or * int(move[0])
					y += int(move[0])
				if move[1] == 'br':
					x -= p_or * int(move[0])
					y += int(move[0])

			new_pos = Position(x, y)
			if new_pos.is_in_boundary(self.SIZE):
				positions.append(Position(x, y))
		
		for p in positions:
			print(p)

		return positions

	def can_move(self, from_pos: Position, to_pos: Position):
		if not from_pos.is_in_boundary(self.SIZE) or not to_pos.is_in_boundary(self.SIZE):
			return False

		from_piece: Piece = self.board[from_pos.x][from_pos.y]
		if from_piece is None:
			return False

		to_piece: Piece = self.board[to_pos.x][to_pos.y]
		if to_piece is not None:
			return False

		available_moves = self.available_moves(from_piece)
		if to_pos in available_moves:
			return True

		return False

	def can_eat(self, from_pos: Position, to_pos: Position):
		if not from_pos.is_in_boundary(self.SIZE) or not to_pos.is_in_boundary(self.SIZE):
			return False

		from_piece: Piece = self.board[from_pos.x][from_pos.y]
		if from_piece is None:
			return False

		to_piece: Piece = self.board[to_pos.x][to_pos.y]
		if to_piece is None:
			return False

		if from_piece.player == to_piece.player:
			return False

		available_moves = self.available_moves(from_piece, eat=True)
		if to_pos in available_moves:
			return True

		return False

	def move(self, from_pos: Position, to_pos: Position):
		if self.can_move(from_pos, to_pos) or self.can_eat(from_pos, to_pos):
			self.board[to_pos.x][to_pos.y] = self.board[from_pos.x][from_pos.y]
			self.board[to_pos.x][to_pos.y].position = to_pos
			self.board[from_pos.x][from_pos.y] = None
		else:
			print("Invalid move.")