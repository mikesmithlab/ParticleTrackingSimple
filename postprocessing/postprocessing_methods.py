import pandas as pd
import numpy as np
from ParticleTrackingSimple.general import dataframes
import trackpy as tp
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
    data=data.sort_values(['particle','index'])
    data[output_name] = data[column].diff(periods=span)
    data['nan'] = data['particle'].diff(periods=span).astype(bool)
    data[output_name][data['nan'] == True] = np.NaN
    data.drop(labels='nan',axis=1)
    return data



def magnitude(data, parameters=None, call_num=None):
    method_key=get_method_key('magnitude', call_num)
    columns = parameters[method_key]['column_names']
    column_data=data.get_info(columns)

def rate(data, parameters=None, call_num=None):
    method_key = get_method_key('rate', call_num)
    column = parameters[method_key]['column_name']
    output_name = parameters[method_key]['output_name']
    data = data.sort_values(['particle', 'index'])
    data['temp_diff'] = data[column].diff()
    data['nan'] = data['particle'].diff().astype(bool)
    data['temp_diff'][data['nan'] == True] = np.NaN
    #Something like the central difference method
    data['frame'] = data.index
    data[output_name + '_gaps']=data['frame'].diff()
    data[data[output_name + '_gaps'] < 0][output_name + '_gaps'] == np.NaN
    data[output_name] = data['temp'] / data[output_name + '_gaps']
    data.drop(labels=['nan','temp','frame'], axis=1)
    return data

def neighbours(data, parameters=None, call_num=None,):
    method_key = get_method_key('neighbours', call_num)
    pass
    return data

def classify(data, parameters=None, call_num=None):
    method_key = get_method_key('classify', call_num)
    pass
    return data
