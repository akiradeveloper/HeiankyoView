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
		return x - w / 2
	def right(self):
		return x + w / 2
	def up(self):
		return y + h / 2
	def bottom(self):
		return y - h / 2

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
		self.boolT = BoolTable()
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
		by = not newYLine in self.xCoord
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
		pm = getPlacement(x, y, position, w, h)
		left   = min(pm.left, self.xCoord.minLine())
		right  = max(pm.right, self.xCoord.maxLine())
		bottom = min(pm.bottom, self.yCoord.minLine())
		top    = max(pm.top, self.yCoord.maxLine())
		return (right-left, top-bottom)

	def place(self, i, j, position, w, h):
		x = self.xCoord[i]
		y = self.yCoord[j]
		pm = getPlacement(x, y, position, w, h)
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

	def _add(self, rect):

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
			self.grid = PackingGrid()
			return
		self._add(rect)

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
			#TODO set r

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
