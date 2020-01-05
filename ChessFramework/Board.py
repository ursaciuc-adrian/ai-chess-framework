from Piece import Piece, Player
from Position import Position
from Guard import Guard
from Move import *
from copy import copy
import re


class Board(object):
    """Represents the chess table manager. It creates the custom pieces, handles its movements and also the special movements which are multiple pieces movement or based on piece movement history."""
    SIZE = 8

    board = []

    def init_board(self):
        """Initializes the pieces on the board."""
        self.board = [[None for j in range(self.SIZE)] for i in range(self.SIZE)]

        # CREATE CUSTOM PIECES
        piece = Piece("Pawn", "P")
        piece.addMove(PawnMovement.moves)
        piece.addAttack(PawnMovement.attacks)

        for i in range(self.SIZE):
            self.add_piece(piece, Position(1, i), Player.WHITE)

        for i in range(self.SIZE):
            self.add_piece(piece, Position(6, i), Player.BLACK)

        piece = Piece("Horse", "H")
        piece.addMove(HorseMovement.moves)
        piece.attackWhileMove = True

        # PLACE PIECES ON BOARD
        self.add_piece(piece, Position(0, 1), Player.WHITE)
        self.add_piece(piece, Position(0, 6), Player.WHITE)

        self.add_piece(piece, Position(7, 1), Player.BLACK)
        self.add_piece(piece, Position(7, 6), Player.BLACK)


    def add_piece(self, piece: Piece, position: Position, player: Player):
        """Adds a piece on the board."""
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


    def available_piece_moves(self, piece: Piece, attack=False):
        positions = []

        p_or = 1 if piece.player == Player.WHITE else -1
        if attack == True and piece.attackWhileMoves == False:
            it_moves = piece.attacks
        else:
            it_moves = piece.moves

        for move in it_moves:
            x = piece.position.x
            y = piece.position.y

            y += p_or * move[1]
            x += move[0]

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

        # should check special moves also (not per piece only)
        available_moves = self.available_piece_moves(from_piece)
        if to_pos in available_moves:
            return True

        return False


    def can_attack(self, from_pos: Position, to_pos: Position):
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

        # should beck special moves also (not per piece only)
        available_moves = self.available_piece_moves(from_piece, attack=True)
        if to_pos in available_moves:
            return True

        return False


    def move(self, from_pos: Position, to_pos: Position):
        if self.can_move(from_pos, to_pos) or self.can_attack(from_pos, to_pos):
            self.board[to_pos.x][to_pos.y] = self.board[from_pos.x][from_pos.y]
            self.board[to_pos.x][to_pos.y].position = to_pos
            self.board[from_pos.x][from_pos.y] = None
        else:
            print("Invalid move.")
