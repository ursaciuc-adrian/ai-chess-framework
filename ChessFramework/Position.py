class Position(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def is_in_boundary(self, b):
		if self.x < 0 or self.y < 0 or self.x >= b or self.y >= b:
			return False
		return True

	def __eq__(self, obj):
		return isinstance(obj, Position) and  self.x == obj.x and self.y == obj.y

	def __str__(self):
		return f"({self.x}, {self.y})"