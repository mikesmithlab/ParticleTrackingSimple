import cv2
import numpy as np
import trackpy as tp
from ParticleTrackingSimple.general.parameters import get_param_val, get_method_key
import pandas as pd


def trackpy(frame, parameters=None, call_num=None):
    method_key = get_method_key('trackpy', call_num)
    df = tp.locate(frame, get_param_val(parameters[method_key]['size_estimate']), invert=get_param_val(parameters[method_key]['invert']))
    return df

def hough(frame, parameters=None, call_num=None):
    method_key = get_method_key('hough', call_num)

    circles = np.squeeze(cv2.HoughCircles(
        frame,
        cv2.HOUGH_GRADIENT, 1,
        get_param_val(parameters[method_key]['min_dist']),
        get_param_val(parameters[method_key]['p1']),
        get_param_val(parameters[method_key]['p2']),
        get_param_val(parameters[method_key]['min_rad']),
        get_param_val(parameters[method_key]['max_rad'])))

    try:
        circles_dict = {'x': circles[:, 0], 'y': circles[:, 1], 'r': circles[:, 2]}
    except:
        circles_dict={'x':[1],'y':[1],'r':[5]}
    df = pd.DataFrame(circles_dict)
    return df


def boxes(frame, parameters=None, call_num=None):
    '''
    boxes method finds contour of object but reduces the info to
    a rotated bounding box. Use for finding an angle of object or
    estimate of size. If you need to do something with the pixels
    use contours instead.
    '''
    method_key = get_method_key('boxes',call_num=call_num)
    params = parameters[method_key]
    area_min = get_param_val(params['area_min'])
    area_max = get_param_val(params['area_max'])
    info = []
    contour_pts = _find_contours(frame)
    for index, contour in enumerate(contour_pts):
        area = cv2.contourArea(contour)
        if (area < area_max) & (area >= area_min):
            info_contour = _rotated_bounding_rectangle(contour)
            info_contour[0], info_contour[1] = np.mean(info_contour[5], axis=0)
            info.append(info_contour)
    info_headings = ['x', 'y', 'theta', 'width', 'length', 'box']
    df = pd.DataFrame(data=info, columns=info_headings)
    return df

def contours(frame, parameters=None, call_num=None):
    '''
    boxes method finds contour of object but reduces the info to
    a rotated bounding box. Use for finding an angle of object or
    estimate of size. If you need to do something with the pixels
    use contours instead.

    contours stores: the centroid cx, cy, area enclosed by contour,
    the bounding rectangle which is used with contour to generate
    mask so that you can extract pixels from original image
    and perform some analysis.
    '''
    method_key = get_method_key('contours',call_num=call_num)
    params = parameters[method_key]
    area_min = get_param_val(params['area_min'])
    area_max = get_param_val(params['area_max'])
    info = []
    contour_pts = _find_contours(frame)
    for index, contour in enumerate(contour_pts):
        M = cv2.moments(contour)
        if M['m00'] > 0:
            area = cv2.contourArea(contour)
            if (area < area_max) & (area > area_min):
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                box = cv2.boundingRect(contour)
                info_contour = [cx, cy, area, contour, box]
                info.append(info_contour)
    info_headings = ['x', 'y', 'area', 'contours', 'boxes']
    df = pd.DataFrame(data=info, columns=info_headings)
    return df


'''
------------------------------------------------------------------------
Supporting functions
------------------------------------------------------------------------
'''

def _find_contours(img, hierarchy=False):
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

def _rotated_bounding_rectangle(contour):
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    dim = np.sort(rect[1])

    #[centrex, centrey, angle, length, width, box_corners]
    info = [rect[0][0], rect[0][1], rect[2], dim[0], dim[1], box]
    return info