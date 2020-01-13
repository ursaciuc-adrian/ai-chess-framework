from Board import Board
from Piece import Player
from Piece import Piece

ai_player = 0
human_player = 0


def set_AI(AI, human):
    global ai_player, human_player
    ai_player = AI
    human_player = human


def get_piece_value(piece: Piece):
    piece_values = {"Rook": 50, "Horse": 30, "Bishop": 30, "King": 900, "Queen": 800, "Pawn": 10}
    if piece.name not in piece_values:
        return 0
    return piece_values[piece.name]


def evaluate_board(board: Board):
    return sum(get_piece_value(x) for x in board.get_pieces_for_player(ai_player)) - sum(
        get_piece_value(x) for x in board.get_pieces_for_player(human_player))


class Minimax:
    def __init__(self, max_depth):
        self.max_depth = max_depth

    def take_decision(self, board):
        best_score = -99999
        best_move = False
        for piece in board.get_pieces_for_player(ai_player):
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
                if value > best_score:
                    print("New score: ", str(value))
                    best_score = value
                    best_move = (piece.position, move)
        return best_move

    '''def minimax(self, board, depth, is_max):
        if depth == 0:
            return evaluate_board(board)
        pieces = board.get_pieces_for_player(ai_player) if is_max else board.get_pieces_for_player(human_player)
        call = max if is_max else min
        best_score = -9999 if is_max else 9999
        for piece in pieces:
            all_moves = board.available_piece_moves(piece, True)
            all_moves += board.available_piece_moves(piece, False)
            for move in all_moves:
                board_copy = Board()
                board_copy.copy(board)
                if board_copy.move(piece.position, move, False) is False:
                    continue
                best_score = call(best_score, self.minimax(board_copy, depth - 1, not is_max))
        return best_score'''

    def minimax_with_alphabeta_pruning(self, board, depth, is_max, alpha, beta):
        if depth == 0:
            return evaluate_board(board)
        pieces = board.get_pieces_for_player(ai_player) if is_max else board.get_pieces_for_player(human_player)
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
