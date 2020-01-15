import random

from Board import Board
from Piece import Piece


class Minimax_Base:

    def __init__(self, AI, human):
        self.ai_player = AI
        self.human_player = human

    def get_piece_value(self, piece: Piece):
        piece_values = {"Rook": 50, "Horse": 30, "Bishop": 30, "King": 900, "Queen": 800, "Pawn": 10}
        if piece.name not in piece_values:
            return 0
        return piece_values[piece.name]

    def evaluate_board(self, board: Board):
        return sum(self.get_piece_value(x) for x in board.get_pieces_for_player(self.ai_player)) - sum(
            self.get_piece_value(x) for x in board.get_pieces_for_player(self.human_player))


class Minimax(Minimax_Base):
    def __init__(self, max_depth, AI, human):
        super().__init__(AI, human)
        self.max_depth = max_depth

    def take_decision(self, board):
        best_score = -99999
        best_move = False
        possible_scores = set()
        valid_moves = []
        for piece in board.get_pieces_for_player(self.ai_player):
            all_moves = board.available_piece_moves(piece, True)
            for move in board.available_piece_moves(piece, False):
                if move not in all_moves:
                    all_moves.append(move)

            for move in all_moves:
                board_copy = Board()
                board_copy.copy(board)
                if board_copy.move(piece.position, move, False) is False:
                    continue
                value = self.minimax_with_alphabeta_pruning(board_copy, self.max_depth - 1, False, -9999999999,
                                                            9999999999)
                if value >= best_score:
                    if value != best_score:
                        print("Current best score -", str(value))
                    possible_scores.add(value)
                    valid_moves.append((piece.position, move))
                    best_score = value
                    best_move = (piece.position, move)

        if max(possible_scores) == 0 or len(possible_scores) == 1:
            print("Aleg random")
            best_move = random.choice(valid_moves)

        return best_move

    def minimax_with_alphabeta_pruning(self, board, depth, is_max, alpha, beta):
        if depth == 0:
            return self.evaluate_board(board)
        pieces = board.get_pieces_for_player(self.ai_player) if is_max else board.get_pieces_for_player(
            self.human_player)
        if is_max:
            value = -999999999999999
            for piece in pieces:
                all_moves = board.available_piece_moves(piece, True)
                for move in board.available_piece_moves(piece, False):
                    if move not in all_moves:
                        all_moves.append(move)

                for move in all_moves:
                    board_copy = Board()
                    board_copy.copy(board)
                    if board_copy.move(piece.position, move, False) is False:
                        continue
                    value = max(value,
                                self.minimax_with_alphabeta_pruning(board_copy, depth - 1, not is_max, alpha, beta))
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
            return value
        else:
            value = 999999999999999
            for piece in pieces:
                all_moves = board.available_piece_moves(piece, True)
                for move in board.available_piece_moves(piece, False):
                    if move not in all_moves:
                        all_moves.append(move)

                for move in all_moves:
                    board_copy = Board()
                    board_copy.copy(board)
                    if board_copy.move(piece.position, move, False) is False:
                        continue
                    value = min(value,
                                self.minimax_with_alphabeta_pruning(board_copy, depth - 1, not is_max, alpha, beta))
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
            return value


class MinimaxRandomSample(Minimax_Base):

    def __init__(self, AI, human, max_depth, number_of_pieces, number_of_moves):
        super().__init__(AI, human)
        self.max_depth = max_depth
        self.number_of_pieces = number_of_pieces
        self.number_of_moves = number_of_moves

    def take_decision(self, board):
        best_score = -99999
        best_move = False
        pieces = board.get_pieces_for_player(self.ai_player)
        if len(pieces) > self.number_of_pieces:
            pieces = random.sample(pieces, self.number_of_pieces)
        for piece in pieces:
            all_moves = board.available_piece_moves(piece, True)
            for move in board.available_piece_moves(piece, False):
                if move not in all_moves:
                    all_moves.append(move)
            if len(all_moves) > self.number_of_pieces:
                all_moves = random.sample(all_moves, self.number_of_moves)
            for move in all_moves:
                board_copy = Board()
                board_copy.copy(board)
                if board_copy.move(piece.position, move, False) is False:
                    continue
                value = self.minimax(board_copy, self.max_depth - 1, False)
                if value > best_score:
                    print("New score: ", str(value))
                    best_score = value
                    best_move = (piece.position, move)
        return best_move

    def minimax(self, board, depth, is_max):
        if depth == 0:
            return self.evaluate_board(board)
        pieces = board.get_pieces_for_player(self.ai_player) if is_max else board.get_pieces_for_player(
            self.human_player)
        if len(pieces) > self.number_of_pieces:
            pieces = random.sample(pieces, self.number_of_pieces)
        call = max if is_max else min
        best_score = -9999 if is_max else 9999
        for piece in pieces:
            all_moves = board.available_piece_moves(piece, True)
            for move in board.available_piece_moves(piece, False):
                if move not in all_moves:
                    all_moves.append(move)
            if len(all_moves) > self.number_of_moves:
                all_moves = random.sample(all_moves, self.number_of_moves)

            for move in all_moves:
                board_copy = Board()
                board_copy.copy(board)
                if board_copy.move(piece.position, move, False) is False:
                    continue
                best_score = call(best_score, self.minimax(board_copy, depth - 1, not is_max))
        return best_score
