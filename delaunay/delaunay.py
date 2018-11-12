import geo

class Delaunay(object):
    def __init__(self, h, w):
        self.height = h
        self.width = w

        self.tris = []

        fresh_start()

    # Create the supertriangle
    def fresh_start(self):
        p1 = geo.Point(0,0)
        # We are using row == y and column == x.
        # 0,0 is the top left of the image
        p2 = geo.Point(self.height, 0)
        p3 = geo.Point(self.height, self.width)
        p4 = geo.Point(0, self.width)

        tris.append(geo.Triangle(p1,p2,p3))
        tris.append(geo.Triangle(p1,p3,p4))

    # Add points to the triangulation
    def add_points(self, points):
        curr_tris = []
        edges = set()

        # Add each point
        for p in points:
            curr_tris = []
            edges.clear()
            # If the point is in a tri's circumcircle, that tri goes away,
            # but its the points of its edges create new triangles with p
            for t in self.tris:
                if t.circle.in_circle(p):
                    edges.add(t.e1)
                    edges.add(t.e2)
                    edges.add(t.e3)
                else:
                    # These triangles come out unscathed
                    curr_tris.append(t)

            # Create the triangles with the edges
            for e in edges:
                curr_tris.append(geo.Triangle(e.p1, e.p2, p))

            # Replace current set of triangles with the new one
            self.tris = curr_tris
