#!/usr/bin/python

class GridPosition(object):
	"""Represent a position on a grid."""
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __hash__(self):
		return hash((self.x, self.y))

	def __repr__(self):
		return "GridPosition(%d,%d)" % (self.x, self.y)

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def get_moves(self):
		# There are times when returning this in a shuffled order
		# would help avoid degenerate cases.  For learning, though,
		# life is easier if the algorithm behaves predictably.
		yield GridPosition(self.x + 1, self.y)
		yield GridPosition(self.x, self.y + 1)
		yield GridPosition(self.x - 1, self.y)
		yield GridPosition(self.x, self.y - 1)
