from ParticleTrackingSimple.preprocessing import preprocessing_methods as pm


class Preprocessor:
    """
    Processes images using a list of methods in
    preprocessor parameters dictionary.
    """

    def __init__(self, parameters):
        self.parameters = parameters

    '''
    def update_parameters(self, parameters):
        self.parameters = parameters
    '''

    def process(self, frame):
        '''
        Preprocesses single frame
        '''
        for method in self.parameters['preprocessor_method']:
            frame = getattr(pm, method)(frame, self.parameters)
        return frame

