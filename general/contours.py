import cv2
import numpy as np

def draw_contours(img, contours, col=(0,0,255), thickness=1):
    """

    :param img:
    :param contours:
    :param col: Can be a defined colour in colors.py or a list of tuples(3,1) of colors of length contours
    :param thickness: -1 fills the contour.
    :return:
    """
    if (np.size(np.shape(col)) == 0) | (np.size(np.shape(col)) == 1):
        img = cv2.drawContours(img, contours, -1, col, thickness)
    else:
        for i, contour in enumerate(contours):
            img = cv2.drawContours(img, contour, -1, col[i], thickness)
    return img

def find_contours(img, hierarchy=False):
    """
    contours is a tuple containing (img, contours)
    """
    # work for any version of opencv
    try:
        im, contours, hier = cv2.findContours(
            img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    except:
        contours, hier = cv2.findContours(
            img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if hierarchy:
        return contours, hier
    else:
        return contours

def sort_contours(cnts):
    """
    Sorts contours by area from smallest to largest.

    Parameters
    ----------
    cnts: list
        List containing contours.

    Returns
    -------
    cnts_new: list
        List of input contours sorted by area.
    """
    area = []
    for cnt in cnts:
        area.append(cv2.contourArea(cnt))
    sorted = np.argsort(area)
    cnts_new = []
    for arg in sorted:
        cnts_new.append(cnts[arg])
    return cnts_new