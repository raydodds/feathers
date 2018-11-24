import sys
import cv2 as cv
import numpy as np

HORIZONTAL_STRUC_DIV = 15
VERTICAL_STRUC_DIV = 15

def show_wait_destroy(winname, img):
    cv.imshow(winname, img)
    cv.moveWindow(winname, 500, 0)
    cv.waitKey(0)
    cv.destroyWindow(winname)

'''
Based on code from:
https://docs.opencv.org/3.2.0/d1/dee/tutorial_moprh_lines_detection.html

Returns a binarized image where white pixels represent the feather.
'''
def feather_pix(img_src):
    img_gs = cv.cvtColor(img_src, cv.COLOR_BGR2GRAY)
    ret, img_bin = cv.threshold(img_gs, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)
    h, w, ch = img_src.shape
    img_gs = cv.cvtColor(img_src, cv.COLOR_BGR2GRAY)
    #show_wait_destroy("thrsh", img_bin)
    hor = img_bin.copy()
    vert = img_bin.copy()

    h_size = w / HORIZONTAL_STRUC_DIV
    v_size = h / VERTICAL_STRUC_DIV

    h_struct = cv.getStructuringElement(cv.MORPH_RECT, (h_size, 1))
    v_struct = cv.getStructuringElement(cv.MORPH_RECT, (1, v_size))

    hor = cv.erode(hor, h_struct)
    #show_wait_destroy("hor_erode", hor)
    hor = cv.dilate(hor, h_struct)
    #show_wait_destroy("hor", hor)

    vert = cv.erode(vert, v_struct)
    vert = cv.dilate(vert, v_struct)
    #vert = cv.bitwise_not(vert)
    #show_wait_destroy("vert", vert)

    img_out = np.zeros((h,w),np.uint8)
    for i in range(0, h):
        for j in range(0, w):
            if(hor[i,j] == 255 and vert[i,j] == 255):
                img_out[i,j] = 255
            else:
                img_out[i,j] = 0
    ret, outout = cv.threshold(img_out, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)

    outout = cv.medianBlur(outout, 5)

    if(img_src[0,0,0]):
        outout = cv.bitwise_not(outout)

    #show_wait_destroy("out",outout)

    return outout

def main(argv):
    img_src = cv.imread(argv[1], cv.IMREAD_COLOR)
    feather_pix(img_src)

if __name__ == "__main__":
    if(len(sys.argv) < 1):
        print("Usage: python test.py filename")
    else:
        main(sys.argv)
