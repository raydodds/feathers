import sys
import cv2 as cv
import numpy as np
import geo
import random
import remove_grid
import os
import delaunay

def show_wait_destroy(winname, img):
	cv.imshow(winname, img)
	cv.moveWindow(winname, 500, 0)
	cv.waitKey(0)
	cv.destroyWindow(winname)

def proc_all(path):
	feathers = []
	feathers_bin = []
	feathers_points = []
	delaun = []
	for filename in os.listdir(path):
		src = cv.imread(os.path.join(path, filename))
		h, w, ch = src.shape
		#show_wait_destroy("ass",src)
		bin_, edge = preProc(src)
		feathers.append(src)
		feathers_bin.append(bin_)
		feathers_points.append(edge)
		d = delaunay.Delaunay(h,w)
		d.add_points(edge)
		delaun.append(d)

	return delaun

def preProc(feather):
	feather_bin = remove_grid.feather_pix(feather)
	h,w,ch = feather.shape
	just_feather = clip(feather, feather_bin)
	#show_wait_destroy("feath", just_feather)
	feather_gs = cv.cvtColor(just_feather, cv.COLOR_BGR2GRAY)
	feather_blur = cv.GaussianBlur(feather_gs, (9,9),0,0)
	edges_x = cv.Sobel(feather_blur, cv.CV_64F, 1, 0, ksize=3)
	xabs = cv.convertScaleAbs(edges_x)
	edges_y = cv.Sobel(feather_blur, cv.CV_64F, 0, 1, ksize=3)
	yabs = cv.convertScaleAbs(edges_y)
	sobeledges = cv.addWeighted(xabs, .5, yabs, .5, 0)
	edges = cv.Canny(feather_blur, 100, 200)
	#show_wait_destroy("edges",edges)
	edges_pts = sampleEdges(sobeledges, 15, .1)
	#print(edges_pts)
	points_img = np.zeros((h,w),np.uint8)
	for p in edges_pts:
		points_img[p.x,p.y] = 255
	show_wait_destroy("sample",points_img)
	print("Finished a feather")
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
	print(len(sampled_points))
	return sampled_points

if __name__ == "__main__":
	if(len(sys.argv) < 2):
		print("no")
	else:
		test = proc_all(sys.argv[1])

		for tri in test[0].tris:
			print(tri)




