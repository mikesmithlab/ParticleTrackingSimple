from ParticleTrackingSimple.project import PTWorkflow

preprocess = {
    'crop_method':'no_crop',
    'preprocessor_method': ('grayscale','adaptive_threshold'),
    'adaptive_threshold':{'block_size': 81,#[81, 3, 101, 2],
                           'C': [12, -30, 30, 1],
                            'mode': [1, 0, 1, 1]
                          }
    }

track = {
    'track method':'trackpy',
    'trackpy':{'size_estimate':[19,1, 101,2],
                'invert':[0,0,1,1]
               }
    }

link = {
    'link_method':'',
    'max_frame_displacement': 50,
    'min_frame_life': 1,
    'memory': 3,
    'trajectory_smoothing': 3,
    }

postprocess = {
    'postprocess_method': None
    }

annotate = {
    'annotate_method': ('text_label', 'var_label'),
    'vectors':{'dx_column':'x',
               'dy_column':'y',
               'thickness':2,
               'line_type':8,
               'tip_length':[1,1,100,1],
               'vector_scale':[1,1,2000,1],
               'cmap_type':'continuous',
               'cmap_column':'y',
               'cmap_max':[1,1,2000,1]
                },
    'circles':{'radius':10,
               'cmap_type':'continuous',
               'cmap_column':'x',#None
               'cmap_max':[1,1,2000,1],
               'thickness':2
               },
    'particle_values':{'values_column':'mass',
                        'font_colour':(255,0,255),
                        'font_size':1,
                        'font_thickness':1
                        },
    'var_label':{'var_column':'index',
                 'position':(100,100),
                 'font_colour':(255,0,255),
                 'font_size':4,
                 'font_thickness':3
                 },
    'text_label':{'text':'Mike',
                 'position':(100,100),
                 'font_colour':(0,0,255),
                 'font_size':4,
                 'thickness':3
                 }

    }

PARAMETERS = {
    #'crop':crop,
    'preprocess':preprocess,
    'track':track,
    'link':link,
    'postprocess':postprocess,
    'annotate':annotate
    }

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
        #Select operations to be performed

        PTWorkflow.__init__(self, video_filename=video_filename)

        self.preprocess_select = True
        self.track_select = True
        self.postprocess_select = False
        self.annotate_select = True

        self.parameters = PARAMETERS

        self._setup()



if '__main__' == __name__:

    from ParticleTrackingSimple.tracking.tracking_gui import TrackingGui

    track = PTProject(video_filename='/home/mike/Videos/HydrogelTest.m4v')
    #track.process()
    TrackingGui(track)