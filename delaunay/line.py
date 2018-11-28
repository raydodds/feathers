#
#	line.py
#	A Line class
#

__author__ = "Ray Dodds, Jonathan Schenk"

import math as m

class Line:
	def __init__(self, start, end, a=None, b=None, c=None):
		# Make sure the line is aligned left to right
		if(a is None and b is None):
			if( start[0] < end[0] ):
				self.start = start
				self.end = end
			else:
				self.start = end
				self.end = start

			# y = ax-b
			try:
				self.a = (end[1]-start[1])/(end[0]-start[0])
			except ZeroDivisionError:
				self.a = m.inf

			# b = ax - y
			self.b = self.a*start[0] - start[1]

			#x = c
			if(self.a == m.inf or self.b == m.inf):

				if(c != None):
					self.c = c
				else:
					self.c = start[0]
			else:
				self.c = c
		else:
			self.start = None
			self.end = None
			self.a = a
			self.b = b
			self.c = c

	def __repr__(self):
		if(self.a == m.inf):
			return 'x='+str(self.c)

		rep = 'y='+str(self.a)+"*x"

		if(self.b > 0):
			rep += "-"+str(self.b)
		else:
			rep += "+"+str(self.b)

		return rep

	# Find where two lines intersect
	def intersect(self, other):
		if(self.a == m.inf or other.a == m.inf):
			if(self.a == other.a):
				return None
			if(self.a == m.inf):
				return (self.c, other.yAt(self.c))
			else:
				return (other.c, self.yAt(other.c))

		if(self.a == other.a):
			# Lines are parallel
			return None
		x = (self.b-other.b)/(self.a-other.a)
		y = self.a*x-self.b

		return (x,y)

	# Get the y for a given x
	def yAt(self, x):
		if(self.a == m.inf):
			return None
		return self.a*x-self.b

	# Get the x for a given y
	def xAt(self, y):
		if(self.a == m.inf):
			return self.c
		return (y+self.b)/(self.a)

	# Check if a point is within the x range of the line
	def in_x(self, point):
		return not ( self.start[0] > point[0] or self.end[0] < point[0] )

	# Check if a point is within the y range of the line
	def in_y(self, point):
		return not ( self.start[1] > point[1] or self.end[1] < point[1] )

	def det(self, p):
		return ((self.end[0] - self.start[0]) * (p[1] - self.start[1])\
				- (self.end[1] - self.start[1]) * (p[0] - self.start[0]))

	def above(self, p):
		return self.det(p) > 0

	def midpoint(self):
		return ((self.start[0]+self.end[0])/2, (self.start[1]+self.end[1])/2)

	def perp_slope(self):
		try:
			inv = 1/self.a
		except ZeroDivisionError:
			return m.inf
		return -inv

	def get_b(slope, point):
		return point[0]*slope-point[1]

	def perp_bisect(self):
		mpoint = self.midpoint()
		p_slope = self.perp_slope()
		new_b = Line.get_b(p_slope, mpoint)
		if(p_slope != m.inf):
			return Line(None, None, p_slope, new_b)
		else:
			return Line(None, None, p_slope, new_b, mpoint[0])
		

	#	COMPARATOR METHODS
	def __eq__(self, other):
		if(self.start != None and other.start != None and self.end != None and other.end != None):
			return (self.start == other.start) and (self.end == other.end)
		else:
			if(self.a == m.inf or other.a == m.inf):
				if(self.a == other.a):
					return self.c == other.c
				else:
					return False
			else:
				return self.a == other.a and self.b == other.b
	
	def __ne__(self, other):
		if(self.a != other.a):
			return True
		elif(self.b != other.b):
			return True
		elif(self.a == m.inf):
			return self.c == other.c
		return not (self == other)

def tests():
	pt0 = (0,0)
	pt2 = (1,1)
	pt3 = (1,0)
	pt1 = (0,1)

	pt4 = (-1, 0)
	pt5 = (0, -1)

	l0 = Line(pt0, pt2)
	l2 = Line(pt1, pt3)
	l1 = Line(pt0, pt2)
	# Verical
	l3 = Line(pt5, pt1)
	l5 = Line(pt2, pt3)
	# Horizontal
	l4 = Line(pt4, pt3)

	# Basic Comparators
	assert l0 == l1
	assert l0 != l2

	# Intersections
	assert l0.intersect(l1) is None
	assert l0.intersect(l2) is not None

	# __repr__
	assert repr(l0) == repr(l1)
	assert repr(l0) == 'y=1.0*x+0.0'

	# Test midpoint
	assert l0.midpoint() == l2.midpoint()

	# test perp_bisector
	assert l0.perp_bisect() == l2

	# test for hline
	assert l4.perp_bisect() == l3

	# intersect with vline and hline
	assert l4.intersect(l3) == (0,0)

	assert l5.intersect(l0) == (1,1)






	

if(__name__ == "__main__"):
	tests()	
