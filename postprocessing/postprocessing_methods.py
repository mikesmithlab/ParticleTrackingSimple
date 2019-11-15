import pandas as pd
import numpy as np
from ParticleTrackingSimple.general import dataframes
import trackpy as tp



def difference(data, parameters=None):
    columns = parameters['difference']['column_names']
    column_data = data.get_info(columns)

    span = parameters['difference']['span']




    return data