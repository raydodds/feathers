#!/usr/bin/python3

import math
import sys
import cv2 as cv
import numpy as np
import geo
import random
import remove_grid
import os
import delaunay
import random
from vectangle import Vectorizer

def show_wait_destroy(winname, img):
	cv.imshow(winname, img)
	cv.moveWindow(winname, 500, 0)
	cv.waitKey(0)
	cv.destroyWindow(winname)

'''

Probably user input: num feathers, thresh, sobel size, sample rate, border on/off, blur, colors?

'''
def proc_all(path, num_feath, sample_thresh, sample_rate, filter_type, border_width, color):
	feathers = []
	feathers_bin = []
	feathers_points = []
	delaun = []
	ind = 0
	vec = Vectorizer('1000px','1000px')
	for filename in os.listdir(path):
		if(ind == num_feath):
			break
		src = cv.imread(os.path.join(path, filename))
		h, w, ch = src.shape
		bin_, edge = preProc(src, sample_thresh, sample_rate, filter_type)
		feathers.append(src)
		feathers_bin.append(bin_)
		feathers_points.append(edge)
		d = delaunay.Delaunay(h,w)
		d.add_points(edge)
		colors = color_tris(src, d.tris)
		rot_tris = rotate(d.tris,random.uniform(0,2*math.pi))
		trans_tris = translate(rot_tris)
		i = 0
		for tri in trans_tris:
			vec.add_tri(tri,colors[i])
			i += 1
		delaun.append(d)
		ind += 1

	vec.save('testvec')
	return delaun

def translate(rot_tris):
	minx = geo.Point(10000,10000)
	maxx = geo.Point(0,0)
	miny = geo.Point(10000,10000)
	maxy = geo.Point(0,0)
	for tri in rot_tris:
		if(tri.p1.y < miny.y):
			miny = tri.p1
		if(tri.p2.y < miny.y):
			miny = tri.p2
		if(tri.p3.y < miny.y):
			miny = tri.p3

		if(tri.p1.x < minx.x):
			minx = tri.p1
		if(tri.p2.x < minx.x):
			minx = tri.p2
		if(tri.p3.x < minx.x):
			minx = tri.p3

		if(tri.p1.y > maxy.y):
			maxy = tri.p1
		if(tri.p2.y > maxy.y):
			maxy = tri.p2
		if(tri.p3.y > maxy.y):
			maxy = tri.p3

		if(tri.p1.y > maxx.x):
			maxx = tri.p1
		if(tri.p2.y > maxx.x):
			maxx = tri.p2
		if(tri.p3.y > maxx.x):
			maxx = tri.p3

	xmove = random.randint(-minx.x, 1000-maxx.x)
	ymove = random.randint(-miny.y, 1000-maxy.y)
	for tri in rot_tris:
		tri.p1.x += xmove
		tri.p1.y += ymove
		tri.p2.x += xmove
		tri.p2.y += ymove
		tri.p3.x += xmove
		tri.p3.y += ymove
	return rot_tris
	

def rotate(tris, angle):
	#actually max
	minpt = geo.Point(0,0)
	for tri in tris:
		if(tri.p1.y > minpt.y):
			minpt = tri.p1
		if(tri.p2.y > minpt.y):
			minpt = tri.p2
		if(tri.p3.y > minpt.y):
			minpt = tri.p3

	for tri in tris:
		dy1 = tri.p1.y - minpt.y
		dx1 = tri.p1.x - minpt.x
		ynew1 = int(dx1 * math.sin(angle) + dy1 * math.cos(angle))
		xnew1 = int(dx1 * math.cos(angle) - dy1 * math.sin(angle))
		ynew1 += minpt.y
		xnew1 += minpt.x
		tri.p1 = geo.Point(xnew1,ynew1)
		dy2 = tri.p2.y - minpt.y
		dx2 = tri.p2.x - minpt.x
		ynew2 = int(dx2 * math.sin(angle) + dy2 * math.cos(angle))
		xnew2 = int(dx2 * math.cos(angle) - dy2 * math.sin(angle))
		ynew2 += minpt.y
		xnew2 += minpt.x
		tri.p2 = geo.Point(xnew2,ynew2)
		dy3 = tri.p3.y - minpt.y
		dx3 = tri.p3.x - minpt.x
		ynew3 = int(dx3 * math.sin(angle) + dy3 * math.cos(angle))
		xnew3 = int(dx3 * math.cos(angle) - dy3 * math.sin(angle))
		ynew3 += minpt.y
		xnew3 += minpt.x
		tri.p3 = geo.Point(xnew3,ynew3)
	return tris
	

def preProc(feather, sample_thresh, sample_rate, filter_type):
	feather_bin = remove_grid.feather_pix(feather)
	h,w,ch = feather.shape
	just_feather = clip(feather, feather_bin)
	feather_gs = cv.cvtColor(just_feather, cv.COLOR_BGR2GRAY)
	feather_blur = cv.GaussianBlur(feather_gs, (9,9),0,0)
	if(filter_type == 's'):
		edges_x = cv.Sobel(feather_blur, cv.CV_64F, 1, 0, ksize=3)
		xabs = cv.convertScaleAbs(edges_x)
		edges_y = cv.Sobel(feather_blur, cv.CV_64F, 0, 1, ksize=3)
		yabs = cv.convertScaleAbs(edges_y)
		edges = cv.addWeighted(xabs, .5, yabs, .5, 0)
	elif(filter_type == 'c'):
		edges = cv.Canny(feather_blur, 100, 200)
	else:
		edges = None

	edges_pts = sampleEdges(edges, sample_thresh, sample_rate)
	points_img = np.zeros((h,w),np.uint8)
	for p in edges_pts:
		points_img[p.x,p.y] = 255
	show_wait_destroy("sample",just_feather)
	return feather_bin, edges_pts

def clip(feather, feather_bin):
	h,w,ch = feather.shape
	just_feather = np.zeros((h,w,ch), np.uint8)
	for i in range(0,h):
		for j in range(0,w):
			if feather_bin[i,j] == 255:
				just_feather[i,j,0] = feather[i,j,0]
				just_feather[i,j,1] = feather[i,j,1]
				just_feather[i,j,2] = feather[i,j,2]
	return just_feather

def sampleEdges(edges, thresh, sample_rate=.75):
	neigh_sum = 0
	total_neigh = 0
	points = []
	h, w = edges.shape
	if(sample_rate > 1):
		sample_rate = 1

	for i in range(0, h):
		for j in range(0, w):
			neigh_sum = 0
			total_neigh = 0
			for ni in range(-1,2):
				ny = ni + i
				if ny >= 0 and ny < h:
					for nj in range(-1,2):
						nx = j + nj
						if nx >= 0 and nx < w:
							neigh_sum += int(edges[ny,nx])
							total_neigh += 1
			if total_neigh > 0:
				neigh_sum /= total_neigh
			if neigh_sum > thresh:
				points.append(geo.Point(i,j))
	edge_pt_count = int(float(len(points) * sample_rate))
	sampled_points = random.sample(points, edge_pt_count)
	return sampled_points

def color_tris(feather, tris):
	colors = []
	for tri in tris:
		cx = (tri.p1.x + tri.p2.x + tri.p3.x) / 3
		cy = (tri.p1.y + tri.p2.y + tri.p3.y) / 3
		b = feather[int(cx)][int(cy)][0]
		g = feather[int(cx)][int(cy)][1]
		r = feather[int(cx)][int(cy)][2]
		colstring = "#{0:02x}{1:02x}{2:02x}".format(r,g,b)
		colors.append(colstring)
	return colors

if __name__ == "__main__":
	if(len(sys.argv) < 2):
		print("no")
	else:
		test = proc_all(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),float(sys.argv[4]),sys.argv[5],sys.argv[6],sys.argv[7])

		for tri in test[0].tris:
			print(tri)




