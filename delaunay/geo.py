import math
import line

TOLERANCE = .001

class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __repr__(self):
		return "Point(%s, %s)" % (self.x, self.y)

	def __eq__(self, other):
		ret = False
		dx = abs(self.x - other.x)
		dy = abs(self.y - other.y)

		if dx < TOLERANCE and dy < TOLERANCE:
			ret = True

		return ret

	def __ne__(self, other):
		ret = False
		dx = math.abs(self.x - other.x)
		dy = math.abs(self.y - other.y)

		if not (dx < TOLERANCE and dy < TOLERANCE):
			ret = True

		return ret

class Edge(object):
	def __init__(self, p1, p2):
		self.p1 = p1
		self.p2 = p2

	def __repr__(self):
		return "Edge(%s, %s)" % (self.p1, self.p2)

	def __eq__(self, other):
		ret = False
		if (self.p1 == other.p1 and self.p2 == other.p2) or\
		   (self.p1 == other.p2 and self.p2 == other.p1):
			ret = True

		return ret

	def __ne__(self, other):
		ret = False
		if not ((self.p1 == other.p1 and self.p2 == other.p2) or\
		   (self.p1 == other.p2 and self.p2 == other.p1)):
			ret = True

		return ret

	def __hash__(self):
		return hash(self.__repr__())

class Circle(object):
	def __init__(self, center, rad):
		self.center = center
		self.rad = rad

	# Is this point within the circumcircle?
	def in_circle(self, p):
		ret = False
		dx = self.center.x - p.x
		dy = self.center.y - p.y

		dist = dx**2 + dy**2

		if(dist < self.rad**2):
			ret = True

		return ret

class Triangle(object):
	def __init__(self, p1, p2, p3):
		self.p1 = p1
		self.p2 = p2
		self.p3 = p3
		self.e1 = Edge(p1, p2)
		self.e2 = Edge(p2, p3)
		self.e3 = Edge(p3, p1)

		# Calculate circumcenter, radius (might be wrong)
		l1 = line.Line((p1.x, p1.y), (p2.x, p2.y))
		l2 = line.Line((p1.x, p1.y), (p3.x, p3.y))

		isct = Point(*(l1.intersect(l2)))

		rad = m.sqrt((p1.x-isct.x)**2 + (p1.y-isct.y)**2)


		self.circle = Circle(Point(circ_x, circ_y), rad)

	def __repr__(self):
		return 'Triangle('+str(self.p1)+','+str(self.p2)+','+str(self.p3)+')'
