import heiankyoview as HV
import random
import time

def create_tree(n):
	g = HV.Graph()
	id = 1
	rootID = id
	g.addNode(rootID)
	
	for _ in xrange(0, n):
		id += 1
		bid = id
		g.addNode(bid)
		g.addChild(rootID, bid)
		nr_min = 10
		nr_max = 1000
		m = random.randint(nr_min, nr_max)
		for _ in xrange(0, m):
			id += 1
			g.addNode(id)
			g.addChild(bid, id)
	return g

ns = []
for i in xrange(0, 10):
	ns.append( (i+1) * 100 )

R = []
for n in ns:
	T = []
	N = 1
	for _ in xrange(0, N):
		t = create_tree(n)
		tp = HV.TreePacking(t)
		start = time.time()
		tp.pack()	
		end = time.time()
		T.append( end - start )	
	ave = sum(T) / N	
	R.append( (n, ave) )	

print("\n".join( ["%d,%f" % (n, t) for n, t in R] ))
