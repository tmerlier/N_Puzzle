#!/usr/bin/python
import subprocess
import random
import argparse
import pprint
import time

import heapq
import math
import random

from puzzle import Puzzle

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

def solve(start, finish, heuristic):
	"""Find the shortest path from START to FINISH."""
	heap = []

	link = {} # parent node link
	h = {} # heuristic function cache
	g = {} # shortest path to a node

	g[start] = 0
	h[start] = 0
	link[start] = None


	heapq.heappush(heap, (0, 0, start))
	# keep a count of the  number of steps, and avoid an infinite loop.
	for kk in xrange(10000000):
		f, junk, current = heapq.heappop(heap)
		if current == finish:
			print "distance:", g[current], "steps:", kk
			return g[current], kk, build_path(start, finish, link)

		moves = current.get_moves()
		distance = g[current]
		for mv in moves:
			if mv not in g or g[mv] > distance + 1:
				g[mv] = distance + 1
				if mv not in h:
					h[mv] = heuristic(mv)
				link[mv] = current
				heapq.heappush(heap, (g[mv] + h[mv], -kk, mv))
	else:
		raise Exception("did not find a solution")

def build_path(start, finish, parent):
	"""
	Reconstruct the path from start to finish given
	a dict of parent links.

	"""
	x = finish
	xs = [x]
	while x != start:
		x = parent[x]
		xs.append(x)
	xs.reverse()
	return xs

def manhattan_h(goal):
	def f(pos):
		dx, dy = pos.x - goal.x, pos.y - goal.y
		return abs(dx) + abs(dy)
	return f

def distance_h(position):
	n = position.n
	def row(x): return x / n
	def col(x): return x % n
	score = 0
	for idx, x in enumerate(position.xs):
		if x == 0: continue
		ir,ic = row(idx), col(idx)
		xr,xc = row(x-1), col(x-1)
		score += abs(ir-xr) + abs(ic-xc)
	return score











if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument("size", type=int, help="Size of the puzzle's side. Must be >3.")

	args = parser.parse_args()

cmd = "python puzzle_generator.py " + str(args.size)
proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()

print out
out = out.strip()
data = out.split('\n')

puzzle = Puzzle(data)

print ''
print 'Comment:', puzzle.comment
print ''
print 'Puzzle:', puzzle.list
print ''
print 'Solution:', puzzle.solution


start = BlockPuzzle(puzzle.size, puzzle.list)
end = BlockPuzzle(puzzle.size, puzzle.solution)
x = solve(start, end, distance_h)

i = 0
for puzzle in x[2]:
	i += 1
	print 'move:', i
	print puzzle.show()
	print ''

