import sys
import cv2 as cv
import numpy as np
import geo
import random

def show_wait_destroy(winname, img):
    cv.imshow(winname, img)
    cv.moveWindow(winname, 500, 0)
    cv.waitKey(0)
    cv.destroyWindow(winname)

def preProc(feather):
    feather_gs = cv.cvtColor(feather, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(feather_gs, 100, 200)
    show_wait_destroy("edges",edges)

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
                        nx = x + nj
                        if ny >= 0 and ny < h:
                            neigh_sum += int(edges[ny,nx])
                            total_neigh += 1
            if total_neigh > 0:
                neigh_sum /= total
            if sum > thresh:
                points.append(geo.Point(i,j))
    edge_pt_count = int(len(points) * sample_rate)
    sampled_points = random.sample(xrange(0,edge_pt_count),points)
    return sampled_points


if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("no")
    else:
        src = cv.imread(sys.argv[1],cv.IMREAD_COLOR)
        preProc(src)
