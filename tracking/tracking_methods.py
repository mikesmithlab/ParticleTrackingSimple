import cv2
from Generic import images
from Generic.images.basics import display
import numpy as np
import skimage
import trackpy as tp
from ParticleTrackingSimple.general.parameters import get_param_val, get_method_key
import pandas as pd



def trackpy(frame, parameters=None, call_num=None):
    method_key = get_method_key('trackpy', call_num)
    df = tp.locate(frame, get_param_val(parameters[method_key]['size_estimate']), invert=get_param_val(parameters[method_key]['invert']))
    return df

def hough(frame, parameters=None, call_num=None):
    method_key = get_method_key('hough', call_num)

    circles = images.find_circles(
                frame,
                get_param_val(parameters[method_key]['min_dist']),
                get_param_val(parameters[method_key]['p1']),
                get_param_val(parameters[method_key]['p2']),
                get_param_val(parameters[method_key]['min_rad']),
                get_param_val(parameters[method_key]['max_rad']))

    try:
        circles_dict = {'x': circles[:, 0], 'y': circles[:, 1], 'r': circles[:, 2]}
    except:
        circles_dict={'x':[1],'y':[1],'r':[5]}
    df = pd.DataFrame(circles_dict)
    return df

def contours(frame, parameters=None):
    method_key = get_method_key('contours',call_num=None)
    info = []
    contours = images.find_contours(frame)
    for index, contour in enumerate(contours):
        info_contour = images.rotated_bounding_rectangle(contour)
        info_contour[0], info_contour[1] = np.mean(info_contour[5], axis=0)
        info.append(info_contour)
    info_headings = ['x', 'y', 'theta', 'width', 'length', 'box']
    df = pd.DataFrame(data=info, columns=info_headings)
    return df


