#!/usr/bin/python3
import line
import geo
import delaunay

p1 = geo.Point(0,0)
p2 = geo.Point(10, 10)
p3 = geo.Point(0, 10)
p4 = geo.Point(10, 10)
p5 = geo.Point(5,6)

d = delaunay.Delaunay(10, 10)

d.add_points([p5])

for tri in d.tris:
	print(tri)
