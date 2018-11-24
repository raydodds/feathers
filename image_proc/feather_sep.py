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

def separate_black(img_src):
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
    #for i in range (0, len(feathers)):
    #    show_wait_destroy("feather", feathers[i])
    #plt.plot(sig)
    plt.show()
    #plt.savefig('signal.png')

def separate_blue(img_src):
    h, w, ch = img_src.shape
    #img_gs = cv.cvtColor(img_src, cv.COLOR_BGR2GRAY)

    sig_y = np.zeros(h)
    for i in range (0, h):
        for j in range (0, w):
            sig_y[i] += img_src[i,j,0]

    #sig_y = smooth(sig_y, 45, 'bartlett')
    sig_y = gaussian_filter(sig_y, 10)
    #plt.plot(sig_y)
    #plt.show()
    maxima_y = argrelextrema(sig_y, np.greater)
    maxima_y = maxima_y[0]
    minima_y = argrelextrema(sig_y, np.less)
    minima_y = minima_y[0]

    big_min = 0
    for min in minima_y:
        if sig_y[min] < sig_y[big_min]:
            big_min = min

    bottom_cut = 0
    top_cut = 0
    for i in range(0, len(maxima_y) - 1):
        if maxima_y[i] < big_min and maxima_y[i+1] > big_min:
            bottom_cut = maxima_y[i]
            top_cut = maxima_y[i+1]
    print(bottom_cut, top_cut)

    img_src = img_src[bottom_cut:top_cut, 0:w]
    #show_wait_destroy("src",img_src)

    h, w, ch = img_src.shape
    #img_gs = cv.cvtColor(img_src, cv.COLOR_BGR2GRAY)
    sig = np.zeros(w)
    for i in range (0, w):
        for j in range (0, h):
            sig[i] += img_src[j,i,0]

    #sig = smooth(sig, 30, 'blackman')
    sig = gaussian_filter(sig, 5)
    minima = argrelextrema(sig, np.greater)
    minima = minima[0]
    #print(minima)

    img_src = img_src[0:h, minima[1]:w]
    #show_wait_destroy("src",img_src)

    h, w, ch = img_src.shape
    #img_gs = cv.cvtColor(img_src, cv.COLOR_BGR2GRAY)
    sig = np.zeros(w)
    for i in range (0, w):
        for j in range (0, h):
            sig[i] += img_src[j,i,0]

    sig = gaussian_filter(sig, 5)
    maxima = argrelextrema(sig, np.greater)
    maxima = maxima[0]

    show_wait_destroy("ass",img_src)
    #print(minima_y)
    #print(bottom_cut,top_cut)
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

    #print(len(feathers))
    #for i in range (0, len(feathers)):
    #    show_wait_destroy("feather", feathers[i])
    #plt.plot(sig)
    plt.show()
    #plt.savefig('signal.png')

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
