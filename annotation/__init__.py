from Generic.video import WriteVideo, WriteVideoFFMPEG
from ParticleTrackingSimple.annotation import annotation_methods as am
from ParticleTrackingSimple.general import dataframes
from ParticleTrackingSimple.general.parameters import get_method_name
from tqdm import tqdm


class TrackingAnnotator:

    def __init__(self, parameters=None, vidobject=None, data_filename=None, bitrate='HIGH1080', framerate=50):
        self.parameters = parameters
        self.cap = vidobject
        self.data_filename=data_filename
        self.output_filename = self.cap.filename[:-4] + '_annotate.mp4'
        frame_size = (self.cap.height, self.cap.width, 3)
        if parameters['videowriter'] == 'opencv':
            self.out = WriteVideo(filename=self.output_filename, frame_size=frame_size)
        elif parameters['videowriter'] == 'ffmpeg':
            self.out = WriteVideoFFMPEG(self.output_filename, bitrate=bitrate, framerate=framerate)

    def annotate(self, f_index=None):
        with dataframes.DataStore(self.data_filename, load=True) as data:
            if f_index is None:
                start=0
                stop=self.cap.num_frames
            else:
                start=f_index
                stop=f_index+1
            self.cap.set_frame(start)

            for f in tqdm(range(start, stop, 1), 'Annotating'):
                frame = self.cap.read_next_frame()

                for method in self.parameters['annotate_method']:
                    # Use function in preprocessing_methods
                    method_name, call_num = get_method_name(method)
                    frame = getattr(am, method_name)(frame, data, f, self.parameters, call_num=call_num)
                if f_index is None:
                    self.out.add_frame(frame)
            if f_index is None:
                self.out.close()
            else:
                return frame



