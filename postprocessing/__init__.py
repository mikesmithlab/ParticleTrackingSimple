from ParticleTrackingSimple.general.parameters import get_method_name
from ParticleTrackingSimple.general.dataframes import DataStore
from ParticleTrackingSimple.postprocessing import postprocessing_methods as pm


class PostProcessor:
    def __init__(self, parameters=None, vidobject=None, data_filename=None):
        self.parameters = parameters
        self.cap = vidobject
        self.data_filename = data_filename
        self.data = DataStore(self.data_filename, load=True)

    def prepare_df(self):
        self.data.df['frame'] = self.data.df.index
        if 'particle' not in self.data.df.columns:
            print('Creating dummy particle ids based on the index. '
                  'Without running the dataframe through linking many'
                  'postprocessor methods are meaningless. They may still'
                  '"work" but think about the results.')
            self.data.df['particle']=self.data.df.index

    def process(self, f_index=None):
        self.prepare_df()
        for method in self.parameters['postprocess_method']:
            method_name, call_num = get_method_name(method)
            self.data.df = getattr(pm, method_name)(self.data.df, f_index=f_index,parameters=self.parameters, call_num=call_num)

        self.data.save()

