from Board import Board
from Position import Position

board = Board()
board.init_board()

board.display_board()

while True:
	from_pos = input("from: ").split()
	to_pos = input("to: ").split()

	from_pos = Position(int(from_pos[0]), int(from_pos[1]))
	to_pos = Position(int(to_pos[0]), int(to_pos[1]))

	board.move(from_pos, to_pos)
	board.display_board()
