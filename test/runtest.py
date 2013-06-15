import heiankyoview as H

import unittest

class Template(unittest.TestCase):
	def setUp(self):
		pass
	def test_hoge(self):
		pass

def mk(w, h):
	r = H.Rectangle()	
	r.w = w
	r.h = h
	return r
def padd(p, L):
	"""
	packing add
	"""
	for r in L:
		p.add(r)
def ras(T, r, xy):
	"""
	rectangle assertion
	"""
	T.assertEquals(r.x, xy[0])	
	T.assertEquals(r.y, xy[1])

class RectanglePacking(unittest.TestCase):
	def setUp(self):
		self.P = H.RectanglePacking()	
	def test_2(self):
		r = [mk(3,3), mk(2,2)]
		padd(self.P, r)
		ras(self, r[0], (1.5, 1.5))
		ras(self, r[1], (1, -1))

class Coordinate(unittest.TestCase):
	def setUp(self):
		self.C = H.Coordinate(0, 3)
		self.C.insert(2, 10)
		self.C.insert(0, -5)
	def test_basic(self):
		self.assertEquals(self.C.size(), 4)
		self.assertEquals(self.C.minLine(), -5)		
		self.assertEquals(self.C.maxLine(), 10)		
		self.assertEquals(self.C.width(), 15)		
		self.assertEquals(self.C.indexOf(3), 2)
	def test_LeftIntersection(self):
		self.assertEquals(self.C.getLeftIntersection(2, 1.5), (1, 1))
		self.assertEquals(self.C.getLeftIntersection(2, 0), (1, 1))
		self.assertEquals(self.C.getLeftIntersection(2, -3), (0, 1))
		self.assertEquals(self.C.getLeftIntersection(2, -5), (0, 1))
		self.assertEquals(self.C.getLeftIntersection(2, -7), (-1, 1))
	def test_RightIntersection(self):
		self.assertEquals(self.C.getRightIntersection(1, 1.5), (1, 1))
		self.assertEquals(self.C.getRightIntersection(1, 3), (1, 1))
		self.assertEquals(self.C.getRightIntersection(1, 5), (1, 2))
		self.assertEquals(self.C.getRightIntersection(1, 10), (1, 2))
		self.assertEquals(self.C.getRightIntersection(1, 11), (1, 3))

class BoolTable(unittest.TestCase):
	def setUp(self):
		self.m = H.BoolTable(1, 1)
	def test_basic(self):
		self.assertFalse(self.m.get(0, -1))
		self.assertFalse(self.m.get(1, 0))
		self.assertFalse(self.m.get(0, 1))
		self.assertFalse(self.m.get(-1, 0))
		self.assertFalse(self.m.get(1, 1))
		self.assertFalse(self.m.get(0, 0))

		self.assertEquals(self.m.n(), 1)
		self.assertEquals(self.m.m(), 1)

	def test_expandI_1(self):
		self.m.set(0, 0, True)
		self.m.expandI(0, 1)
		self.assertEquals(self.m.n(), 2)
		self.assertFalse(self.m.get(0, 0))
		#self.m.show()
		self.assertTrue(self.m.get(1, 0))
	def test_expandI_2(self):
		self.m.expandI(0, 2)
		self.assertEquals(self.m.n(), 3)
	def test_expandI_3(self):
		"""
		start from the outside
		"""
		self.m.expandI(1, 1)
		self.assertEquals(self.m.n(), 2)

	def test_expandJ_1(self):
		self.m.set(0, 0, True)
		self.m.expandJ(0, 1)
		self.assertEquals(self.m.m(), 2)
		self.assertFalse(self.m.get(0, 0))
		#self.m.show()
		self.assertTrue(self.m.get(0, 1))
	def test_expandJ_2(self):
		self.m.expandJ(0, 2)
		self.assertEquals(self.m.m(), 3)

class BinSearch(unittest.TestCase):
	def setUp(self):
		self.arr = [1,3,6,10]
		pass
	def test_binSearch(self):
		self.assertEqual(H.binSearch(self.arr, 3), 1)
		self.assertEqual(H.binSearch(self.arr, 11), -1)
		self.assertEqual(H.binSearch(self.arr, 2), -1)
		self.assertEqual(H.binSearch(self.arr, 1), 0) 
		self.assertEqual(H.binSearch(self.arr, 0), -1) 

class Graph(unittest.TestCase):
	def setUp(self):
		g = H.Graph()
		g.addNode(1)
		g.addNode(2)
		g.addNode(3)
		g.addNode(4)

		g.addChild(1,2)
		g.addChild(1,3)
		g.addChild(2,4)

		self.g = g

	def test_check(self):
		self.assertEqual(self.g.getRoot(), 1)
		self.assertEqual(self.g.getChildren(2), [4])
		self.assertEqual(self.g.isLeaf(3), True)
		self.assertEqual(self.g.isLeaf(4), True)

	def test_BFS(self):
		L = H.BFS(self.g)
		self.assertEqual(L, [1,3,2,4])

if __name__ == '__main__':
	unittest.main()
