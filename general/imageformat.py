import numpy as np
import cv2

def bgr_2_grayscale(img):
    """Converts a BGR image to grayscale"""
    sz = np.shape(img)
    if np.shape(sz)[0] == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if np.shape(sz)[0] == 2:
        print('Image is already grayscale')
        return img


def stack_3(img):
    """Stacks a grayscale image to 3 depths so that coloured objects
    can be drawn on top"""
    im = np.dstack((img, img, img))
    return im

def get_depth(img):
    shp = np.shape(img)
    if len(shp) == 2:
        return 1
    else:
        return shp[2]
