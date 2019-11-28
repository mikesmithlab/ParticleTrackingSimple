experiment = {'bkg_img':None,#None gives default of video_filename[:-4] + '_bkgimg.png'
              'sample':'500nm colloids in buffer',
              'fps':30
              }

crop = {'crop_method': None,
        'crop_coords': None,# (254, 92, 864, 529),
        'mask': None
        }

preprocess = {
    'preprocess_method': ('variance','grayscale','adaptive_threshold',),
    'load_bkg_img':True,
    'grayscale':{},
    'threshold':{'threshold':[1,0,255,1],
                 'mode':[0,0,1,1]},
    'adaptive_threshold':{'block_size': [15,1,300,2],
                          'C': [-29, -30, 30, 1],
                          'mode': [0, 0, 1, 1]
                          },
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
    'trackpy':{'size_estimate':[7,1, 101,2],
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
    'default':{'search_range': 15,
                'pos_columns':None,
                'max_frame_displacement': 10,
                'memory': 3,
                'min_frame_life': 30
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
    'annotate_method': ('circles', 'trajectories','text_label',),
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
               'cmap_type':'continuous',
               'cmap_column':None,#'x'
               'cmap_max':[470,1,2000,1],
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
               'cmap_type':'continuous',
               'cmap_column':'y',
               'cmap_max':[1,1,2000,1]
                },
    'trajectories':{'x_column':'x',
                    'y_column':'y',
                    'traj_length': [200,0,100,1],
                    'classifier_column':None,
                    'classifier': 1,
                    'colour':(50,200,50),
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
