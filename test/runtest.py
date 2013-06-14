import heiankyoview as H

import unittest

class Template(unittest.TestCase):
	def setUp(self):
		pass
	def testHoge(self):
		pass

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
