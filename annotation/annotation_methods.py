from ParticleTrackingSimple.general.parameters import get_param_val
from ParticleTrackingSimple.annotation.cmap import colourmap, cmap_variables
from Generic import images
import cv2
import numpy as np

'''
--------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------
Text annotation
--------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------
'''
def text_label(frame, data, f, parameters=None):
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
    text=parameters['text_label']['text']
    position = parameters['text_label']['position']
    annotated_frame=cv2.putText(frame, text, position, cv2.FONT_HERSHEY_COMPLEX, parameters['text_label']['font_size'], parameters['text_label']['font_colour'],parameters['text_label']['font_thickness'], cv2.LINE_AA)

    return annotated_frame

def var_label(frame, data, f, parameters=None):
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

    var_column=parameters['var_label']['var_column']
    text = str(data.get_info(f, var_column)[0])
    position = parameters['var_label']['position']

    annotated_frame=cv2.putText(frame, text, position, cv2.FONT_HERSHEY_COMPLEX, parameters['var_label']['font_size'], parameters['var_label']['font_colour'],parameters['var_label']['font_thickness'], cv2.LINE_AA)

    return annotated_frame

def particle_values(frame, data, f, parameters=None):
    '''
        Function annotates image with particle ids
        This function only makes sense if run on linked trajectories

        :param frame: frame to be annotated should be 3 colour channel
        :param data: datastore with particle information
        :param f: frame number
        :param parameters: annotation sub dictionary

        :return: annotated frame
        '''

    x = data.get_info(f, 'x')
    y = data.get_info(f, 'y')

    particle_values = data.get_info(f, parameters['particle_values']['values_column']).astype(int)

    for index, particle_val in enumerate(particle_values):
        frame = cv2.putText(frame, str(particle_val), (int(x[index]), int(y[index])), cv2.FONT_HERSHEY_COMPLEX, parameters['particle_values']['font_size'], parameters['particle_values']['font_colour'], parameters['particle_values']['font_thickness'], cv2.LINE_AA)

    return frame


'''
--------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------
Particle annotation
--------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------
'''
def circles(frame, data, f, parameters=None):
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

    if 'r' not in list(data.df.columns):
        data.add_particle_property('r', get_param_val(parameters['circles']['radius']))

    thickness = get_param_val(parameters['circles']['thickness'])
    circles = data.get_info(f, ['x', 'y', 'r'])

    colour_data, cmap_type, cmax_max = cmap_variables(data, f, parameters, method='circles')
    colours = colourmap(colour_data, cmap_type=cmap_type,cmax_max=cmax_max)

    for i, circle in enumerate(circles):
        frame = cv2.circle(frame, (int(circle[0]), int(circle[1])), int(circle[2]), colours[i], thickness)
    return frame

#Not yet working
def boxes(frame, data, f, parameters=None):
    #Requires a column classifying traj with corresponding colour
    box = data.get_info(f, 'box')
    classifiers = data.get_info(f,'classifier')
    for index, classifier in enumerate(classifiers):
       annotated_frame = images.draw_contours(frame, [
        box[index]], col=get_param_val(parameters['colors'])[classifier], thickness=get_param_val(parameters['contour thickness']))
    return annotated_frame

def contours(frame, data, f, parameters=None):
    return annotated_frame

def network(frame, data, f, parameters=None):
    return annotated_frame
'''
--------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------
Particle motion annotation
--------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------
'''
def vectors(frame, data, f, parameters=None):

    dx = parameters['vectors']['dx_column']
    dy = parameters['vectors']['dy_column']

    vectors = data.get_info(f, ['x', 'y',dx, dy])

    thickness = get_param_val(parameters['vectors']['thickness'])
    line_type = 8
    tipLength = 0.01*get_param_val(parameters['vectors']['tip_length'])
    vector_scale = 0.01*get_param_val(parameters['vectors']['vector_scale'])


    colour_data, cmap_type, cmax_max = cmap_variables(data, f, parameters, method='vectors')
    colours = colourmap(colour_data, cmap_type=cmap_type,cmax_max=cmax_max)

    for i, vector in enumerate(vectors):
        frame = cv2.arrowedLine(frame, (int(vector[0]), int(vector[1])),
                                (int(vector[0]+vector[2]*vector_scale),int(vector[1]+vector[3]*vector_scale)),
                                color=colours[i], thickness=thickness,line_type=line_type,shift=0,tipLength=tipLength)
    return frame
'''
def trajectories(self, frame, f, parameters=None):
    df = data.df
    #This can only be run on a linked trajectory
    particle_ids = self.data.get_info(f, 'particle')

    df_temp=df[df['particle'].isin(particle_ids)]
    df_temp2 = df_temp[df_temp.index <= f]
    for index, particle in enumerate(particle_ids):
    traj_pts= df_temp2[df_temp2['particle'] == particle][[colx, coly,'classifier']]
    frame = cv2.polylines(frame, np.int32([traj_pts[[colx,coly]].values]), False,
                     self.params['colors'][traj_pts['classifier'].median()],
                     self.params['trajectory thickness'])
    return frame

'''