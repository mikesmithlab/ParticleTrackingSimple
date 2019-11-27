from ParticleTrackingSimple.general.parameters import get_param_val
from ParticleTrackingSimple.annotation.cmap import colourmap, cmap_variables
from ParticleTrackingSimple.general.contours import draw_contours
from ParticleTrackingSimple.general.parameters import get_method_key
import cv2
import numpy as np
import pandas as pd


'''
--------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------
Text annotation
--------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------
'''

def text_label(frame, data, f, parameters=None, call_num=None):
    '''
    Function puts text on an image at specific location.
    This function is for adding metadata or info not labelling
    particles with their ids.

    :param frame: frame to be annotated should be 3 colour channel
    :param data: datastore with particle information
    :param f: frame number
    :param parameters: annotation sub dictionary

    :return: annotated frame
    '''
    method_key = get_method_key('text_label', call_num=call_num)
    text=parameters[method_key]['text']
    position = parameters[method_key]['position']
    annotated_frame=cv2.putText(frame, text, position, cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                parameters[method_key]['font_size'],
                                parameters[method_key]['font_colour'],
                                parameters[method_key]['font_thickness'],
                                cv2.LINE_AA)

    return annotated_frame

def var_label(frame, data, f, parameters=None, call_num=None):
    '''
    Function puts text on an image at specific location.
    This function is for adding data specific to a single frame or info not labelling
    particles with their ids. The data for a given frame should be stored in 'var_column'
    ie all particles have this value stored. You could use it to put the "temperature" on
    a frame or the mean order parameter etc. Calling 'index' will place the

    :param frame: frame to be annotated should be 3 colour channel
    :param data: datastore with particle information
    :param f: frame number
    :param parameters: annotation sub dictionary.

    :return: annotated frame
    '''
    method_key = get_method_key('var_label', call_num=call_num)
    var_column=parameters[method_key]['var_column']
    text = str(data.get_info(f, var_column)[0])
    position = parameters[method_key]['position']

    annotated_frame=cv2.putText(frame, text, position, cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                parameters[method_key]['font_size'],
                                parameters[method_key]['font_colour'],
                                parameters[method_key]['font_thickness'],
                                cv2.LINE_AA)

    return annotated_frame

def particle_values(frame, data, f, parameters=None, call_num=None):
    '''
        Function annotates image with particle ids
        This function only makes sense if run on linked trajectories

        :param frame: frame to be annotated should be 3 colour channel
        :param data: datastore with particle information
        :param f: frame number
        :param parameters: annotation sub dictionary

        :return: annotated frame
        '''
    method_key = get_method_key('particle_values', call_num=None)
    x = data.get_info(f, 'x')
    y = data.get_info(f, 'y')

    particle_values = data.get_info(f, parameters[method_key]['values_column']).astype(int)

    for index, particle_val in enumerate(particle_values):
        frame = cv2.putText(frame, str(particle_val), (int(x[index]), int(y[index])),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL,
                            parameters[method_key]['font_size'],
                            parameters[method_key]['font_colour'],
                            parameters[method_key]['font_thickness'],
                            cv2.LINE_AA)

    return frame


'''
--------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------
Particle annotation
--------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------
'''
def circles(frame, data, f, parameters=None, call_num=None):
    '''
    Function draws circles on an image at x,y locations. If data.df['r'] exists
    circles have this radius, else 'r' col is created with value set from annotation
    sub dictionary.

    :param frame: frame to be annotated should be 3 colour channel
    :param data: datastore with particle information
    :param f: frame number
    :param parameters: annotation sub dictionary

    :return: annotated frame
    '''
    method_key = get_method_key('circles', call_num=call_num)
    if 'r' not in list(data.df.columns):
        data.add_particle_property('r', get_param_val(parameters[method_key]['radius']))

    thickness = get_param_val(parameters[method_key]['thickness'])

    circles = data.df.loc[f, ['x', 'y', 'r']].values
    print(circles)

    colour_data, cmap_type, cmax_max = cmap_variables(data, f, parameters, method=method_key)
    colours = colourmap(colour_data, cmap_type=cmap_type,cmax_max=cmax_max)

    for i, circle in enumerate(circles):
        try:
            frame = cv2.circle(frame, (int(circle[0]), int(circle[1])), int(circle[2]), colours[i], thickness)
        except:
            print('Failed plotting circle, check data is valid')
            print(circle)
    return frame

#Not yet working
def boxes(frame, data, f, parameters=None, call_num=None):
    method_key = get_method_key('boxes', call_num=call_num)
    #Requires a column classifying traj with corresponding colour
    box = data.get_info(f, 'box')
    classifiers = data.get_info(f,'classifier')
    for index, classifier in enumerate(classifiers):
       annotated_frame = draw_contours(frame, [
                                 box[index]], col=get_param_val(parameters['colors'])[classifier],
                                       thickness=get_param_val(parameters['contour thickness']))
    return annotated_frame

def contours(frame, data, f, parameters=None, call_num=None):
    method_key = get_method_key('contours', call_num=call_num)
    return annotated_frame

def networks(frame, data, f, parameters=None, call_num=None):
    method_key = get_method_key('networks', call_num=call_num)
    df = data.df.loc[f]
    df=df.set_index('particle')
    particle_ids = df.index.values
    colour = parameters[method_key]['colour']
    thickness = parameters[method_key]['thickness']
    for index, particle in enumerate(particle_ids):
        pt = df.loc[particle, ['x', 'y']].values
        pt1 = (int(pt[0]), int(pt[1]))
        # neighbour_ids = df['neighbours'].loc(particle)
        neighbour_ids = df.loc[particle, 'neighbours']
        for index2, neighbour in enumerate(neighbour_ids):
            pt = df.loc[neighbour, ['x','y']].values
            pt2 = (int(pt[0]), int(pt[1]))
            frame = cv2.line(frame,pt1, pt2, colour, thickness, lineType=cv2.LINE_AA)
    return frame
'''
--------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------
Particle motion annotation
--------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------
'''
def vectors(frame, data, f, parameters=None, call_num=None):
    method_key = get_method_key('vectors', call_num=call_num)
    dx = parameters[method_key]['dx_column']
    dy = parameters[method_key]['dy_column']

    vectors = data.get_info(f, ['x', 'y',dx, dy])

    thickness = get_param_val(parameters[method_key]['thickness'])
    line_type = 8
    tipLength = 0.01*get_param_val(parameters[method_key]['tip_length'])
    vector_scale = 0.01*get_param_val(parameters[method_key]['vector_scale'])


    colour_data, cmap_type, cmax_max = cmap_variables(data, f, parameters, method=method_key)
    colours = colourmap(colour_data, cmap_type=cmap_type,cmax_max=cmax_max)

    for i, vector in enumerate(vectors):
        frame = cv2.arrowedLine(frame, (int(vector[0]), int(vector[1])),
                                (int(vector[0]+vector[2]*vector_scale),int(vector[1]+vector[3]*vector_scale)),
                                color=colours[i], thickness=thickness,line_type=line_type,shift=0,tipLength=tipLength)
    return frame

def trajectories(frame, data, f, parameters=None, call_num=None):
    #This can only be run on a linked trajectory
    method_key = get_method_key('trajectories', call_num=call_num)
    traj_length = get_param_val(parameters[method_key]['traj_length'])
    if f-traj_length < 0:
        traj_length = f

    df = data.df.sort_index()
    df.index.name='frame'
    df['frame'] = df.index
    df2 = df.loc[f-traj_length:f]

    classifier_column = parameters[method_key]['classifier_column']
    classifier = parameters[method_key]['classifier']

    if classifier_column is None:
        df2 = df2.loc[:, ['x', 'y', 'particle']]
        particle_ids = df2.loc[f,'particle'].values
    else:
        classifier_select = df2.loc[f, classifier_column]
        df2 = df2.loc[:, ['x', 'y', 'particle', classifier_column]]
        particle_ids = df2.loc[f, 'particle'].values
        particle_ids=particle_ids[classifier_select == classifier]

    df3 = df2.set_index('particle','frame').sort_index()

    colour_data, cmap_type, cmax_max = cmap_variables(data, f, parameters, method=method_key)
    colours = colourmap(colour_data, cmap_type=cmap_type, cmax_max=cmax_max)
    thickness = get_param_val(parameters[method_key]['thickness'])

    for index, particle in enumerate(particle_ids):
        traj_pts = df3.loc[particle].values
        traj_pts = np.array(traj_pts, np.int32).reshape((-1,1,2))

        frame = cv2.polylines(frame,[traj_pts],False,colours[index],thickness)

    return frame

