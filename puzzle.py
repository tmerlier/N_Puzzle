#!/usr/bin/python
import pprint

class Puzzle(object):
	"""docstring for Puzzle"""
	def __init__(self, data):
		super(Puzzle, self).__init__()
		self.comment = data[0]
		if "unsolvable" in self.comment:
			raise Exception(self.comment)
		self.size = int(data[1])
		self.puzzle = self.getPuzzle(data)
		self.list = self.getPuzzleLst(self.puzzle)

		self.snail = self.checkSnail()
		self.solution = self.getSolution()

	def __repr__(self):
		return "%s\nPuzzle(%d, %s)" % (self.comment, self.size, self.list)


	def getPuzzleLst(self, data):
		lst = []
		for line in data:
			for coln in line:
				lst.append(coln)
		return lst

	def getPuzzle(self, data):
		puzzle = []
		for x in xrange(2, len(data)):
			line = data[x].split(' ')
			tab = []
			for number in line:
				if number != '':
					tab.append(int(number))
			puzzle.append(tab)
		return puzzle

	def getSolution(self):
		solucList = sorted(self.list, key=int)
		solucList.pop(0)
		solucList.append(0)

		firstTurn = True
		x = 0
		y = 0
		diff = 0
		index = self.size - 1
		list = self.puzzle
		while index > 0:
			index = index - diff

			if firstTurn == True:
				list[x][y] = solucList.pop(0)
				firstTurn = False

			while y < index:
				y += 1
				list[x][y] = solucList.pop(0)

			while x < index:
				x += 1
				list[x][y] = solucList.pop(0)

			index = index - diff

			while y > diff:
				y -= 1
				list[x][y] = solucList.pop(0)

			diff += 1

			while x > diff:
				x -= 1
				list[x][y] = solucList.pop(0)

		res = []
		for line in list:
			for coln in line:
				res.append(coln)
		return res

	def addNumber(self, list, number):
		if number not in list:
			list.append(number)
		return list

	def checkSnail(self):
		x = 0
		y = 0
		diff = 0
		index = self.size - 1
		list = []
		while index > 0:
			index = index - diff

			list = self.addNumber(list, self.puzzle[x][y])
			while y < index:
				y += 1
				list = self.addNumber(list, self.puzzle[x][y])

			while x < index:
				x += 1
				list = self.addNumber(list, self.puzzle[x][y])

			index = index - diff

			while y > diff:
				y -= 1
				list = self.addNumber(list, self.puzzle[x][y])

			diff += 1

			while x > diff:
				x -= 1
				list = self.addNumber(list, self.puzzle[x][y])
		return list

