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
	def show(self):
		print( (self.x, self.y, self.position) )

class Rectangle:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.w = 0
		self.h = 0
	def show(self):		
		print(self.x, self.y, self.w, self.h)
	def left(self):		
		return x - 0.5 * w
	def right(self):
		return x + 0.5 * w 
	def up(self):
		return y + 0.5 * h
	def bottom(self):
		return y - 0.5 * h
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

	def copyI(self, src, dest):
		for j in xrange(0, self.m):
			self.matrix.set(dest, j, self.matrix.get(src, j))
	def copyJ(self, src, dest):
		for i in xrange(0, self.n):
			self.matrix.set(i, dest, self.matrix.get(i, src))

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
			self.copyI(i - addI, i)
			#print(i)
			#for j in xrange(0, self.m):
				# print(self.matrix.get(i - addI, j))
				#self.matrix.set(i, j, self.matrix.get(i - addI, j))
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
		#for i in xrange(0, self.n):
		for j in reversed( xrange(startJ + addJ, self.m) ):
				#self.matrix.set(i, j, self.matrix.get(i, j - addJ))
			self.copyJ(j - addJ, j)
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
	def copyI(self, src, dest):
		self.boolT.copyI(self.adjustI(src), self.adjustI(dest))
	def copyJ(self, src, dest):
		self.boolT.copyJ(self.adjustJ(src), self.adjustJ(dest))

class BinarySearch:
	def binarySearch(self, L, x, left, right):
		if right < left:
			return -1

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
	def get(self, i):
		return self.L[i]
	def insert(self, i, line):
		self.L.insert(i, line)
	def size(self):
		return len(self.L)
	def indexOf(self, line):
		return binSearch(self.L, line)
	def has(self, line):
		return self.indexOf(line) != -1
	def minLine(self):
		return self.L[0]
	def maxLine(self):
		return self.L[len(self.L) - 1]
	def width(self):
		return self.maxLine() - self.minLine()

	def getRightIntersection(self, i, line):
		for j in xrange(i+1, self.size()):
			upper = self.L[j]
			if line <= upper:
				return (i, j-1)
		return (i, self.size()-1)	

	def getLeftIntersection(self, i, line):
		for j in reversed(xrange(0, i)):
			lower = self.L[j]
			if line >= lower:
				return (j, i-1)
		return (-1, i-1)
	def show(self):
		print(self.L)

class Placement:
	def __init__(self, left, right, bottom, top):	
		self.left = left
		self.right = right
		self.bottom = bottom
		self.top = top

	def x(self):
		return self.left + 0.5 * (self.right - self.left) 
	def y(self):
		return self.bottom + 0.5 * (self.top - self.bottom) 
	def show(self):
		print( (self.left, self.right, self.bottom, self.top) )

class PackingGrid:
	def __init__(self, left, right, bottom, top):
		self.xCoord = Coordinate(left, right)
		self.yCoord = Coordinate(bottom, top)
		self.boolT = BoolTable(1, 1)
		self.boolT.set(0, 0, True)
		self.candidates = []

	def isOccupied(self, i, j):
		return self.boolT.get(i, j)

	def center(self):
		x = self.xCoord.minLine() + 0.5 * self.xCoord.width()
		y = self.yCoord.minLine() + 0.5 * self.yCoord.width()
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

	def getCornerType(self, i, j, base, target):
		i1, j1 = self.getGridIndex(i, j, base)
		i2, j2 = self.getGridIndex(i, j, target)

		if self.isOccupied(i2, j2):
			cornerType = CornerType.OCCUPIED
		else:
			if self.isOccupied(i1, j1):
				cornerType = CornerType.ADJACENT
			else:
				cornerType = CornerType.FREE
		return cornerType

	def collectCandidates(self, iLeft, iRight, jBottom, jTop, position):
		print("collect")
		def OneSide(i, j, base, target):
			if self.getCornerType(i, j, base, target) == CornerType.ADJACENT:
				print(i, j)
				self.xCoord.show()
				self.yCoord.show()
				c = Candidate(
						self.xCoord.get(i), 
						self.yCoord.get(j),
						target)
				c.show()
				self.candidates.append(c)
		def Vertical(i, start, end, lowerPos, upperPos):
			OneSide(i, start, lowerPos, upperPos)
			for j in xrange(start+1, end):
				OneSide(i, j, lowerPos, upperPos)
				OneSide(i, j, upperPos, lowerPos)
			OneSide(i, end, upperPos, lowerPos)
		def HorizonTal(j, start, end, leftPos, rightPos):
			OneSide(start, j, leftPos, rightPos)
			for i in xrange(start+1, end):
				OneSide(i, j, leftPos, rightPos)
				OneSide(i, j, rightPos, leftPos)
			OneSide(end, j, rightPos, leftPos)
		def Left():
			Vertical(iLeft, jBottom, jTop, CornerPosition.LEFT_DOWN, CornerPosition.LEFT_UP)
		def Right():
			Vertical(iRight, jBottom, jTop, CornerPosition.RIGHT_DOWN, CornerPosition.RIGHT_UP)
		def Bottom():
			HorizonTal(jBottom, iLeft, iRight, CornerPosition.LEFT_DOWN, CornerPosition.RIGHT_DOWN)
		def Upper():
			HorizonTal(jTop, iLeft, iRight, CornerPosition.LEFT_UP, CornerPosition.RIGHT_UP)

		Left()
		Right()
		Bottom()
		Upper()

	def calcIntersectableRegion(self, x, y, position, w, h):
		I = self.xCoord.indexOf(x)
		J = self.yCoord.indexOf(y)

		def ru():
			_, a = self.xCoord.getRightIntersection(I, x + w)
			_, b = self.yCoord.getRightIntersection(J, y + h)
			return (I, a, J, b)
		def rd():
			_, a = self.xCoord.getRightIntersection(I, x + w)
			b, _ = self.yCoord.getLeftIntersection(J, y - h)
			return (I, a, b, J-1)
		def lu():
			a, _ = self.xCoord.getLeftIntersection(I, x - w)
			_, b = self.yCoord.getRightIntersection(J, y + h)
			return (a, I-1, J, b)
		def ld():
			a, _ = self.xCoord.getLeftIntersection(I, x - w)
			b, _ = self.yCoord.getLeftIntersection(J, y - h)
			return (a, I-1, b, J-1)
		
		m = {
				CornerPosition.RIGHT_UP   : ru(),
				CornerPosition.RIGHT_DOWN : rd(),
				CornerPosition.LEFT_UP    : lu(),
				CornerPosition.LEFT_DOWN  : ld(),
		}
		return m[position]

	def intersects(self, x, y, position, w, h):
		iLeft, iRight, jBottom, jTop = self.calcIntersectableRegion(x, y, position, w, h)
		for i in xrange(iLeft, iRight + 1):
			for j in xrange(jBottom, jTop + 1):
				if self.isOccupied(i, j):
					return True
		return False

	def plac(self, x, y, position, newXLine, newYLine):
		w = abs(newXLine - x)
		h = abs(newYLine - y)

		iL, iR, jB, jT = self.calcIntersectableRegion(x, y, position, w, h)
		m = {
				CornerPosition.RIGHT_UP   : (iR + 1, jT + 1),
				CornerPosition.RIGHT_DOWN : (iR + 1, jB + 1),
				CornerPosition.LEFT_UP    : (iL + 1, jT + 1),
				CornerPosition.LEFT_DOWN  : (iL + 1, jB + 1),
		}
		I, J = m[position]

		if not self.xCoord.has(newXLine):
			print("new xline")
			mid = self.xCoord.minLine() < newXLine < self.xCoord.maxLine()
			self.xCoord.insert(I, newXLine)
			self.boolT.expandI(I, 1)
			if mid:
				self.boolT.copyI(I-1, I)

		if not self.yCoord.has(newYLine):
			print("new yline")
			mid = self.yCoord.minLine() < newYLine < self.yCoord.maxLine()
			self.yCoord.insert(J, newYLine)
			self.boolT.expandJ(J, 1)
			if mid:
				self.boolT.copyJ(J-1, J)

		iLeft, iRight, jBottom, jTop = self.calcIntersectableRegion(x, y, position, w, h)
		print("inter region")
		print(iLeft, iRight, jBottom, jTop)
		self.updateBoolT(iLeft, iRight, jBottom, jTop)
		self.boolT.show()
		self.collectCandidates(iLeft, iRight + 1, jBottom, jTop + 1, position)

	def getPlacement(self, x, y, position, w, h):
		r = None
		if position == CornerPosition.RIGHT_UP:
			r = Placement(x, x + w, y, y + h)
		if position == CornerPosition.RIGHT_DOWN:
			r = Placement(x, x + w, y - h, y)
		if position == CornerPosition.LEFT_UP:
			r = Placement(x - w, x, y, y + h)
		if position == CornerPosition.LEFT_DOWN:		
			r = Placement(x - w, x, y - h, y)
		return r

	def tryPlacement(self, x, y, position, w, h):
		pm = self.getPlacement(x, y, position, w, h)
		left   = min(pm.left, self.xCoord.minLine())
		right  = max(pm.right, self.xCoord.maxLine())
		bottom = min(pm.bottom, self.yCoord.minLine())
		top    = max(pm.top, self.yCoord.maxLine())
		return (right-left, top-bottom)

	def place(self, x, y, position, w, h):
		pm = self.getPlacement(x, y, position, w, h)
		pm.show()
		if position == CornerPosition.RIGHT_UP:
			self.plac(x, y, position, pm.right, pm.top)
		elif position == CornerPosition.RIGHT_DOWN:
			self.plac(x, y, position, pm.right, pm.bottom)
		elif position == CornerPosition.LEFT_UP:
			self.plac(x, y, position, pm.left, pm.top)
		elif position == CornerPosition.LEFT_DOWN:		
			self.plac(x, y, position, pm.left, pm.bottom)
		else:
			raise RuntimeError

class RectanglePacking:
	def __init__(self):
		self.grid = None

	def evaluatePlacement(self, w, h):
		aspectRatio = max( float(w)/h, float(h)/w )
		size = w * h
		return size * aspectRatio

	def addAnother(self, rect):
		bestEval = float("inf")

		for i in reversed(xrange(0, len(self.grid.candidates))):
			print("candidate")
			candidate = self.grid.candidates[i]
			decisionIdx = i

			candidate.show()
			X = candidate.x
			Y = candidate.y
			P = candidate.position

			gridIdx = self.grid.getGridIndex(X, Y, P)
	
			if self.grid.isOccupied(gridIdx[0], gridIdx[1]):
				self.grid.candidates.pop(i)
				continue

			if self.grid.intersects(X, Y, P, rect.w, rect.h):
				#self.grid.candidates.pop(i)
				continue

			tryW, tryH = self.grid.tryPlacement(X, Y, P, rect.w, rect.h)
			tryEval = self.evaluatePlacement(tryW, tryH)

			currentsize = self.grid.xCoord.width() * self.grid.yCoord.width()
			if (tryW * tryH) <= currentsize:
				print("size not change! tryEval % f" % tryEval)
				bestEval = tryEval
				decision = candidate
				break

			if tryEval < bestEval:
				print("size changed by candidate placed. tryEval %f" % tryEval)
				bestEval = tryEval
				decision = candidate

		decisionOutside = False

		leftDownCorner = (
				self.grid.xCoord.minLine(),
				self.grid.yCoord.minLine())
		tryW1, tryH1 = self.grid.tryPlacement(leftDownCorner[0], leftDownCorner[1], CornerPosition.RIGHT_DOWN, rect.w, rect.h)
		tryEval1 = self.evaluatePlacement(tryW1, tryH1)
		print("tryEval1 % f" % tryEval1)
		if tryEval1 < bestEval:
			print("choose outside candidate 1")
			bestEval = tryEval1
			decision = Candidate(leftDownCorner[0], leftDownCorner[1], CornerPosition.RIGHT_DOWN)
			decisionOutside = True

		rightUpCorner = (
				self.grid.xCoord.maxLine(),
				self.grid.yCoord.maxLine())
		tryW2, tryH2 = self.grid.tryPlacement(rightUpCorner[0], rightUpCorner[1], CornerPosition.RIGHT_DOWN, rect.w, rect.h)
		tryEval2 = self.evaluatePlacement(tryW2, tryH2)
		print("tryEval2 %f" % tryEval2)
		if tryEval2 < bestEval:
			print("choose outside candidate 2")
			bestEval = tryEval2
			decision = Candidate(rightUpCorner[0], rightUpCorner[1], CornerPosition.RIGHT_DOWN)
			decisionOutside = True

		pm = self.grid.getPlacement(
				decision.x,
				decision.y,
				decision.position,
				rect.w,
				rect.h)
		# pm.show()
			
		print("place")
		self.grid.place(
				decision.x,
				decision.y,
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
			rect.x = 0.5 * rect.w
			rect.y = 0.5 * rect.h
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

		#TODO set leafsize to 8*8

		for branch in reversed(L):
			packer = RectanglePacking()
			rects = [self.tree.getRect(child) for child in self.tree.getChildren(branch)]

			# pack from the bigger rectangles.
			def f(r1, r2):
				return r2.size() - r1.size()
			for rect in sorted(rects, cmp=f):
				packer.add(rect)

			r = self.tree.getRect(branch)
			r.x, r.y = packer.grid.center()
			r.w, r.h = packer.grid.xCoord.width(), packer.grid.yCoord.width()

			# offset to (0,0)

		#TODO align the tree
		#TODO shrink 0.5

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
		#TODO HERE??? default size
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
