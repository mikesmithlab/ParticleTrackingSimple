from ParticleTrackingSimple.general.parameters import get_method_name
from ParticleTrackingSimple.general.dataframes import DataStore
from ParticleTrackingSimple.postprocessing import postprocessing_methods as pm


class PostProcessor:
    def __init__(self, parameters=None, vidobject=None, data_filename=None):
        self.parameters = parameters
        self.cap = vidobject
        self.data_filename = data_filename
        self.data = DataStore(self.data_filename, load=True)

    def process(self, f_index=None):
        self.data.df['frame'] = self.data.df.index

        for method in self.parameters['postprocess_method']:
            method_name, call_num = get_method_name(method)
            self.data.df = getattr(pm, method_name)(self.data.df, f_index=f_index,parameters=self.parameters, call_num=call_num)

        self.data.save()

