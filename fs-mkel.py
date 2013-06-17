import sys
import os
import os.path

import heiankyoview as HV

root = sys.argv[1]

# path -> id
m = {}
g = HV.Graph()

id = 1
m[root] = id
g.addNode(id)

for parent, dirs, files in os.walk(root):
	parentID = m[parent]
	for child in dirs + files:
		path = "/".join( [parent, child] )
		if os.path.islink(path):
			continue
		id += 1	
		g.addNode(id)
		m[path] = id
		g.addChild( parentID, id )

HV.p(m)

L = []
for n in HV.BFS(g):
	for child in g.getChildren(n):	
		L.append( (n, child) )

print( "\n".join( [ "%s,%s" % (src, dest) for src, dest in L ] ) )
