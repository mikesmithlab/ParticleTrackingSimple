from ParticleTrackingSimple.general import dataframes
import trackpy

class LinkTrajectory:
    def __init__(self, data_filename=None, parameters=None):
        self.data_filename=data_filename
        self.parameters=parameters

    def link_trajectories(self):
        """Implements the trackpy functions link_df and filter_stubs"""
        # Reload DataStore
        print('link')
        data=dataframes.DataStore(self.data_filename, load=True)
        print(data.df)

        with dataframes.DataStore(self.data_filename, load=True) as data:
            # Trackpy methods

            print(data)
            print(data.df.head(n=20))
            data.reset_index()
            data.df = trackpy.link_df(data.df,self.parameters['default']['max_frame_displacement'],memory=self.parameters['default']['memory'])

            data.df = trackpy.filter_stubs(data.df, self.parameters['default']['min_frame_life'])
            # Save DataStore
            #data.set_frame_index()
            data.save(filename=self.data_filename)