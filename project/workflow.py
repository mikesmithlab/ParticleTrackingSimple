from ParticleTrackingSimple.project.bacteria import PARAMETERS
from ParticleTrackingSimple.project import PTWorkflow

class PTProject(PTWorkflow):
    '''
    PTProject is a daughter class which is used as the interface to a particle tracking project.

    Setup:
    Select which bits of the process you are interested in by setting the Boolean
    Operators. You attach a dictionary PARAMETERS which controls all of the settings.
    It is up to you to make sure you have the correct parameters.

    Create an "instance" of the class:
    track=PTProject(video_filename="Full Path To File")

    There are 2 modes of operation:
    1) Pass the instance as an argument to TrackGui to optimise/trial things
    track = PTProject(video_filename='/home/mike/Documents/HydrogelTest.m4v')
    TrackingGui(track)
    2) call "instance".process() to process an entire movie.
    track = PTProject(video_filename='/home/mike/Documents/HydrogelTest.m4v')
    track.process()

    You can select the various parts of the operation by setting the flags to self.process_select
    self.preprocess_select = True
    self.track_select = True
    self.postprocess_select = False
    self.annotate_select = True

    What these processes will do is governed by the respective parts of the PARAMETERS dictionary above
    '''

    def __init__(self, video_filename=None):
        #Select operations to be performed'output_name':'x_smooth',

        PTWorkflow.__init__(self, video_filename=video_filename)
        self.crop_select = True
        self.preprocess_select = False
        self.track_select = False
        self.link_select = False
        self.postprocess_select = False
        self.annotate_select = True

        self.parameters = PARAMETERS

        self._setup()



if '__main__' == __name__:
    from ParticleTrackingSimple.general.gui import Gui
    filename='/media/ppzmis/data/dots.mp4'
    #filename = '/media/ppzmis/data/ActiveMatter/Microscopy/191126_500nm_particles/test.mp4'
    track = PTProject(video_filename=filename)
    #track.process()
    Gui(track)