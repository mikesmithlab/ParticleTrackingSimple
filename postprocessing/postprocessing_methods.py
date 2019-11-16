import pandas as pd
import numpy as np
from ParticleTrackingSimple.general import dataframes
import trackpy as tp
from ParticleTrackingSimple.general.parameters import get_method_key


def smooth(data, parameters=None, call_num=None):
    method_key = get_method_key('difference', call_num)
    #Rolling average smoothing param.
    pass
    return data

def difference(data, parameters=None, call_num=None):
    method_key = get_method_key('difference', call_num)
    span = parameters[method_key]['span']
    columns = parameters[method_key]['column_names']
    column_data = data.get_info(columns)

    return data

def rate(data, parameters=None, call_num=None):
    method_key = get_method_key('rate', call_num)
    pass
    return data

def neighbours(data, parameters=None, call_num=None,):
    method_key = get_method_key('neighbours', call_num)
    pass
    return data

def classify(data, parameters=None, call_num=None):
    method_key = get_method_key('classify', call_num)
    pass
    return data
