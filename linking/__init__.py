from ParticleTrackingSimple.general import dataframes
import trackpy

class LinkTrajectory:
    def __init__(self, data_filename=None, parameters=None):
        self.data_filename=data_filename
        self.parameters=parameters

    def link_trajectories(self):
        """Implements the trackpy functions link_df and filter_stubs"""
        # Reload DataStore
        with dataframes.DataStore(self.data_filename) as data:
            # Trackpy methods
            data.reset_index()
            data.df = trackpy.link_df(data.df,self.parameters['default']['max_frame_displacement'],memory=self.parameters['default']['memory'])

            data.df = trackpy.filter_stubs(data.df, self.parameters['default']['min_frame_life'])
            data.set_frame_index()

            # Save DataStore
            data.save(filename=self.data_filename)