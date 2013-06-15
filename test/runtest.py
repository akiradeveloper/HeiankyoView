import heiankyoview as H

import unittest

class Template(unittest.TestCase):
	def setUp(self):
		pass
	def test_hoge(self):
		pass

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
		self.assertEquals(2, self.m.n())
		self.assertFalse(self.m.get(0, 0))
		#self.m.show()
		self.assertTrue(self.m.get(1, 0))
	def test_expandI_2(self):
		self.m.expandI(0, 2)
		self.assertEquals(3, self.m.n())

	def test_expandJ_1(self):
		self.m.set(0, 0, True)
		self.m.expandJ(0, 1)
		self.assertEquals(2, self.m.m())
		self.assertFalse(self.m.get(0, 0))
		#self.m.show()
		self.assertTrue(self.m.get(0, 1))
	def test_expandJ_2(self):
		self.m.expandJ(0, 2)
		self.assertEquals(3, self.m.m())

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
