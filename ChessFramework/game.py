from Board import Board
from Position import Position
from Piece import Player

board = Board()
board.init_board()
board.display_board()

turn = Player.WHITE

while True:

    # Check check-mate or check and if move doesn't get the king out of check disallow for current player
    # If check-mate, the other one wins
    if not board.is_check_mate(turn):
        from_pos = input("from: ").split()
        to_pos = input("to: ").split()

        from_pos = Position(int(from_pos[0]), int(from_pos[1]))
        to_pos = Position(int(to_pos[0]), int(to_pos[1]))

        if board.get_player_from_pos(from_pos) != turn:
            print('This is the other player turn')
        else:
            correct_move = board.move(from_pos, to_pos)
            board.display_board()

            if correct_move is not None:
                continue

            if turn == Player.WHITE:
                turn = Player.BLACK
            else:
                turn = Player.WHITE
