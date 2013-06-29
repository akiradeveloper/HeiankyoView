import heiankyoview as HV
import random
import time

def create_tree(n):
	g = HV.Graph()
	id = 1
	rootID = id
	HV.TreePacking.addNode(g, rootID)
	
	for _ in xrange(0, n):
		id += 1
		bid = id
		HV.TreePacking.addNode(g, bid)
		g.addChild(rootID, bid)
		nr_min = 10
		nr_max = 1000
		m = random.randint(nr_min, nr_max)
		for _ in xrange(0, m):
			id += 1
			HV.TreePacking.addNode(g, id)
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
		start = time.time()
		HV.TreePacking.pack(t)	
		end = time.time()
		T.append( end - start )	
	ave = sum(T) / N	
	R.append( (n, ave) )	

print("\n".join( ["%d,%f" % (n, t) for n, t in R] ))
