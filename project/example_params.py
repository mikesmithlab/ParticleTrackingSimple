'''
Using the parameters dictionary

There are 7 sections to the parameters dictionary. methods in each section are used if listed
in the order specified in the _______method: (methodA, methodB,). This tuple should end with a , after last method
and before closing bracket. Many method parameters can be adjusted in the gui using a slider. The sliders can be
turned on and off by changing the parameter into a 4 number list.
eg. 'adaptive_threshold':{'block_size': 111, will set the block_size to a fixed value and no slider will appear.
    'adaptive_threshold':{'block_size': [111,1,300,2], will produce a slider with start value 111, min val 1,
     max val 300 and increment 2. Most variables use a 1 increment but kernel based values require odd numbers.
     Therefore these should have an odd min val and 2 increment.

1.experiment
    Contains info about the experiment. Can be used to store sample info
    with the data file. There are no compulsory labels. The only potential
    info that is used is the filename of the bkg_img if used. None is automatically
    replaced if used with the default value of video_filename[:-4] = '_bkg_img'
2.crop
    'crop_method': can be None or 'box'. 'box results in a rectangular subsection of image
                   being cut from each subsequently called image
    'crop_coords': if tuple of coords is specified in format (x0,y0,w,h) these will be used
                   if 'box' in 'crop_method' and None here a gui window allows selection from first frame
    'mask':        currently inactive
3. preprocess
    'preprocess_method': Applies image preprocessing methods which are defined in preprocessing_methods.py
4. track
    'track_method': You can only run a single track_method. These are defined in tracking_methods.py
5. link
    'link_method': links particle positions into trajectories. This is necessary for some methods in postprocess
                    and annotate to work.
6. postprocess
    'postprocess_method': Applies postprocessing methods which are defined in postprocessing_methods.py these do things
    like calculate derivative quantities such as velocities, neighbours and classification of particles
7. annotate
    'annotate_method': Applies annotation methods such as colour coding, trajectories etc to videos.

'''


experiment = {'bkg_img':None,#None gives default of video_filename[:-4] + '_bkgimg.png'
              'sample':'500nm colloids in buffer',
              'fps':30
              }

crop = {'crop_method': None,
        'crop_coords': None,# (254, 92, 864, 529),
        'mask': None
        }

preprocess = {
    'preprocess_method': ('grayscale','adaptive_threshold','distance','threshold',),
    'load_bkg_img':True,
    'grayscale':{},
    'threshold':{'threshold':150,#[1,0,255,1],
                 'th_mode':0},#[1,0,1,1]},
    'adaptive_threshold':{'block_size': 111,#[15,1,300,2],
                          'C': 14,#[-29, -30, 30, 1],
                          'ad_mode': 1,#[0, 0, 1, 1]
                          },
    'distance':{},
    'blur':{'kernel':[1,1,15,2]},
    'medianblur':{'kernel':[1,1,15,2]},
    'gamma':{'gamma':[1,0,100,1]},
    'resize':{'scale':[1,0,500,1]},
    'subtract_bkg':{},
    'variance':{'variance_type':'img',
                'variance_blur_kernel': 3,
                'variance_bkg_norm':True
                },
    'flip':{},



    }

track = {
    'track_method':('trackpy',),
    'trackpy':{'size_estimate':21,#[7,1, 1001,2],
                'invert':[0,0,1,1]
               },
    'hough':{'min_dist':[10,1,201,2],
              'p1':[10, 1, 201,2],
              'p2':[10, 1, 201,2],
              'min_rad':[10, 1, 201,2],
              'max_rad':[10, 1, 201,2]
             },
    'contours':{'noise_cutoff':[2,1,50,1],
                'area':[20, 1, 200, 1],
                'aspect':[1,1,20,1]},
    'distance':{}
    }

link = {
    'link_method':'default',
    'default':{'search_range': 100,
                'pos_columns':None,
                'max_frame_displacement': 100,
                'memory': 3,
                'min_frame_life': 5
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
    'neighbours':{'method':'delaunay',
                  'neighbours':6,
                  'cutoff':[50,1,200,1],
                },
    'classify':{'column_name':'y',
                'output_name':'classify',
                'bin_norm':True,
                'bin_edges':[0,0.1,0.5,1]}
    }

annotate = {
    'annotate_method': ('trajectories',),#, 'trajectories'
    'videowriter':'opencv',
    'text_label':{'text':'Just Particles',
                 'position':(100,100),
                 'font_colour':(255,0,0),
                 'font_size':3,
                 'font_thickness':2
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
    'circles':{'radius':6,
               'cmap_type':'static',#'continuous',
               'cmap_column':'x',#For continuous
               'cmap_max':[470,1,2000,1],#For continuous
               'cmap_scale':1,
               'colour': (0,0,255),#For static
               'classifier_column':None,#For discrete or continuous
               'classifier': None,#For discrete or continuous
               'thickness':2
               },
    'boxes':{'radius':10,
               'cmap_type':'continuous',
               'cmap_column':'x',#None
               'cmap_max':[1,1,2000,1],
               'thickness':2
               },
    'contours':{'radius':10,
               'cmap_type':'continuous',
               'cmap_column':'x',#Nonedf['neighbours'].loc(particle)
               'cmap_max':[1,1,2000,1],
               'thickness':2
               },
    'networks':{'colour':(0,255,0),
               'thickness':2
               },
    'vectors':{'dx_column':'x',
               'dy_column':'y',
               'thickness':2,
               'line_type':8,
               'tip_length':[1,1,100,1],
               'vector_scale':[1,1,2000,1],
               'cmap_type':'static',#'continuous',
               'cmap_column':'x',#For continuous
               'cmap_max':[470,1,2000,1],#For continuous
               'cmap_scale':1,
               'colour': (0,0,255),#For static
               'classifier_column':None,#For discrete or continuous
               'classifier': None,#For discrete or continuous
               'thickness':2
                },
    'trajectories':{'x_column':'x',
                    'y_column':'y',
                    'traj_length': [200,0,100,1],
                    'cmap_type':'static',#'continuous',
               'cmap_column':'x',#For continuous
               'cmap_max':[470,1,2000,1],#For continuous
               'cmap_scale':1,
               'colour': (0,255,0),#For static
               'classifier_column':None,#For discrete or continuous
               'classifier': None,#For discrete or continuous
               'thickness':1
               }


    }

PARAMETERS = {
    'experiment': experiment,
    'crop': crop,
    'preprocess':preprocess,
    'track':track,
    'link':link,
    'postprocess':postprocess,
    'annotate':annotate
    }

