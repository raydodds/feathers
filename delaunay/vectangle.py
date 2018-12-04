import delaunay.geo as geo

__author__ = "Ray Dodds"


class Vectorizer:

	TO_HEIGHT = '<svg baseProfile="full" height="'
	TO_WIDTH = '" version="1.1" width="'
	HEAD_END = '" xmlns="http://www.w3.org/2000/svg"'+\
				' xmlns:ev="http://www.w3.org/2001/xml-events"'+\
				' xmlns:xlink="http://www.w3.org/1999/xlink">\n'+\
				'<defs />\n'
	TAIL = '</svg>'

	def __init__(self, h='500px', w='500px'):
		self.tristrs = []
		self.height = h
		self.width = w
		self.bbox = '<path d="M 0, 0 '
		self.bbox += '0, '+str(self.height)+' '
		self.bbox += str(self.width)+', '+str(self.height)+' '
		self.bbox += str(self.height)+', 0 z" fill="#FFF" stroke="#000"'
		self.bbox += ' stroke-width="5px" />'

	def add_tri(self, t, color, sw=0):
		ts = '<path d="M '
		ts += str(t.p1.x)+', '+str(t.p1.y)+' '
		ts += str(t.p2.x)+', '+str(t.p2.y)+' '
		ts += str(t.p3.x)+', '+str(t.p3.y)+' '
		ts += 'z" fill="'+color+'" stroke="#0000000" stroke-width="'
		ts += str(sw)+'" />'

		self.tristrs += [ts]

	def stringify(self):
		res = ''
		res += Vectorizer.TO_HEIGHT
		res += str(self.height)
		res += Vectorizer.TO_WIDTH
		res += str(self.width)
		res += Vectorizer.HEAD_END
		for tri in self.tristrs:
			res += tri+'\n'
		res += Vectorizer.TAIL

		return res


	def save(self, filename):
		try:
			f = open(filename+'.svg', 'w+')
		except Exception as e:
			print(e)

		f.write(self.stringify())

		f.close()




