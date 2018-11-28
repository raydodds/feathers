#!/usr/bin/python3
import line
import geo
import delaunay
import random as r
from vectangle import Vectorizer

p1 = geo.Point(100,100)
p2 = geo.Point(150,150)
p3 = geo.Point(100,150)
p4 = geo.Point(150,150)
p5 = geo.Point(125,130)
p6 = geo.Point(130,125)
p7 = geo.Point(120,125)
p8 = geo.Point(125,120)

colors = ['#FFFFFF',
'#C0C0C0','#808080',
'#000000','#FF0000',
'#800000','#FFFF00',
'#808000','#00FF00',
'#008000','#00FFFF',
'#008080','#0000FF',
'#000080','#FF00FF',
'#800080']


d = delaunay.Delaunay(200, 200)

d.add_points([p5, p6, p7, p8])

for tri in d.tris:
	print(tri)

vec = Vectorizer('15cm', '15cm')
for tri in d.tris:
	vec.add_tri(tri, colors[r.randint(0, 16)])

vec.save('testvec')
