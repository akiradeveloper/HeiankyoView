import numpy as np
import math

def p(msg):
	pass
	#print(msg)

def half(n):
	assert(n % 2 == 0)
	return n / 2

def delElems(L, indices):
	DL = []
	for i in xrange(0, len(indices)):
		idx = indices[i]
		DL.append( idx - i )
	for i in DL:
		L.pop(i)

class EdgeList:
	@classmethod
	def read(cls, filename):
		f = open(filename)
		T = f.readlines()

		E = []
		for line in T:
			src,dest = line.split(",")
			E.append( (src.strip(), dest.strip()) )

		V = []
		for src,dest in E:
			V.append(src)
			V.append(dest)
		V = set(V)

		g = Graph()
		for n in V:
			TreePacking.addNode(g, n)
		for e in E:
			src,dest = e
			g.addChild(src, dest)
		return g

	@classmethod
	def dump(cls, g):
		L = []
		for n in BFS(g):
			for child in g.getChildren(n):	
				L.append( (n, child) )
		return "\n".join( [ "%s,%s" % (src, dest) for src, dest in L ] ) 

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
		p((self.x, self.y, self.position))

class Rectangle:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.w = 0
		self.h = 0
	def left(self):		
		return self.x - half(self.w)
	def right(self):
		return self.x + half(self.w)
	def up(self):
		return self.y + half(self.h)
	def bottom(self):
		return self.y - half(self.h)
	def size(self):
		return self.w * self.h
	def expand(self, x):
		self.w += x
		self.h += x
	def translate(self, v):
		self.x += v[0]
		self.y += v[1]
	def show(self):		
		p( (self.x, self.y, self.w, self.h) )

class BoolT:
	def __init__(self, N, M):
		self.n = N
		self.m = M
		self.matrix = np.zeros((N, M), dtype=bool)

	def N(self):
		return self.matrix.shape[0]
	def M(self):
		return self.matrix.shape[1]

	def set(self, i, j, value):
		self.matrix[i][j] = value
	def get(self, i, j):
		return self.matrix[i][j]

	def copyI(self, src, dest):
		self.matrix[dest, 0:self.M()] = self.matrix[src, 0:self.M()]
	def copyJ(self, src, dest):
		self.matrix[0:self.N(), dest] = self.matrix[0:self.N(), src]

	def fillIRange(self, begin, end, val):
		self.matrix[begin:end+1, 0:self.M()] = val
	def fillJRange(self, begin, end, val):	
		self.matrix[0:self.N(), begin:end+1] = val
	def fillRange(self, ibegin, iend, jbegin, jend, val):
		self.matrix[ibegin:iend+1, jbegin:jend+1] = val

	def backup(self, to):
		"""
		helper function
		copy all data to another larger 2d-ndarry
		"""
		N = self.N()
		M = self.M()
		to[0:N, 0:M] = self.matrix[0:N, 0:M]

	def doubleN(self):
		m = np.zeros((self.N() * 2, self.M()), dtype=bool)
		self.backup(m)
		self.matrix = m
	def ensureI(self, addI):		
		if self.n + addI > self.N():
			self.doubleN()
	def mvI(self, startI, addI):
		for i in reversed(xrange(startI + addI, self.n)):
			self.copyI(i - addI, i)
		self.fillIRange(startI, startI + addI - 1, False)
	def expandI(self, startI, addI):
		self.ensureI(addI)
		self.n += addI
		self.mvI(startI, addI)

	def doubleM(self):
		m  = np.zeros((self.N(), self.M() * 2), dtype=bool)
		self.backup(m)
		self.matrix = m
	def ensureJ(self, addJ):
		if self.m + addJ > self.M():
			self.doubleM()
	def mvJ(self, startJ, addJ):
		for j in reversed(xrange(startJ + addJ, self.m)):
			self.copyJ(j - addJ, j)
		self.fillJRange(startJ, startJ + addJ - 1, False)
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
	def fillRange(self, ibegin, iend, jbegin, jend, val):
		self.boolT.fillRange(
				self.adjustI(ibegin), self.adjustI(iend),
				self.adjustJ(jbegin), self.adjustJ(jend),
				val)

	def get(self, i, j):
		return self.boolT.get(self.adjustI(i), self.adjustJ(j))
	def set(self, i, j, b):
		self.boolT.set(self.adjustI(i), self.adjustJ(j), b)
	def n(self):
		return self.boolT.n - 2
	def m(self):
		return self.boolT.m - 2
	def expandI(self, startI, addI):
		self.boolT.expandI(self.adjustI(startI), addI)
	def expandJ(self, startJ, addJ):
		self.boolT.expandJ(self.adjustJ(startJ), addJ)
	def copyI(self, src, dest):
		self.boolT.copyI(self.adjustI(src), self.adjustI(dest))
	def copyJ(self, src, dest):
		self.boolT.copyJ(self.adjustJ(src), self.adjustJ(dest))
	def show(self):
		for i in xrange(0, self.n()):
			for j in xrange(0, self.m()):
				pass

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
		p(self.L)

class Placement:
	def __init__(self, left, right, bottom, top):	
		self.left = left
		self.right = right
		self.bottom = bottom
		self.top = top

	def x(self):
		return self.left + half(self.right - self.left) 
	def y(self):
		return self.bottom + half(self.top - self.bottom) 

	def show(self):
		p( (self.left, self.right, self.bottom, self.top) )

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
		x = self.xCoord.minLine() + half(self.xCoord.width())
		y = self.yCoord.minLine() + half(self.yCoord.width())
		return (x, y)

	def updateBoolT(self, iGridMin, iGridMax, jGridMin, jGridMax):
		self.boolT.fillRange(iGridMin, iGridMax, jGridMin, jGridMax, True)

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

	#FIXME position is not used.
	def collectCandidates(self, iLeft, iRight, jBottom, jTop, position):
		p("collect")
		def OneSide(i, j, base, target):
			if self.getCornerType(i, j, base, target) == CornerType.ADJACENT:
				c = Candidate(
						self.xCoord.get(i), 
						self.yCoord.get(j),
						target)
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
			mid = self.xCoord.minLine() < newXLine < self.xCoord.maxLine()
			self.xCoord.insert(I, newXLine)
			self.boolT.expandI(I, 1)
			if mid:
				self.boolT.copyI(I-1, I)

		if not self.yCoord.has(newYLine):
			mid = self.yCoord.minLine() < newYLine < self.yCoord.maxLine()
			self.yCoord.insert(J, newYLine)
			self.boolT.expandJ(J, 1)
			if mid:
				self.boolT.copyJ(J-1, J)

		iLeft, iRight, jBottom, jTop = self.calcIntersectableRegion(x, y, position, w, h)
		self.updateBoolT(iLeft, iRight, jBottom, jTop)
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

		N = len(self.grid.candidates)
		decisionIdx = N
		delList = []
		for i in reversed(xrange(0, N)):
			candidate = self.grid.candidates[i]

			candidate.show()
			X = candidate.x
			Y = candidate.y
			P = candidate.position

			#FIXED X, Y are coordinate, not index
			gridIdx = self.grid.getGridIndex(
					self.grid.xCoord.indexOf(X), 
					self.grid.yCoord.indexOf(Y), 
					P)
	
			if self.grid.isOccupied(gridIdx[0], gridIdx[1]):
				delList.append(i)
				continue

			if self.grid.intersects(X, Y, P, rect.w, rect.h):
				continue

			tryW, tryH = self.grid.tryPlacement(X, Y, P, rect.w, rect.h)
			p( "tryW:%f tryH:%f" % (tryW, tryH) )
			tryEval = self.evaluatePlacement(tryW, tryH)

			currentsize = self.grid.xCoord.width() * self.grid.yCoord.width()
			if (tryW * tryH) <= (currentsize + 1):
				p("size not change! tryEval % f" % tryEval)
				bestEval = tryEval
				decision = candidate
				decisionIdx = i
				break

			if tryEval < bestEval:
				p("size changed by candidate placed. tryEval %f" % tryEval)
				bestEval = tryEval
				decision = candidate
				decisionIdx = i

		p("bestEval %f" % bestEval)
		bestEval -= 1
		decisionOutside = False

		rightUpCorner = (
				self.grid.xCoord.maxLine(),
				self.grid.yCoord.maxLine())
		tryW1, tryH1 = self.grid.tryPlacement(rightUpCorner[0], rightUpCorner[1], CornerPosition.RIGHT_DOWN, rect.w, rect.h)
		tryEval1 = self.evaluatePlacement(tryW1, tryH1)
		p("tryEval1 %f" % tryEval1)
		if tryEval1 < bestEval:
			p("choose outside candidate 1")
			bestEval = tryEval1
			decision = Candidate(rightUpCorner[0], rightUpCorner[1], CornerPosition.RIGHT_DOWN)
			decisionOutside = True

		leftDownCorner = (
				self.grid.xCoord.minLine(),
				self.grid.yCoord.minLine())
		tryW2, tryH2 = self.grid.tryPlacement(leftDownCorner[0], leftDownCorner[1], CornerPosition.RIGHT_DOWN, rect.w, rect.h)
		tryEval2 = self.evaluatePlacement(tryW2, tryH2)
		p("tryEval2 % f" % tryEval2)
		if tryEval2 < bestEval:
			p("choose outside candidate 2")
			bestEval = tryEval2
			decision = Candidate(leftDownCorner[0], leftDownCorner[1], CornerPosition.RIGHT_DOWN)
			decisionOutside = True

		pm = self.grid.getPlacement(
				decision.x,
				decision.y,
				decision.position,
				rect.w,
				rect.h)
			
		self.grid.place(
				decision.x,
				decision.y,
				decision.position,
				rect.w,
				rect.h)

		if not decisionOutside:
			p("not outside")
			delList.append(decisionIdx)

		delElems(self.grid.candidates, sorted(delList))

		rect.x = pm.x()
		rect.y = pm.y()

	def add(self, rect):
		"""
		Add a rectangle to the packing grid.
		The position of the rectangle will be calculated.
		"""
		if not self.grid:
			self.grid = PackingGrid(0, rect.w, 0, rect.h)
			rect.x = half(rect.w)
			rect.y = half(rect.h)
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

	@classmethod
	def addNode(cls, g, id):
		"""
		Add a node to a graph.
		Use this function when the graph is a tree to be packed afterward.
		"""
		g.addNode(id)	
		g.setAttr(id, Rectangle())

	@classmethod
	def pack(cls, tree):
		"""
		Calculate the size and position of the nodes.
		"""
		L = BFS(tree)
		branches = filter(lambda id: not tree.isLeaf(id), L)
		leaves = filter(lambda id: tree.isLeaf(id), L)

		pad = 2
			
		for leaf in leaves:		
			r = tree.getRect(leaf)
			r.w = 10
			r.h = 10

		for parent in reversed(branches):
			#print(parent)
			packer = RectanglePacking()
			crects = [tree.getRect(child) for child in tree.getChildren(parent)]

			uniformsz = True	
			#uniformsz = False
			r = crects[0]
			sz = (r.w, r.h)
			for cr in crects:
				if not sz == (cr.w, cr.h):
					uniformsz = False
					break
			D = half(sz[0])
			
			pr = tree.getRect(parent)
			if uniformsz:
				n = len(crects)
				sq = math.sqrt(n)
				# N >= M
				N = int(math.ceil(sq))		
				M = int(math.ceil(float(n)/N))
				stride = 2 * D + pad
				for j in xrange(0, M):
					for i in xrange(0, N):
						idx = j * N + i
						if not idx < n:
							break
						cr = crects[idx]
						cr.x = stride * i 
						cr.y = - stride * j
				left = - (D + pad)
				right = stride * (N-1) + D + pad
				bottom =  - (stride * (M-1) + D + pad)
				top = D + pad

				pr.x = half(left + right)
				pr.y = half(bottom + top)
				pr.w = right - left
				pr.h = top - bottom
			else:			
				# pack from the bigger rectangles
				def f(r1, r2):
					return r2.size() - r1.size()
				for cr in sorted(crects, cmp=f):
					cr.expand(pad)
					packer.add(cr)
	
				pr.x, pr.y = packer.grid.center()
				pr.w, pr.h = packer.grid.xCoord.width(), packer.grid.yCoord.width()
	
				pr.expand(pad)
				for cr in crects:
					cr.expand(-pad)	

			for cr in crects:
				cr.translate( (-pr.x, -pr.y) )

			pr.x = 0
			pr.y = 0

		for parent in branches:
			pr = tree.getRect(parent)
			crects = [tree.getRect(child) for child in tree.getChildren(parent)]
			# pr.show()
			for cr in crects:
				# cr.show()
				cr.translate( (pr.x, pr.y) )
	
		#rr = self.tree.getRect( self.tree.getRoot() )
		#rr.expand(-2)

class Graph:
	def __init__(self):
		self.nodes = {} # ID -> rect
		self.children = {} # ID -> [childID]
		self.parent = {} # ID -> parentID

	def size(self):
		return len(self.nodes)

	def isLeaf(self, id):
		return not id in self.children

	def addNode(self, id):
		if id in self.nodes:
			return
		self.nodes[id] = None	
		self.parent[id] = None

	def setAttr(self, id, attr):
		self.nodes[id] = attr

	def getAttr(self, id):
		return self.nodes[id]

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
		self.parent[child] = parent

	def getRoot(self):
		for k in self.nodes.keys():
			anyID = k
			break
		root = anyID
		while(self.parent[root]):
			root = self.parent[root]
		return root

if __name__ ==  '__main__':
	pass
