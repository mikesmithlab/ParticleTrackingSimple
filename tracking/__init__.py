import os
from tqdm import tqdm
from ParticleTrackingSimple.general import dataframes
from ParticleTrackingSimple.tracking import tracking_methods as tm
from ParticleTrackingSimple.general.parameters import get_method_name
import numpy as np

class ParticleTracker:
    """
    Class to track the locations of the particles in a video_crop.

    1) Uses preprocessing.Preprocessor to manipulate images.
    2) Uses method to locate the particles
    3) Confirms that each detected particle is real
    4) Saves particle positions and boundary information in a dataframe
    5) Saves a cropped copy of the video_crop

    Attributes
    ----------
    input_filename : str
        Contains path of the input video_crop
    filename: str
        Contains path of the input video_crop without extension
    data_filename: str
        Contains path to save the dataframe to
    parameters: dict
        Contains arguments for preprocessing, detection, tracking
    multiprocess: bool
        If true using multiprocessing to speed up tracking
    save_crop_video: bool
        If true saves the cropped copy of the video_crop
    save_check_video: bool
        If true saves the annoatated copy of the video_crop
    ip: class instance of preprocessing.Preprocessor

    """

    def __init__(self, parameters=None, preprocessor=None, vidobject=None, data_filename=None, multiprocess=False):
        """

        Parameters
        ----------
        filename: str
            Filepath of input video_crop/stack

        methods: list of str
            Contains methods for Preprocessor

        parameters: dictionary
            Contains parameters for any functions

        crop_method: String or None
            Decides video_crop method.
            None: no crop
            'auto': Automatically crop around blue hexagon
            'manual': Manually select video_crop points
        """
        self.filename = os.path.splitext(vidobject.filename)[0]
        self.parameters = parameters
        self.ip = preprocessor
        self.cap = vidobject
        self.data_filename = self.filename + '.hdf5'

    def track(self, f_index=None):
        """
        Method called by track.

        Parameters
        ----------
        group_number: int
            Sets the group number for multiprocessing to split the input.
        """
        data_name = self.data_filename
        with dataframes.DataStore(data_name) as data:
            data.add_metadata('number_of_frames', self.cap.num_frames)
            data.add_metadata('fps', self.cap.fps)
            data.add_metadata('video_filename', self.cap.filename)
            if f_index is None:
                start = 0
                stop = self.cap.num_frames
            else:
                start = f_index
                stop = f_index + 1

            self.cap.set_frame(start)

            for f in tqdm(range(start, stop, 1), 'Tracking'):
                df_frame = self.analyse_frame()
                data.add_tracking_data(f, df_frame)
            data.save()

    def analyse_frame(self):
        frame = self.cap.read_next_frame()
        method = self.parameters['track_method'][0]
        if self.ip is None:
            preprocessed_frame = frame
        else:
            preprocessed_frame = self.ip.process(frame)

        df_frame = getattr(tm, method)(preprocessed_frame, self.parameters)
        return df_frame

    def update_parameters(self, parameters):
        self.parameters = parameters
        self.ip.update_parameters(self.parameters)
