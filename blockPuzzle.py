#!/usr/bin/python

class BlockPuzzle(object):
	def __init__(self, n, xs=None):
		"""Create an nxn block puzzle

		Use XS to initialize to a specific state.
		"""
		self.n = n
		self.n2 = n * n
		if xs is None:
			self.xs = [(x + 1) % self.n2 for x in xrange(self.n2)]
		else:
			self.xs = list(xs)
		self.hsh = None
		self.last_move = []

	def __hash__(self):
		if self.hsh is None:
			self.hsh = hash(tuple(self.xs))
		return self.hsh

	def __repr__(self):
		return "BlockPuzzle(%d, %s)" % (self.n, self.xs)

	def show(self):
		ys = ["%2d" % x for x in self.xs]
		xs = [" ".join(ys[kk:kk+self.n]) for kk in xrange(0,self.n2, self.n)]
		return "\n".join(xs)

	def __eq__(self, other):
		return self.xs == other.xs

	def copy(self):
		return BlockPuzzle(self.n, self.xs)

	def get_moves(self):
		# Find the 0 tile, and then generate any moves we
		# can by sliding another block into its place.
		tile0 = self.xs.index(0)
		def swap(i):
			j = tile0
			tmp = list(self.xs)
			last_move = tmp[i]
			tmp[i], tmp[j] = tmp[j], tmp[i]
			result = BlockPuzzle(self.n, tmp)
			result.last_move = last_move
			return result

		if tile0 - self.n >= 0:
			yield swap(tile0-self.n)
		if tile0 +self.n < self.n2:
			yield swap(tile0+self.n)
		if tile0 % self.n > 0:
			yield swap(tile0-1)
		if tile0 % self.n < self.n-1:
			yield swap(tile0+1)
