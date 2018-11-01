#!/usr/bin/python

'''
segment.py

Provides functionality to perform segmentation using textures.

author: Jonathan Schenk : jds8899
'''

import sys
import cv2 as cv
import numpy as np
import random
import math
import makeLMfilters
from sklearn.cluster import KMeans
from sklearn.cluster import MeanShift

def show_wait_destroy(winname, img):
    cv.imshow(winname, img)
    cv.moveWindow(winname, 500, 0)
    cv.waitKey(0)
    cv.destroyWindow(winname)

'''
Segments the given file using textures. Uses 48 texture filters to get
responeses for each pixel, then performs k means on the responses.

params:
    filename: path to image file
return: segmented image
'''
def segmentImg(filename):
    img_src = cv.imread(filename)
    img_gs = cv.cvtColor(img_src, cv.COLOR_BGR2GRAY)
    img_dest = img_gs.copy()
    img_lab = img_src.copy()
    img_lab = cv.cvtColor(img_src, cv.COLOR_BGR2Lab)
    height, width = img_gs.shape

    bank = makeLMfilters.makeLMfilters()
    fx,fy,fz = bank.shape
    responses = np.zeros((fz, height, width), np.uint8)

    # Apply filters
    for i in range(0,fz):
        cv.filter2D(src=img_gs, ddepth=-1, dst=img_dest, kernel=bank[:,:,i], anchor=(-1,-1))
        responses[i] = img_dest

    kmeans_in = np.zeros((height*width, fz))
    ms_in = np.zeros((height*width, 3))
    ind_1d = 0

    # reshape responses so it can be fed to kmeans
    for i in range(0, height):
        for j in range(0, width):
            ms_in[ind_1d] = img_lab[i,j]
            for k in range(0, fz):
                kmeans_in[ind_1d,k] = responses[k,i,j]
            ind_1d += 1
    clusties = KMeans(n_clusters=10).fit(kmeans_in)
    #clusties = MeanShift().fit(ms_in)
    #ret, imgf = cv.threshold(img_gs, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)
    #show_wait_destroy("otsu",imgf)

    labels = clusties.labels_
    labels = labels.astype(np.uint8)
    labels = np.reshape(labels, (height,width))
    cv.imwrite("seg.png",labels)
    return labels

'''
Reads image specified by command line args and segments it.
Saves color version of segmentation for evaluating clustering and
greyscale version for feeding into the transfer function

params:
    argv[1]: filename
'''
def main(argv):
    src = argv[1]
    seg = segmentImg(src)
    color = np.zeros((16,3),np.uint8)
    color[0] = [0,0,100]
    color[1] = [0,100,0]
    color[2] = [100,0,0]
    color[3] = [100,0,100]
    color[4] = [0,100,100]
    color[5] = [100,100,0]
    color[6] = [50,0,100]
    color[7] = [0,50,100]
    color[8] = [0,100,50]
    color[9] = [50,50,100]
    color[10] = [255,0,0]
    color[11] = [0,255,0]
    color[12] = [0,0,255]
    color[13] = [255,255,0]
    color[14] = [255,0,255]
    color[15] = [0,255,255]
    seg_color = cv.cvtColor(seg, cv.COLOR_GRAY2BGR)
    h, w = seg.shape
    for i in range(0, h):
        for j in range(0, w):
            seg_color[i,j] = color[seg[i,j]]
    cv.imwrite("seg_color.png",seg_color)

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Usage: python transfer.py seg src dest")
    else:
        main(sys.argv)
