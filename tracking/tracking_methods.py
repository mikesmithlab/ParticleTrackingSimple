import cv2
from Generic import images
from Generic.images.basics import display
import numpy as np
import skimage
import trackpy as tp
from ParticleTrackingSimple.general.parameters import get_param_val, get_method_key
import pandas as pd



def trackpy(frame, parameters=None, call_num=None):
    method_key = get_method_key('rate', call_num)
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
        info_contour = _classify(contour, parameters[method_key])
        info.append(info_contour)

    info_headings = ['x', 'y', 'theta', 'width', 'length', 'box',
                     'classifier']
    info_out = [info_headings,[info]]
    info_out = dict(zip(*info_out))
    df = pd.DataFrame(data=info, columns=info_headings)
    print(df.columns.to_list())
    print(df.head())
    return df

def _classify(contour, parameters):
    '''
            We fit the bounded rectangle to the bacterium contour
            we then overwrite the x and y coords with contour centre of mass.
            '''
    info = images.rotated_bounding_rectangle(contour)
    info[0], info[1] = np.mean(info[5], axis=0)  # images.find_contour_centre(contour)

    area = info[3] * info[4]
    aspect = 100 * info[4] / info[3]
    if area <= parameters['noise_cutoff'][0]:
        # Too small to be significant, probably noise
        classifier = int(1)
    elif (area > get_param_val(parameters['noise_cutoff'])) & (area <= get_param_val(parameters['area'])) & (
            aspect <= get_param_val(parameters['aspect'])):
        # This is probably a particle.
        classifier = int(2)
    elif (area > get_param_val(parameters['noise_cutoff'])) & (area <= get_param_val(parameters['area'])) & (
            aspect > get_param_val(parameters['aspect'])):
        # This is probably a bacterium
        classifier = int(3)
    elif (area > get_param_val(parameters['area'])):
        # Probably an aggregate
        classifier = int(4)
    else:
        classifier = int(0)
    info.append(classifier)
    return info

def distance(frame, parameters=None):
   dist = cv2.distanceTransform(frame, cv2.DIST_L2, 5)
   display(dist / np.max(dist))
   return dist

