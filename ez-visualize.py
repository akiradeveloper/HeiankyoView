import heiankyoview as HV
import svgwrite
import sys

fn = sys.argv[1]

dwg = svgwrite.Drawing(size=('100%', '100%'), profile='tiny')

g = HV.EdgeList.read(fn)
L = HV.BFS(g)

tp = HV.TreePacking(g)
tp.pack()

rr = g.getRect( g.getRoot() )
mvx, mvy = 0.5 * rr.w - rr.x, (-0.5) * rr.h - rr.y
W, H = float(rr.w + 1), float(rr.h + 1)

def toperc(n):
	return "%f" % (100.0 * n) + "%"

for n in L:
	rect = g.getRect(n)
	rect.translate( (mvx, mvy) )
	
	# 0.0-1.0
	x, y = rect.left() / W, -rect.up() / H
	w, h = rect.w / W, rect.h / H

	dwg.add(dwg.rect(
		insert=(toperc(x), toperc(y)),
		size=(toperc(w), toperc(h)),
		stroke="black",
		stroke_width=1,
		fill_opacity=0))

print(dwg.tostring())
