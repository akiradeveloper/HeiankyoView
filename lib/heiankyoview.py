class CornerType:
	OCCUPIED = 0
	ADJACENT = 1
	FREE     = 2

class CornerPosition:
	LEFT_UP    = 0
	LEFT_DOWN  = 1
	RIGHT_UP   = 2
	RIGHT_DOWN = 3

class Candidate:
	def __init__(x, y, position):
		self.x = x
		self.y = y
		self.position = position

class Rectangle:

	def __init__(self):
		self.x = 0
		self.y = 0
		self.w = 0
		self.h = 0

	def left(self):		
		return x - w
	def right(self):
		return x + w
	def up(self):
		return y + h
	def bottom(self):
		return y - h

class Table:
	def __self__(self, N, M, value):
		self.matrix = []
		for i in N:
			self.matrix.append([])
			for j in M:
				arr = self.matrix[i]
				arr.append(value)
	def set(self, i, j, value):
		self.matrix[i][j] = value
	def get(self, i, j):
		return self.matrix[i][j]
	def doubleN(self):
		pass
	def doubleM(self):
		pass

class BoolT:
	def __self__(self, N, M):
		self.n = N
		self.m = M
		self.matrix = Table(N, M, False)
	def expandN(startI, addI):
		ensureN(addI)
		self.n += addI
		mvN(startI, addI)
	def mvN(startI, addI):
		pass
	def expandM(startJ, addJ):
		pass
	def mvM(startJ, addJ):
		pass

class BoolTable:
	def __self__(self, N, M):
		self.boolT = BoolT(N+2, M+2)
	def adjustI(i):
		return i + 1
	def adjustJ(j):
		return j + 1
	def get(i, j):
		pass
	def set(i, j, b):
		pass
	def n():
		return self.boolT.n - 2
	def m():
		pass
	def expandN(startI, addI):
		self.boolT.expandN(adjustI(startI), addI)
	def expandM(startJ, addJ):
		pass

class Coordinate:
	def __init__(self, minLine, maxLine):
		self.L = [minLine, maxLine]
	def size(self):
		self.L.size()
	def indexOf(line):
		return binSearch(self.L, line)
	def minLine(self):
		return self.L[0]
	def maxLine(self):
		return self.L[self.L.size() - 1]

class PackingGrid:
	def __init__(self):
		self.xCoord = Coordinate()
		self.yCoord = Coordinate()
		self.boolT = BoolTable()
	
class LightPackingGrid:
	def __init__(self):
		self.grid = PackingGrid()
		self.candidates = []

class RectanglePacking:
	def __init__(self):
		self.lgrid = LightPackingGrid()
		pass

	def add(self, rect):
		pass

class TreePacking:
	def __init__(self, tree):
		self.tree = tree

	def listBFS(self):
		L1 = []
		L2 = []
		L1.append(self.tree.getRoot())	
		while not L1:
			L2.append(L1.pop())
			for child in self.tree.children(id):
				L1.append(child)
		return L2

	def pack(self):
		L = self.listBFS()
		L = filter(lambda id: not self.tree.isLeaf(id), L)
		L.reverse()
		for branch in L:
			packer = RectanglePacking()
			for child in self.tree.children(branch):
				packer.add(self.tree.getRect(child)

			outline = packer.grid.outline()

			r = self.tree.getRect(branch)
			# set r
		
	def translate(x, y):
		pass

	def shrinkBy(length):
		pass

class Graph:
	def __init__(self):
		nodes = {}
		children = {}

	def isLeaf(self, id):
		pass

	def addNode(self, id):
		if id in nodes:
			return
		r = Rectangle()
		nodes[id] = r

	def getRect(self, id):
		if not id in nodes:
			return None
		return nodes[id]
	
	def children(self, id):
		return children[id]

	def addChild(self, parent, child):
		if not parent in edges:
			children[parent] = []
		children[parent].append(child)

	def getRoot(self):
		pass

if __name__ ==  '__main__':
	pass
