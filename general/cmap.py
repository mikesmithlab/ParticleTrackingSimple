import matplotlib.pyplot as plt
import numpy as np




def cmap(colour_data cmap_type=None):
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

    cmap_type = parameters[annotation_method]['cmap type']
    if cmap_type == 'discrete':
        cmap_name = 'Set1'
    elif cmap_type == 'continuous':
        cmap_name = 'seismic'

    colour_obj = plt.get_cmap(cmap_name, np.size)



    data_column = data.get_info(f, col_name)


if __name__=='__main__':
    colour = plt.get_cmap('Set1',2)
    print(colour(np.array([0.01,0.1])))