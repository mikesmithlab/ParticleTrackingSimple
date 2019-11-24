import numpy as np
from ParticleTrackingSimple.general.parameters import get_method_key


def smooth(data, parameters=None, call_num=None):
    method_key = get_method_key('smooth', call_num)
    #Rolling average smoothing param.
    pass
    return data

def difference(data, parameters=None, call_num=None):
    '''Returns frame with new column of rolling differences
       The differences are calculated at separations equal
       to span. Where this is not possible the value np.Nan
       is inserted.
    '''
    method_key = get_method_key('difference', call_num)
    span = parameters[method_key]['span']
    column = parameters[method_key]['column_name']
    output_name = parameters[method_key]['output_name']

    data[output_name] = data[column].diff(periods=span)
    data['nan'] = data['particle'].diff(periods=span).astype(bool)
    data[output_name][data['nan'] == True] = np.NaN
    data.drop(labels='nan',axis=1)
    return data

def rate(data, parameters=None, call_num=None):
    '''
    rate function takes an input column and calculates the
    rate of change of the quantity. It takes into account
    the fact that particles go missing from frames. Where this
    is the case the rate = change in quantity between observations
    divided by the gap between observations.
    Nans are inserted at end and beginning of particle trajectories
    where calc is not possible.

    We sort by particle and then calculate diffs. This leads to differences
    between pairs of particles above one another in dataframe. We then backfill
    these slots with Nans.

    :param data:
    :param parameters:
    :param call_num:
    :return:
    '''
    method_key = get_method_key('rate', call_num)
    column = parameters[method_key]['column_name']
    output_name = parameters[method_key]['output_name']

    data = data.sort_values(['particle', 'index'])
    #Change and time over which change happened
    data['temp_diff'] = data[column].diff()
    data['nan'] = data['particle'].diff().astype(bool)
    data['temp_diff'][data['nan'] == True] = np.NaN
    data['time'] = (1/parameters[method_key]['fps'])*data.index
    data['dt']=data['time'].diff()
    #Put Nans in values crossing particles.
    data[data['dt'] < 0]['dt'] == np.NaN
    data[output_name] = data['temp_diff'] / data['dt']
    #remove temporary columns
    data.drop(labels=['nan','temp_diff','dt'], axis=1)
    return data

def magnitude(data, parameters=None, call_num=None):
    method_key=get_method_key('magnitude', call_num)
    columns = parameters[method_key]['column_names']
    output_name = parameters[method_key]['output_name']
    column_data=data[columns]
    if np.size(columns) == 2:
        data[output_name] = (column_data[columns[0]]**2 + column_data[columns[1]]**2)**0.5
    elif np.size(columns) == 3:
        data[output_name] = (column_data[columns[0]]**2 + column_data[columns[1]]**2 + column_data[columns[2]]**2)**0.5
    return data

def angle(data, parameters=None, call_num=None):
    '''
    angle assumes you want to calculate from column_data[0] as x and column_data[1] as y
    it uses tan2 so that -x and +y give a different result to +x and -y
    Angles are output in radians or degrees given by parameters['angle']['units']

    :param data: dataframe input
    :param parameters: dictionary of params
    :param call_num:

    :return: dataframe with new angle column.
    '''
    method_key = get_method_key('angle', call_num)
    columns = parameters[method_key]['column_names']
    output_name = parameters[method_key]['output_name']
    data[output_name] = np.arctan2(data[columns[0]]/data[data[columns[1]]])
    return data

def neighbours(data, parameters=None, call_num=None,):
    method_key = get_method_key('neighbours', call_num)
    pass
    return data

def classify(data, parameters=None, call_num=None):
    method_key = get_method_key('classify', call_num)
    column = parameters[method_key]['column_name']
    output_name=parameters[method_key]['output_name']
    data[output_name] = 1
    return data
