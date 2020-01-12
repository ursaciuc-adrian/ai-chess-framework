from Board import Board
from Position import Position
from Piece import Player
import Strategies


class PvAI_Game(Board):
    def __init__(self, board: Board, ai_strategy):
        self.board = board
        self.board.init_board()

        self.strategy = ai_strategy

    def play(self):
        self.board.display_board()

        turn = Player.WHITE

        Strategies.set_AI(Player.BLACK, Player.WHITE)

        while True:

            # Check check-mate or check and if move doesn't get the king out of check disallow for current player
            # If check-mate, the other one wins
            if not self.board.is_check_mate(turn):
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


class PvP_Game:
    def __init__(self, board):
        self.board = board
        self.board.init_board()

    def play(self):
        self.board.display_board()

        turn = Player.WHITE

        while True:

            # Check check-mate or check and if move doesn't get the king out of check disallow for current player
            # If check-mate, the other one wins
            if not self.board.is_check_mate(turn):
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


if __name__ == '__main__':
    # game = PvAI_Game(Board(), Strategies.Minimax(3))
    game = PvP_Game(Board())
    game.play()
