import geo

class Delaunay(object):
    def __init__(self, h, w):
        self.height = h
        self.width = w

        self.tris = []

        fresh_start()

    def fresh_start(self):
        p1 = geo.Point(0,0)
        p2 = geo.Point(self.height, 0)
        p3 = geo.Point(self.height, self.width)
        p4 = geo.Point(0, self.width)

        tris.append(geo.Triangle(p1,p2,p3))
        tris.append(geo.Triangle(p1,p3,p4))

    def add_points(self, points):
        temp_tris = []
        edges = []

        for p in points:
            temp_tris = []
            edges = []
            for t in self.tris:
                if t.circle.in_circle(p):
                    edges.append(t.e1)
                    edges.append(t.e2)
                    edges.append(t.e3)
                else:
                    temp_tris.append(t)
