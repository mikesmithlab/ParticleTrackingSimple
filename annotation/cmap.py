import matplotlib.pyplot as plt
import numpy as np
from ParticleTrackingSimple.general.parameters import get_param_val

def cmap_variables(data, f, parameters, method=None):
    '''
    Convenience method to extract the inputs necessary for building a colourmap

    :param data: DataStore
    :param f: frame number
    :param parameters: annotation parameters dictionary
    :param method: String of the method being used to annotate

    :return: Numpy array of data to be used in colour coding, type of colour map, maximum value to scale data.
    '''
    colour_data = data.get_info(f, parameters[method]['cmap_column'])
    cmap_type = parameters[method]['cmap_type']
    cmax_max = get_param_val(parameters[method]['cmap_max'])
    return colour_data, cmap_type, cmax_max

def colourmap(colour_data, cmap_type=None, cmax_max=None):
    '''
    cmap could have different use cases:
    1: 'discrete' data is colour coded according to some classifier
    2: 'continuous' data is colour coded according to continuous scale

    Colormap definitions: https://matplotlib.org/3.1.1/gallery/color/colormap_reference.html
    case 1 colourmap is Set1 of Matplotlibs Qualitative color maps
    case 2 colourmap is seismic from diverging colormaps


    :param data: Datastore object containing column upon which to perform the mapping
    :param f: integer specifying frame number
    :param col_name: string specifying column in dataframe of Datastore which supplies values for colour coding
    :param parameters: Dictionary specifying parameters

    :return: a
    '''

    if cmap_type == 'discrete':
        cmap_name = 'Set1'
    elif cmap_type == 'continuous':
        cmap_name = 'jet'
    else:
        cmap_name = cmap_type

    if cmax_max is None:
        cmax_max = np.max(colour_data)

    colour_obj = plt.get_cmap(cmap_name, np.size(colour_data))
    colour_vals = 255*colour_obj(colour_data/cmax_max)
    colours=[]
    for colour in colour_vals:
        colours.append((colour[0],colour[1],colour[2]))
    return np.array(colours)




if __name__=='__main__':
    colour = plt.get_cmap('Set1',2)
    print(colour(np.array([0.01,0.1])))