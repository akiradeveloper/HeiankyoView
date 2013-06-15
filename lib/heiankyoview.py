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
	def __init__(self, x, y, position):
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
		return x - w / 2
	def right(self):
		return x + w / 2
	def up(self):
		return y + h / 2
	def bottom(self):
		return y - h / 2

	def size(self):
		return self.w * self.h

class Table:
	def __init__(self, N, M, value):
		self.matrix = []
		for i in xrange(0, N):
			self.matrix.append([])
			for j in xrange(0, M):
				arr = self.matrix[i]
				arr.append(value)
		self.N = N
		self.M = M
	def set(self, i, j, value):
		self.matrix[i][j] = value
	def get(self, i, j):
		return self.matrix[i][j]
	def backup(self, to):
		for i in xrange(0, self.N):
			for j in xrange(0, self.M):
				to.set(i, j, self.get(i, j))
	def show(self):
		for i in xrange(0, self.N):
			for j in xrange(0, self.M):
				print(i, j)
				print(self.get(i, j))	

class BoolT:
	def __init__(self, N, M):
		self.n = N
		self.m = M
		self.matrix = Table(N, M, False)

	def doubleN(self):
		m = Table(self.matrix.N * 2, self.matrix.M, False)
		self.matrix.backup(m)
		self.matrix = m
	def ensureI(self, addI):		
		if self.n + addI > self.matrix.N:
			self.doubleN()
	def mvI(self, startI, addI):
		# print(startI)
		# print(addI)
		# print(self.n)
		for i in reversed( xrange(startI + addI, self.n) ):
			#print(i)
			for j in xrange(0, self.m):
				# print(self.matrix.get(i - addI, j))
				self.matrix.set(i, j, self.matrix.get(i - addI, j))
				# print(i, j)
				# print(self.matrix.get(i, j))
		for i in xrange(startI, startI + addI):
			for j in xrange(0, self.m):
				self.matrix.set(i, j, False)
	def expandI(self, startI, addI):
		self.ensureI(addI)
		self.n += addI
		self.mvI(startI, addI)

	def doubleM(self):
		m  = Table(self.matrix.N, self.matrix.M * 2, False)
		self.matrix.backup(m)
		self.matrix = m
	def ensureJ(self, addJ):
		if self.m + addJ > self.matrix.M:
			self.doubleM()
	def mvJ(self, startJ, addJ):
		for i in xrange(0, self.n):
			for j in reversed( xrange(startJ + addJ, self.m) ):
				self.matrix.set(i, j, self.matrix.get(i, j - addJ))
				#print(i, j)
				#print(self.matrix.get(i, j))
		for i in xrange(0, self.n):
			for j in xrange(startJ, startJ + addJ):
				self.matrix.set(i, j, False)
	def expandJ(self, startJ, addJ):
		self.ensureJ(addJ)
		self.m += addJ
		self.mvJ(startJ, addJ)

class BoolTable:
	def __init__(self, N, M):
		self.boolT = BoolT(N+2, M+2)
	def adjustI(self, i):
		return i + 1
	def adjustJ(self, j):
		return j + 1

	def get(self, i, j):
		return self.boolT.matrix.get(self.adjustI(i), self.adjustJ(j))
	def set(self, i, j, b):
		self.boolT.matrix.set(self.adjustI(i), self.adjustJ(j), b)
	def n(self):
		return self.boolT.n - 2
	def m(self):
		return self.boolT.m - 2
	def expandI(self, startI, addI):
		self.boolT.expandI(self.adjustI(startI), addI)
	def expandJ(self, startJ, addJ):
		self.boolT.expandJ(self.adjustJ(startJ), addJ)
	def show(self):
		print("show table")
		#self.boolT.matrix.show()
		print(self.n())
		print(self.m())
		for i in xrange(0, self.n()):
			for j in xrange(0, self.m()):
				# print(j)
				print(i, j)
				print(self.get(i, j))	

class BinarySearch:
	NOT_FOUND = -1
	def binarySearch(self, L, x, left, right):
		if right < left:
			return self.NOT_FOUND

		mid = (left + right) / 2
		if x > L[mid]:
			return self.binarySearch(L, x, mid + 1, right)
		elif x < L[mid]:
			return self.binarySearch(L, x, left, mid - 1)
		else:
			return mid

	def search(self, L, x):
		left = 0
		right = len(L) - 1
		return self.binarySearch(L, x, left, right)

def binSearch(L, x):
	bs = BinarySearch()
	return bs.search(L, x)

class Coordinate:
	def __init__(self, minLine, maxLine):
		self.L = [minLine, maxLine]
	def size(self):
		return self.L.size()
	def indexOf(self, line):
		return binSearch(self.L, line)
	def minLine(self):
		return self.L[0]
	def maxLine(self):
		return self.L[self.L.size() - 1]
	def width(self):
		return self.maxLine() - self.minLine()

class Placement:
	def __init__(self, left, right, bottom, top):	
		self.left = left
		self.right = right
		self.bottom = bottom
		self.top = top

	def x(self):
		return (self.right - self.left) / 2
	def y(self):
		return (self.top - self.bottom) / 2

class PackingGrid:
	def __init__(self, left, right, bottom, top):
		self.xCoord = Coordinate(left, right)
		self.yCoord = Coordinate(bottom, top)
		self.boolT = BoolTable(1, 1)
		self.candidates = []

	def center(self):
		x = self.xCoord.minLine() + self.xCoord.width() / 2
		y = self.yCoord.minLine() + self.yCoord.width() / 2
		return (x, y)

	def updateBoolT(self, iGridMin, iGridMax, jGridMin, jGridMax):
		for i in xrange(iGridMin, iGridMax + 1):
			for j in xrange(jGridMin, jGridMax + 1):
				self.boolT.set(i, j, True)

	def getGridIndex(self, i, j, position):
		m = { 
			CornerPosition.RIGHT_UP   : (i, j),	
			CornerPosition.RIGHT_DOWN : (i, j - 1),
			CornerPosition.LEFT_UP    : (i - 1, j),
			CornerPosition.LEFT_DOWN  : (i - 1, j - 1),
		}
		return m[position]

	def getCornerType(self, i, j, checkCorner, adjacentCorner):
		ic, jc = self.getGridIndex(i, j, checkCorner)
		ia, ja = self.getGridIndex(i, j, adjacentCorner)

		if self.isOccupied(ic, jc):
			cornerType = CornerType.OCCUPIED
		else:
			if self.isOccupied(ia, ja):
				cornerType = CornerType.ADJACENT
			else:
				cornerType = CornerType.FREE

		return cornerType

	def plac(self, i, j, position, newXLine, newYLine):
		def addNewXLine(newXLine):
			pass
		def addNewYLine(newYLine):
			pass

		bx = not newXLine in self.xCoord
		if bx:
			addNewXLine(newXLine)	
		by = not newYLine in self.yCoord
		if by:
			addNewYLine(newYLine)		

		newXLineIndex = self.xCoord.indexOf(newXLine)
		newYLineIndex = self.yCoord.indexOf(newYLine)

		addI = 1 if bx else 0
		addJ = 1 if by else 0

		#TODO

		self.collectCandidate(iLeft, iRight, jBottom, jTop, position)
		self.updateBoolT(iLeft, iRight - 1, jBottom, jTop - 1)

	def getPlacement(self, x, y, position, w, h):
		r = None
		if position == CornerPosition.RIGHT_UP:
			r = Placement(x, x+w, y, y+h)
		if position == CornerPosition.RIGHT_DOWN:
			r = Placement(x, x+w, y-h, y)
		if position == CornerPosition.LEFT_UP:
			r = Placement(x-w, x, y, y+h)
		if position == CornerPosition.LEFT_DOWN:		
			r = Placement(x-w, x, y-h, y)
		return r

	def tryPlacement(self, x, y, position, w, h):
		pm = self.getPlacement(x, y, position, w, h)
		left   = min(pm.left, self.xCoord.minLine())
		right  = max(pm.right, self.xCoord.maxLine())
		bottom = min(pm.bottom, self.yCoord.minLine())
		top    = max(pm.top, self.yCoord.maxLine())
		return (right-left, top-bottom)

	def place(self, i, j, position, w, h):
		x = self.xCoord[i]
		y = self.yCoord[j]
		pm = self.getPlacement(x, y, position, w, h)
		if position == CornerPosition.RIGHT_UP:
			self.plac(i, j, position, pm.right, pm.top)
		if position == CornerPosition.RIGHT_DOWN:
			self.plac(i, j, position, pm.right, pm.bottom)
		if position == CornerPosition.LEFT_UP:
			self.plac(i, j, position, pm.left, pm.top)
		if position == CornerPosition.LEFT_DOWN:		
			self.plac(i, j, position, pm.left, pm.bottom)

class RectanglePacking:
	def __init__(self):
		self.grid = None
		pass

	def evaluatePlacement(w, h):
		aspectRatio = max( w/h, h/w )
		size = w * h
		return size * aspectRatio

	def addAnother(self, rect):

		bestEval = float("inf")

		for i in reversed(xrange(0, self.grid.candidates.size())):
			candidate = self.grid.candidates[i]
			decisionIdx = i

			gridIdx = self.grid.getGridIndex(
					candidate.x,
					candidate.y,
					candidate.position)
	
			if self.grid.isOccupied(gridIdx[0], gridIdx[1]):
				self.grid.candidates.pop(i)
				continue

			if self.intersects(x, y, position, rect.w, rect.h):
				#self.grid.candidates.pop(i)
				continue

			tryW, tryH = self.grid.tryPlacement(x, y, position, rect.w, rect.h)
			tryEval = self.evaluatePlacement(tryW, tryH)

			currentsize = self.xCoord.width() * self.yCoord.width()
			if (tryW * tryH) <= currentsize:
				bestEval = tryEval
				decision = candidate
				break

			if tryEval < bestEval:
				bestEval = tryEval
				decision = candidate

		decisionOutside = False


		leftDownCorner = (
				self.grid.xCoord.minLine(),
				self.grid.yCoord.minLine())
		tryW1, tryH1 = self.grid.tryPlacement(leftDownCorner[0], leftDownCorner[1], CornerPosition.RIGHT_DOWN)
		tryEval1 = self.evaluatePlacement(tryW1, tryH1)
		if tryEval1 < bestEval:
			bestEval = tryEval1
			decision = Candidate(leftDownCorner[0], leftDownCorner[1], CornerPosition.RIGHT_DOWN)
			decisionOutside = True


		rightUpCorner = (
				self.grid.xCoord.maxLine(),
				self.grid.yCoord.maxLine())
		tryW2, tryH2 = self.grid.tryPlacement(rightUpCorner[0], rightUpCorner[1], CornerPosition.RIGHT_DOWN)
		tryEval2 = self.evaluatePlacement(tryW2, tryH2)
		if tryEval2 < bestEval:
			bestEval = tryEval2
			decision = Candidate(rightUpCorner[0], rightUpCorner[1], CornerPosition.RIGHT_DOWN)
			decisionOutside = True

		pm = self.grid.getPlacement(
				decision.x,
				decision.y,
				decision.position,
				rect.w,
				rect.h)
			
		self.grid.place(
				self.grid.xCoord.indexOf(decision.x),
				self.grid.yCoord.indexOf(decision.y),
				decision.position,
				rect.w,
				rect.h)

		if not decisionOutside:
			self.grid.candidates.pop(decisionIdx)

		rect.x = pm.x()
		rect.y = pm.y()

	def add(self, rect):
		if not self.grid:
			self.grid = PackingGrid(0, rect.w, 0, rect.h)
			return
		self.addAnother(rect)

def BFS(tree):
	L1 = []
	L2 = []
	L1.append(tree.getRoot())	
	while L1:
		id = L1.pop()
		L2.append(id)
		for child in tree.getChildren(id):
			L1.append(child)
	return L2

class TreePacking:
	def __init__(self, tree):
		self.tree = tree

	def pack(self):
		L = BFS(self.tree)
		L = filter(lambda id: not self.tree.isLeaf(id), L)
		for branch in reversed(L):
			packer = RectanglePacking()
			rects = [self.tree.getRect(child) for child in self.tree.children(branch)]

			def f(r1, r2):
				return r2.size() - r1.size()
			for rect in sorted(rects, cmp=f):
				packer.add(rect)

			r = self.tree.getRect(branch)
			r.x, r.y = packer.grid.center()
			r.w, r.h = packer.grid.xCoord.width(), packer.grid.yCoord.width()

class Graph:
	def __init__(self):
		self.nodes = {}
		self.children = {}
		self.root = None

	def isLeaf(self, id):
		return not id in self.children

	def addNode(self, id):
		if id in self.nodes:
			return
		if not self.root:
			self.root = id
		r = Rectangle()
		self.nodes[id] = r

	def getRect(self, id):
		if not id in self.nodes:
			return None
		return self.nodes[id]
	
	def getChildren(self, id):
		if self.isLeaf(id):
			return []
		return self.children[id]

	def addChild(self, parent, child):
		if not parent in self.children:
			self.children[parent] = []
		self.children[parent].append(child)
		if child == self.root:
			self.root = parent

	def getRoot(self):
		return self.root

if __name__ ==  '__main__':
	pass
