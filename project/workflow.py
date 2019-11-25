from ParticleTrackingSimple.project import PTWorkflow

crop = {'crop_method': 'crop_box',
        'crop_coords': (254, 92, 864, 529),
        'mask': None
        }

preprocess = {
    'preprocessor_method': ('grayscale','adaptive_threshold'),
    'grayscale':{},
    'threshold':{'threshold':[1,0,255,1],
                 'mode':[0,0,1,1]},
    'adaptive_threshold':{'block_size': 81,
                          'C': [12, -30, 30, 1],
                          'mode': [1, 0, 1, 1]
                          },
    'blur':{'kernel':[1,1,15,2]},
    'medianblur':{'kernel':[1,1,15,2]},
    'gamma':{'gamma':[1,0,100,1]},
    'resize':{'scale':[1,0,500,1]},
    'subtract_bkg':{},
    'variance':{},
    'flip':{},



    }

track = {
    'track_method':'trackpy',
    'trackpy':{'size_estimate':[19,1, 101,2],
                'invert':[0,0,1,1]
               },
    'hough':{},
    'contours':{},
    'distance':{}
    }

link = {
    'link_method':'default',
    'default':{'search_range': 10,
                'pos_columns':None,
                'max_frame_displacement': 10,
                'memory': 3,
                'min_frame_life': 1
                #
                }
    }

postprocess = {
    'postprocess_method': ('neighbours',),
    'smooth':{'column_name':'y',
              'output_name':'y_smooth',
              'span':5,
              'method':'default'
              },
    'difference':{'column_name':'x',
                  'output_name':'x_diff',
                  'span':2
                  },
    'difference*2':{'column_name':'y',
                  'output_name':'y_diff',
                  'span':2
                  },
    'magnitude':{'column_names':('vx','vy'),
                 'output_name':'v'
    },
    'angle':{'column_names':('x','y'),
             'output_name':'theta',
             'units':'degrees'

    },
    'rate':{'column_name':'x',
            'output_name':'vx',
            'fps':50.0,
            'method':'finite_difference'
              },
    'rate*2':{'column_name':'y',
            'output_name':'vy',
            'fps':50.0,
            'method':'finite_difference'
              },
    'neighbours':{'method':'delaunay'
                },
    'classify':{'column_name':'y',
                'output_name':'classify',
                'bin_norm':True,
                'bin_edges':[0,0.1,0.5,1]}
    }

annotate = {
    'annotate_method': ('circles',),
    'videowriter':'opencv',
    'text_label':{'text':'Mike',
                 'position':(100,100),
                 'font_colour':(0,0,255),
                 'font_size':4,
                 'font_thickness':3
                 },
    'var_label':{'var_column':'index',
                 'position':(100,100),
                 'font_colour':(255,0,255),
                 'font_size':4,
                 'font_thickness':3
                 },
    'particle_values': {'values_column': 'particle',
                        'font_colour': (255, 0, 255),
                        'font_size': 1,
                        'font_thickness': 1
                        },
    'circles':{'radius':10,
               'cmap_type':'continuous',
               'cmap_column':'x',#None
               'cmap_max':[300,1,2000,1],
               'thickness':1
               },
    'boxes':{'radius':10,
               'cmap_type':'continuous',
               'cmap_column':'x',#None
               'cmap_max':[1,1,2000,1],
               'thickness':2
               },
    'contours':{'radius':10,
               'cmap_type':'continuous',
               'cmap_column':'x',#None
               'cmap_max':[1,1,2000,1],
               'thickness':2
               },
    'networks':{'radius':10,
               'cmap_type':'continuous',
               'cmap_column':'x',#None
               'cmap_max':[1,1,2000,1],
               'thickness':2
               },

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

    'trajectories':{'x_column':'x',
                    'y_column':'y',
                    'traj_length': [10,0,100,1],
                    'classifier_column':None,
                    'classifier': 1,
                    'cmap_type':'discrete',
                    'cmap_column':'x',#None
                    'cmap_max':[200,1,2000,1],
                    'thickness':2
               }


    }

PARAMETERS = {
    'crop': crop,
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
        #Select operations to be performed'output_name':'x_smooth',

        PTWorkflow.__init__(self, video_filename=video_filename)
        self.crop_select = False
        self.preprocess_select = False
        self.track_select = False
        self.postprocess_select = True
        self.annotate_select = False

        self.parameters = PARAMETERS

        self._setup()



if '__main__' == __name__:

    from ParticleTrackingSimple.tracking.tracking_gui import TrackingGui

    track = PTProject(video_filename='/home/mike/Videos/HydrogelTest.m4v')
    #track.process()
    TrackingGui(track)