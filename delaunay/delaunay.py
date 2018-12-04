import delaunay.geo as geo
import delaunay.line as line

class Delaunay(object):
	def __init__(self, h, w):
		self.height = h
		self.width = w

		self.tris = []
		self.corners = []

		self.fresh_start()

	# Create the supertriangle
	def fresh_start(self):
		p1 = geo.Point(0,0)
		# We are using row == y and column == x.
		# 0,0 is the top left of the image
		p2 = geo.Point(self.height, 0)
		p3 = geo.Point(self.height, self.width)
		p4 = geo.Point(0, self.width)
		self.corners = [p1,p2,p3,p4]

		self.tris.append(geo.Triangle(p1,p2,p3))
		self.tris.append(geo.Triangle(p1,p3,p4))

	# Add points to the triangulation
	def add_points(self, points):
		#curr_tris = []
		polygon = set()
		good_tris = []
		bad_tris = []

		# Add each point
		for p in points:
			good_tris = []
			bad_tris = []
			bad = False
			# If the point is in a tri's circumcircle, that tri goes away,
			# but its the points of its edges create new triangles with p
			for t in self.tris:
				if t.circle.in_circle(p):
					# FUCK CHECK
					bad = bad or (line.Line((t.p1.x, t.p1.y), (t.p2.x, t.p2.y)).det((p.x, p.y)) == 0)
					bad = bad or (line.Line((t.p3.x, t.p3.y), (t.p2.x, t.p2.y)).det((p.x, p.y)) == 0)
					bad = bad or (line.Line((t.p1.x, t.p1.y), (t.p3.x, t.p3.y)).det((p.x, p.y)) == 0)
					# END FUCK CHECK
					if(not bad):
						bad_tris.append(t)
				else:
					# These triangles come out unscathed
					good_tris.append(t)

			if(bad):
				continue
			polygon = set()
			for t in bad_tris:
				t_edges = [t.e1,t.e2,t.e3]
				for edge in t_edges:
					shared_edge = False
					for ot in bad_tris:
						ot_edges = [ot.e1,ot.e2,ot.e3]
						if(t != ot and edge in ot_edges):
							shared_edge = True
							break
					if(not shared_edge):
						polygon.add(edge)
						

			# Create the triangles with the edges
			for e in polygon:
				good_tris.append(geo.Triangle(e.p1, e.p2, p))

			# Replace current set of triangles with the new one
			self.tris = good_tris

		real_tris = []
		for t in self.tris:
			if (t.p1 not in self.corners) and (t.p2 not in self.corners) and (t.p3 not in self.corners):
				real_tris.append(t)
		self.tris = real_tris

