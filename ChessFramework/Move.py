class Movement:
    """No movement"""
    moves = []
    attacks = []


class HorseMovement(Movement):
    """Regular horse/king movement: can move once in L."""
    moves = [(2, 1), (2, -1), (1, -2), (1, 2), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    attacks = [(2, 1), (2, -1), (1, -2), (1, 2), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    name = "Horse movement"
    vacant = False


class LimitedDiagonalMovement(Movement):
    """Can move only once diagonally (King like)"""
    moves = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
    attacks = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
    name = "Limited diagonal movement"
    vacant = False


class LimitedHorizontalMovement(Movement):
    """Can move only once horizontally (King like)"""
    moves = [(0, -1), (0, 1)]
    attacks = [(0, -1), (0, 1)]
    name = "Limited horizontal movement"
    vacant = False


class LimitedVerticalMovement(Movement):
    """Can move only once vertically (King like)"""
    moves = [(1, 0), (-1, 0)]
    attacks = [(1, 0), (-1, 0)]
    name = "Limited vertical movement"
    vacant = False


class DiagonalMovement(Movement):
    """Can move a vacant number of times diagonally"""
    moves = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
    attacks = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
    name = "Diagonal movement"
    vacant = True


class HorizontalMovement(Movement):
    """Can move a vacant number of times horizontally"""
    moves = [(0, -1), (0, 1)]
    attacks = [(0, -1), (0, 1)]
    name = "Horizontal movement"
    vacant = True


class VerticalMovement(Movement):
    """Can move a vacant number of times vertically"""
    moves = [(1, 0), (-1, 0)]
    attacks = [(1, 0), (-1, 0)]
    name = "Vertical movement"
    vacant = True


class PawnMovement(Movement):
    """Regular (not conditional) pawn movements"""
    moves = [(1, 0)]  # (2, 0) is a special movement only when pawn didn't move
    attacks = [(1, 1), (1, -1)]
    name = "Pawn movement"
    vacant = False


class CustomMovement(Movement):
    def __init__(self):
        self.moves = []
        self.attacks = []
        self.name = "Custom movement"
        self.vacant = False

    def set_name(self, new_name):
        self.name = new_name

    def add_custom_movement(self, x, y):
        self.moves.append((x, y))

    def add_custom_attack(self, x, y):
        self.attacks.append((x, y))

    def set_vacant(self, value):
        """Can apply the movement a variable number of times each turn"""
        self.vacant = value
