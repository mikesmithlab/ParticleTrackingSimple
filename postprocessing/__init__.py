from ParticleTrackingSimple.general import get_method_name
from ParticleTrackingSimple.general.dataframes import DataStore
from ParticleTrackingSimple.postprocessing import postprocessing_methods as pm

class PostProcessor:
    def __init__(self, parameters=None, data_filename=None):
        self.parameters = parameters
        self.data_filename = data_filename
        self.data = DataStore(self.data_filename, load=True)

    def process(self):
        for method in self.parameters['postprocessor method']:
            method_name, call_num = get_method_name(method)
            self.data = getattr(pm, method_name)(self.data, parameters=self.parameters, call_num=call_num)
        self.data.save()
