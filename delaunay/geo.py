import math

TOLERANCE = .001

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def equals(self, other):
        ret = False
        dx = math.abs(self.x - other.x)
        dy = math.abs(self.y - other.y)

        if dx < tolerance and dy < tolerance:
            ret = True

        return ret

class Edge(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def equals(other):
        ret = False
        if (self.p1.equals(other.p1) and self.p2.equals(other.p2))\
           (self.p1.equals(other.p2) and self.p2.equals(other.p1)):
            ret = True

        return ret

class Circle(object):
    def __init__(self, center, rad):
        self.center = center
        self.rad = rad

    def in_circle(self, p):
        ret = False
        dx = self.x - p.x
        dy = self.y - p.y

        dist = dx**2 + dy**2

        if(dist < self.rad):
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

        ux = p2.x - p1.x
        uy = p2.y - p1.y
        vx = p3.x - p1.x
        vy = p3.y - p1.y

        u = ux**2 + uy**2
        v = vx**2 + vy**2
        s = .5 / (ux * vy - uy * vy)

        circ_x = p1.x + (vy * u - uy * v) * s
        circ_y = p1.y + (ux * v - vx * u) * s

        dx = p1.x - circ_x
        dy = p1.y - circ_y

        rad = dx**2 + dy**2

        self.circle = Circle(Point(circ_x, cirx_y), rad)
