from Position import Position

class Guard:
	@staticmethod
	def check_position(position: Position, size):
		if not position.is_in_boundary(size):
			raise Exception("Invalid position. " + str(position))
