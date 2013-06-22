import heiankyoview as HV

import unittest

class Template(unittest.TestCase):
	def setUp(self):
		pass
	def test_hoge(self):
		pass

class Util(unittest.TestCase):
	def setUp(self):
		pass
	def test_delElems(self):
		L = [3,5,2,9,1]
		HV.delElems(L, [1,3])
		self.assertEquals(L, [3,2,1])

class TreePacking(unittest.TestCase):
	def setUp(self):
		pass
		
	def test_1(self):
		print("test1")
		g = HV.Graph()
		HV.TreePacking.addNode(g, 1) 
		HV.TreePacking.addNode(g, 2)
		g.addChild(1,2)

		HV.TreePacking.pack(g)

		L = HV.BFS(g)
		for n in L:
			r = g.getRect(n)
			r.show()

	def test_2(self):
		print("test2")
		g = HV.Graph()
		HV.TreePacking.addNode(g, 1)
		HV.TreePacking.addNode(g, 2)
		HV.TreePacking.addNode(g, 3)
		HV.TreePacking.addNode(g, 4)

		g.addChild(1,2)
		g.addChild(1,3)
		g.addChild(2,4)

		self.g = g

		HV.TreePacking.pack(g)

		print("test2 tree show")
		L = HV.BFS(g)
		for n in L:
			r = g.getRect(n)
			r.show()

def mk(w, h):
	r = HV.Rectangle()	
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
		self.P = HV.RectanglePacking()	
	def test_2(self):
		r = [mk(6,6), mk(4,4)]
		padd(self.P, r)
		ras(self, r[0], (3,3))
		ras(self, r[1], (2,-2))
	def test_3_1(self):
		print("test 3 1")
		r = [mk(6,6), mk(4,4)]
		padd(self.P, r)
		self.assertEquals(self.P.grid.xCoord.size(), 3)
		self.assertEquals(self.P.grid.yCoord.size(), 3)
		self.P.grid.xCoord.show()
		self.P.grid.yCoord.show()
		r2 = mk(4,2)
		print("add r2")
		self.P.add(r2)
		self.P.grid.xCoord.show()
		self.P.grid.yCoord.show()
		r2.show()
		ras(self, r2, (6,-1)) 
	def test_3_2(self):
		r = [mk(6,6), mk(4,4), mk(2,2)]
		padd(self.P, r)
		ras(self, r[2], (5,-1)) 
	def test_9(self):
		r = [mk(10,10), mk(6,6), mk(2,2), mk(2,2), mk(2,2), mk(2,2), mk(2,2), mk(2,2), mk(2,2)]
		padd(self.P, r)
		for R in r:
			pass
			R.show()

class Coordinate(unittest.TestCase):
	def setUp(self):
		self.C = HV.Coordinate(0, 3)
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
		self.m = HV.BoolTable(1, 1)
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
		self.assertEqual(HV.binSearch(self.arr, 3), 1)
		self.assertEqual(HV.binSearch(self.arr, 11), -1)
		self.assertEqual(HV.binSearch(self.arr, 2), -1)
		self.assertEqual(HV.binSearch(self.arr, 1), 0) 
		self.assertEqual(HV.binSearch(self.arr, 0), -1) 

class Graph(unittest.TestCase):
	def setUp(self):
		g = HV.Graph()
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
		L = HV.BFS(self.g)
		self.assertEqual(L, [1,3,2,4])

if __name__ == '__main__':
	unittest.main()
