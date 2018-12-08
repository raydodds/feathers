import sys
import cv2 as cv
import numpy as np
from scipy.signal import argrelextrema
from scipy.ndimage import gaussian_filter

HORIZONTAL_STRUC_DIV = 15
VERTICAL_STRUC_DIV = 15

'''

Separate feathers in a black background image

'''
def separate_black(img_src):
	h, w, ch = img_src.shape
	img_gs = cv.cvtColor(img_src, cv.COLOR_BGR2GRAY)

	sig_y = np.zeros(h)
	for i in range (0, h):
		for j in range (0, w):
			sig_y[i] += img_gs[i,j]

	sig_y = gaussian_filter(sig_y, 10)
	maxima_y = argrelextrema(sig_y, np.greater)
	maxima_y = maxima_y[0]
	minima_y = argrelextrema(sig_y, np.less)
	minima_y = minima_y[0]

	big_max = 0
	for maxx in maxima_y:
		if sig_y[maxx] > sig_y[big_max]:
			big_max = maxx

	min_left = big_max
	min_right = big_max
	for minn in minima_y:
		if minn < big_max and sig_y[minn] < sig_y[min_left]:
			min_left = minn
		if minn > big_max and sig_y[minn] < sig_y[min_right]:
			min_right = minn

	if min_left == big_max:
		min_left = 50
	if min_right == big_max:
		min_right = h - 100

	img_src = img_src[min_left:min_right, 0:w]

	h, w, ch = img_src.shape
	img_gs = cv.cvtColor(img_src, cv.COLOR_BGR2GRAY)
	sig = np.zeros(w)
	for i in range (0, w):
		for j in range (0, h):
			sig[i] += img_gs[j,i]

	sig = gaussian_filter(sig, 5)
	minima = argrelextrema(sig, np.greater)
	minima = minima[0]

	img_src = img_src[0:h, minima[1]:w]

	h, w, ch = img_src.shape
	img_gs = cv.cvtColor(img_src, cv.COLOR_BGR2GRAY)
	sig = np.zeros(w)
	for i in range (0, w):
		for j in range (0, h):
			sig[i] += img_gs[j,i]

	sig = gaussian_filter(sig, 5)
	minima = argrelextrema(sig, np.less)
	minima = minima[0]

	feathers = []
	for i in range (0, len(minima) - 1):
		new_feath = img_src[0:h, minima[i]:minima[i+1]]
		fh,fw,fc = new_feath.shape
		if(fh > 0 and fw > 0):
			cv.imwrite("f"+str(i)+".png",new_feath)
			feathers.append(new_feath)

	new_feath = img_src[0:h, minima[len(minima)-1]:w]
	fh,fw,fc = new_feath.shape
	if(fh > 0 and fw > 0):
		cv.imwrite("f"+str(len(minima)-1)+".png",new_feath)
		feathers.append(new_feath)

'''

Separate feathers in a blue background image

'''
def separate_blue(img_src):
	h, w, ch = img_src.shape

	sig_y = np.zeros(h)
	for i in range (0, h):
		for j in range (0, w):
			sig_y[i] += img_src[i,j,0]

	sig_y = gaussian_filter(sig_y, 10)
	maxima_y = argrelextrema(sig_y, np.greater)
	maxima_y = maxima_y[0]
	minima_y = argrelextrema(sig_y, np.less)
	minima_y = minima_y[0]

	big_min = 0
	for min in minima_y:
		if sig_y[min] < sig_y[big_min]:
			big_min = min

	max_left = big_min
	max_right = big_min
	for maxx in minima_y:
		if maxx < big_min and sig_y[maxx] > sig_y[max_left]:
			max_left = maxx
		if maxx > big_min and sig_y[maxx] > sig_y[max_right]:
			max_right = maxx

	if max_left == big_min:
		max_left = 50
	if max_right == big_min:
		max_right = h - 100

	img_src = img_src[max_left:max_right, 0:w]

	h, w, ch = img_src.shape
	sig = np.zeros(w)
	for i in range (0, w):
		for j in range (0, h):
			sig[i] += img_src[j,i,0]

	sig = gaussian_filter(sig, 5)
	minima = argrelextrema(sig, np.greater)
	minima = minima[0]

	img_src = img_src[0:h, minima[1]:w]

	h, w, ch = img_src.shape
	sig = np.zeros(w)
	for i in range (0, w):
		for j in range (0, h):
			sig[i] += img_src[j,i,0]

	sig = gaussian_filter(sig, 5)
	maxima = argrelextrema(sig, np.greater)
	maxima = maxima[0]

	feathers = []
	for i in range (0, len(maxima) - 1):
		new_feath = img_src[0:h, maxima[i]:maxima[i+1]]
		fh,fw,fc = new_feath.shape
		if(fh > 0 and fw > 0):
			cv.imwrite("f"+str(i)+".png",new_feath)
			feathers.append(new_feath)

	new_feath = img_src[0:h, maxima[len(maxima)-1]:w]
	fh,fw,fc = new_feath.shape
	if(fh > 0 and fw > 0):
		cv.imwrite("f"+str(len(maxima)-1)+".png",new_feath)
		feathers.append(new_feath)

'''

Direct flow to correct background color separation function

'''
def main(argv):
	img_src = cv.imread(argv[1], cv.IMREAD_COLOR)
	if(img_src[0,0,0] > 50):
		separate_blue(img_src)
	else:
		separate_black(img_src)


if __name__ == "__main__":
	if(len(sys.argv) < 1):
		print("Usage: python test.py filename")
	else:
		main(sys.argv)
