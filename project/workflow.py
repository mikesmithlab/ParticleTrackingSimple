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

    def __init__(self, video_filename=None, params=None):
        #Select operations to be performed'output_name':'x_smooth',

        PTWorkflow.__init__(self, video_filename=video_filename)
        #self.crop_select = True
        #self.preprocess_select = True
        #self.track_select = True
        #self.link_select = True
        self.postprocess_select = True
        self.annotate_select = True

        self.parameters = params.copy()

        self._setup()



if '__main__' == __name__:
    from ParticleTrackingSimple.general.gui import Gui
    from ParticleTrackingSimple.project.bacteria import PARAMETERS
    from Generic.filedialogs import BatchProcess

    for filename in BatchProcess(pathfilter='/media/ppzmis/data/ActiveMatter/Microscopy/191218_MP_particles_bacteria/streams/BacteriaParticles009.mp4'):
        print(filename)
        track = PTProject(video_filename=filename, params=PARAMETERS)
        #track.process()
        Gui(track)

