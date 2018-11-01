import sys
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from scipy.ndimage import gaussian_filter

HORIZONTAL_STRUC_DIV = 15
VERTICAL_STRUC_DIV = 15

def show_wait_destroy(winname, img):
    cv.imshow(winname, img)
    cv.moveWindow(winname, 500, 0)
    cv.waitKey(0)
    cv.destroyWindow(winname)

def main(argv):
    img_src = cv.imread(argv[1], cv.IMREAD_COLOR)
    h, w, ch = img_src.shape
    img_gs = cv.cvtColor(img_src, cv.COLOR_BGR2GRAY)

    sig_y = np.zeros(h)
    for i in range (0, h):
        for j in range (0, w):
            sig_y[i] += img_gs[i,j]

    #sig_y = smooth(sig_y, 45, 'bartlett')
    sig_y = gaussian_filter(sig_y, 10)
    maxima_y = argrelextrema(sig_y, np.greater)
    maxima_y = maxima_y[0]
    minima_y = argrelextrema(sig_y, np.less)
    minima_y = minima_y[0]

    big_max = 0
    for max in maxima_y:
        if sig_y[max] > sig_y[big_max]:
            big_max = max

    bottom_cut = 0
    top_cut = 0
    for i in range(0, len(minima_y) - 1):
        if minima_y[i] < big_max and minima_y[i+1] > big_max:
            bottom_cut = minima_y[i]
            top_cut = minima_y[i+1]
    print(bottom_cut, top_cut)

    img_src = img_src[bottom_cut:top_cut, 0:w]

    h, w, ch = img_src.shape
    img_gs = cv.cvtColor(img_src, cv.COLOR_BGR2GRAY)
    sig = np.zeros(w)
    for i in range (0, w):
        for j in range (0, h):
            sig[i] += img_gs[j,i]

    #sig = smooth(sig, 30, 'blackman')
    sig = gaussian_filter(sig, 5)
    minima = argrelextrema(sig, np.greater)
    minima = minima[0]
    #print(minima)

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

    show_wait_destroy("ass",img_src)
    #print(minima_y)
    #print(bottom_cut,top_cut)
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

    #print(len(feathers))
    for i in range (0, len(feathers)):
        show_wait_destroy("feather", feathers[i])
    plt.plot(sig)
    plt.show()
    #plt.savefig('signal.png')

if __name__ == "__main__":
    if(len(sys.argv) < 1):
        print("Usage: python test.py filename")
    else:
        main(sys.argv)
