from Piece import Piece, Player
from Position import Position
from Guard import Guard
from Move import *
from copy import copy, deepcopy
import re


class Board(object):
    """Represents the chess table manager. It creates the custom pieces, handles its movements and also the special movements which are multiple pieces movement or based on piece movement history."""
    SIZE = 8

    board = []
    fifty_moves_rule_count = 0
    moves_count = 0

    def init_board(self):
        """Initializes the pieces on the board."""
        self.board = [[None for j in range(self.SIZE)] for i in range(self.SIZE)]

        # CREATE CUSTOM PIECES
        piece = Piece("Pawn", "P")
        piece.add_movement(PawnMovement())

        for i in range(self.SIZE):
            self.add_piece(piece, Position(1, i), Player.WHITE)

        for i in range(self.SIZE):
            self.add_piece(piece, Position(6, i), Player.BLACK)

        piece = Piece("Horse", "H")
        piece.add_movement(HorseMovement())

        # PLACE PIECES ON BOARD
        self.add_piece(piece, Position(0, 1), Player.WHITE)
        self.add_piece(piece, Position(0, 6), Player.WHITE)

        self.add_piece(piece, Position(7, 1), Player.BLACK)
        self.add_piece(piece, Position(7, 6), Player.BLACK)

        piece = Piece("Rook", "R")
        piece.add_movement(HorizontalMovement())
        piece.add_movement(VerticalMovement())

        self.add_piece(piece, Position(0, 0), Player.WHITE)
        self.add_piece(piece, Position(0, 7), Player.WHITE)

        self.add_piece(piece, Position(7, 0), Player.BLACK)
        self.add_piece(piece, Position(7, 7), Player.BLACK)

        piece = Piece("Bishop", "B")
        piece.add_movement(DiagonalMovement())

        self.add_piece(piece, Position(0, 2), Player.WHITE)
        self.add_piece(piece, Position(0, 5), Player.WHITE)

        self.add_piece(piece, Position(7, 2), Player.BLACK)
        self.add_piece(piece, Position(7, 5), Player.BLACK)

        piece = Piece("Queen", "Q")
        piece.add_movement(HorizontalMovement())
        piece.add_movement(VerticalMovement())
        piece.add_movement(DiagonalMovement())

        self.add_piece(piece, Position(0, 4), Player.WHITE)
        self.add_piece(piece, Position(7, 4), Player.BLACK)

        piece = Piece("King", "K")
        piece.add_movement(LimitedHorizontalMovement())
        piece.add_movement(LimitedVerticalMovement())
        piece.add_movement(LimitedDiagonalMovement())

        self.add_piece(piece, Position(0, 3), Player.WHITE)
        self.add_piece(piece, Position(7, 3), Player.BLACK)

    def copy(self, other):
        if not isinstance(other, Board):
            return False
        self.board = deepcopy(other.board)
        self.SIZE = other.SIZE

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

    def get_pieces(self):
        pieces = []
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if self.board[i][j] is not None:
                    pieces.append(self.board[i][j])
        return pieces

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
        for movement in piece.movements:
            moves = movement.attacks if attack else movement.moves

            for move in moves:
                x = piece.position.x
                y = piece.position.y

                y += move[1]
                x += p_or * move[0]
                new_pos = Position(x, y)
                if new_pos.is_in_boundary(self.SIZE):
                    positions.append(Position(x, y))

                while movement.vacant:
                    y += move[1]
                    x += p_or * move[0]

                    new_pos = Position(x, y)
                    if new_pos.is_in_boundary(self.SIZE) and self.board[new_pos.x][new_pos.y] is None:
                        positions.append(Position(x, y))
                    elif new_pos.is_in_boundary(self.SIZE) and attack == True:
                        positions.append(Position(x, y))
                        break
                    else:
                        break

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

    def move(self, from_pos: Position, to_pos: Position, verbose=True):
        if self.can_move(from_pos, to_pos) or self.can_attack(from_pos, to_pos):
            # if a piece is taken out then fifty_moves_rule_count is updated
            if self.board[to_pos.x][to_pos.y] is not None:
                self.fifty_moves_rule_count = self.moves_count

            self.board[to_pos.x][to_pos.y] = self.board[from_pos.x][from_pos.y]
            self.board[to_pos.x][to_pos.y].position = to_pos
            self.board[from_pos.x][from_pos.y] = None

            # moves_count incremented, needed for the fifty moves rule draw
            self.moves_count += 1
            # if a pawn is moved on either side the fifty_moves_rule_count is updated
            if self.get_piece_id_from_board_position(to_pos.x, to_pos.y) == 'P':
                self.fifty_moves_rule_count = self.moves_count
        else:
            if verbose:
                print("Invalid move.")
            return False

    def get_player_from_pos(self, from_pos: Position):
        if self.board[from_pos.x][from_pos.y]:
            return self.board[from_pos.x][from_pos.y].player

        return None

    def is_attacked(self, piece: Piece, player: Player):
        """Method to verify if the piece from the player is attacked."""
        for attacking_piece in self.get_pieces():
            if attacking_piece.player != player and self.can_attack(attacking_piece.position, piece.position):
                return True
        return False

    def is_draw(self, mode='fifty_moves'):
        """Checks if it is a drawn"""
        # fifty moves rule
        if mode == 'fifty_moves':
            if self.moves_count + 50 >= self.fifty_moves_rule_count:
                return True
        if mode == 'three_fold':
            pass
        return False

    def is_check(self, player: Player):
        """ Checks if it is check for the player"""
        for piece in self.get_pieces_for_player(player):
            if piece.id == 'K':
                if self.is_attacked(piece, player):
                    return True
                else:
                    return False

    def is_check_mate(self, player: Player):
        """ Checks if it is check mate for the player"""
        for piece in self.get_pieces_for_player(player):
            board_copy = deepcopy(self)

            # Check if moving the piece makes the player not be in check anymore
            for position in self.available_piece_moves(piece):
                initial_position = piece.position

                if self.can_move(initial_position, position):
                    board_copy.move(initial_position, position)
                    if not self.is_check(player):
                        return False
                    else:
                        board_copy.move(position, initial_position)

            # Check if attacking a piece makes the player not be in check anymore
            for position in self.available_piece_moves(piece, attack=True):
                initial_position = piece.position

                if self.can_attack(initial_position, position):
                    board_copy.move(initial_position, position)
                    if not self.is_check(player):
                        return False
                    else:
                        board_copy.move(position, initial_position)
        return True

    def get_pieces_for_player(self, player: Player):
        pieces = []
        for piece in self.get_pieces():
            if piece.player == player:
                pieces.append(piece)
        return pieces

    def get_piece_id_from_board_position(self, line_pos, col_pos):
        for piece in self.get_pieces():
            if piece.position.x == line_pos and piece.position.y == col_pos:
                return piece.id
