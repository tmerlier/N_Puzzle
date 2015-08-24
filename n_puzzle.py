#!/usr/bin/python
import subprocess
import random
import argparse

import heapq
import math

from puzzle import Puzzle
from blockPuzzle import BlockPuzzle


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

