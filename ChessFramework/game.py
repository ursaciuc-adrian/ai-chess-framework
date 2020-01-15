from Board import Board
from Position import Position
from Piece import Player
import Strategies
from copy import deepcopy

class PvAI_Game:
    def __init__(self, board: Board, ai_strategy):
        self.board = board
        self.board.init_board()

        self.strategy = ai_strategy

    def play(self):
        self.board.display_board()

        turn = Player.WHITE

        while True:
            if not self.board.is_check_mate(turn) and not self.board.is_draw():
                if turn == Player.BLACK:
                    ai_move = self.strategy.take_decision(self.board)
                    self.board.move(ai_move[0], ai_move[1])
                    self.board.display_board()
                    turn = Player.WHITE
                    continue

                from_pos = input("from: ").split()
                to_pos = input("to: ").split()

                correct_input = False
                while not correct_input:
                    try:
                        from_pos = Position(int(from_pos[0]), int(from_pos[1]))
                        to_pos = Position(int(to_pos[0]), int(to_pos[1]))
                        correct_input = True
                    except:
                        print('An input pair should look like this: "1 0", where x = 1, y = 0.')
                        correct_input = False

                if self.board.get_player_from_pos(from_pos) != turn:
                    print('This is the other player turn')
                else:
                    correct_move = self.board.move(from_pos, to_pos)
                    self.board.display_board()

                    if correct_move is not None:
                        continue

                    if turn == Player.WHITE:
                        turn = Player.BLACK
                    else:
                        turn = Player.WHITE
            if self.board.is_draw():
                print("It's a draw.")
                break


class PvP_Game:
    def __init__(self, board):
        self.board = board
        self.board.init_board()

    def play(self):
        self.board.display_board()

        turn = Player.WHITE

        while True:
            if not self.board.is_check_mate(turn) and not self.board.is_draw():
                from_pos = input("from: ").split()
                to_pos = input("to: ").split()

                correct_input = False
                while not correct_input:
                    try:
                        from_pos = Position(int(from_pos[0]), int(from_pos[1]))
                        to_pos = Position(int(to_pos[0]), int(to_pos[1]))
                        correct_input = True
                    except:
                        print('An input pair should look like this: "1 0", where x = 1, y = 0.')
                        correct_input = False

                if self.board.get_player_from_pos(from_pos) != turn:
                    print('This is the other player turn')
                else:
                    correct_move = self.board.move(from_pos, to_pos)
                    self.board.display_board()

                    if correct_move is not None:
                        continue

                    if turn == Player.WHITE:
                        turn = Player.BLACK
                    else:
                        turn = Player.WHITE
            if self.board.is_draw():
                print("It's a draw.")
                break


class AIvAI_Game:
    def __init__(self, board: Board, ai_strategy1, ai_strategy2):
        self.board = board
        self.board.init_board()

        self.strategy1 = ai_strategy1
        self.strategy2 = ai_strategy2

    def play(self):
        self.board.display_board()

        turn = Player.WHITE

        while True:
            if not self.board.is_check_mate(turn) and not self.board.is_draw('all'):
                copy = deepcopy(self.board)
                if turn == Player.BLACK:
                    ai_move = self.strategy1.take_decision(copy)
                    if self.board.move(ai_move[0], ai_move[1]) is False:
                        return
                    self.board.display_board()
                    turn = Player.WHITE
                    continue
                elif turn == Player.WHITE:
                    ai_move = self.strategy2.take_decision(copy)
                    if self.board.move(ai_move[0], ai_move[1]) is False:
                        return
                    self.board.display_board()
                    turn = Player.BLACK
                    continue
            if self.board.is_draw('all'):
                print("It's a draw.")
                break


if __name__ == '__main__':
    # game = PvAI_Game(Board(), Strategies.Minimax(2, Player.BLACK, Player.WHITE))
    # game = PvAI_Game(Board(), Strategies.MinimaxRandomSample(3, 5, 5))
    # game = PvP_Game(Board())
    # game = AIvAI_Game(Board(), Strategies.MinimaxRandomSample(Player.BLACK, Player.WHITE, 3, 5, 5), Strategies.MinimaxRandomSample(Player.WHITE, Player.BLACK, 3, 5, 5))
    game = AIvAI_Game(Board(), Strategies.Minimax(2, Player.BLACK, Player.WHITE),
                      Strategies.Minimax(2, Player.WHITE, Player.BLACK))
    game.play()
