import cv2
import numpy as np
from ParticleTrackingSimple.general.parameters import  get_param_val, get_method_key
from ParticleTrackingSimple.general.imageformat import bgr_2_grayscale
from Generic.images.basics import display

def distance(frame, parameters=None, call_num=None):
    '''
    Performs distance transform:

    distance implements the opencv distance transform. This
    transform operates on a binary image. For each chosen white pixel
    it calculates the distance to the nearest black pixel. This
    distance is the value of the chosen pixel. Thus if operating on
    a white circle the distance transform is a maximum at the middle and
    1 at the perimeter.

    :param frame: binary frame
    :param parameters: parameters dictionary

    :return: The distance transform image.
    '''
    dist = cv2.distanceTransform(frame, cv2.DIST_L2, 5)
    dist = 255*dist/np.max(dist)
    return dist

def grayscale(frame, parameters=None, call_num=None):
    '''
    Convert colour to grayscale:

    This function converts a bgr colour image into a monochrome
    or grayscale image.

    :param frame: A 3 channel colour image
    :param parameters: parameters dictionary

    :return: A grayscale image
    '''
    """Converts a BGR image to grayscale"""
    sz = np.shape(frame)
    if np.shape(sz)[0] == 3:
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif np.shape(sz)[0] == 2:
        print('Image is already grayscale')
        return frame
    else:
        print('Something went wrong! Shape img not recognised')
        return frame

def subtract_bkg(frame, parameters=None, call_num=None):
    '''
    Subtract bkg image

    This function subtracts a background image from a grayscale frame.

    options:
    parameters['subtract bkg type'] == 'mean' : subtracts the mean intensity from image
                                    == 'img' : subtracts a pre-prepared background image.
                                            (See preprocessing > meanbkg_img.py)
    parameters['subtract bkg norm'] == True   : Stretches range of final image intensities 0-255

    :param frame: grayscale image
    :param parameters: parameters dictionary

    :return: image with background image subtracted
    '''
    method_key = get_method_key('subtract_bkg', call_num=call_num)
    params = parameters['preprocess'][method_key]

    if params['subtract bkg type'] == 'mean':
        mean_val = int(np.mean(frame))
        subtract_frame = mean_val * np.ones(np.shape(frame), dtype=np.uint8)
    elif params['subtract bkg type'] == 'img':
        temp_params = {}

        # This option subtracts the previously created image which is added to dictionary.
        temp_params = {}
        temp_params['preprocess'] = {
            'blur': {'kernel': get_param_val(params['subtract_bkg_blur_kernel'])}}
        if parameters['experiment']['bkg_img'] is None:
            name = parameters['experiment']['video_filename']
            subtract_frame = cv2.imread(name[:-4] + '_bkgimg.png', -1)
        else:
            subtract_frame = cv2.imread(parameters['experiment']['bkg_img'])

        frame = blur(frame, temp_params)
        subtract_frame = blur(subtract_frame, temp_params)

    frame = cv2.subtract(subtract_frame, frame)

    if params['subtract bkg norm'] == True:
        frame = cv2.normalize(frame, None, alpha=0, beta=255,
                              norm_type=cv2.NORM_MINMAX)
    return frame

def variance(frame, parameters=None, call_num=None):
    '''
    variance image

    This function finds the mean value of image and then returns
    frame which is the absolute difference of each pixel from that value

    options:
    parameters['variance type'] == 'mean' : Returns the absolute difference from the mean
                                            img value
    parameters['variance type'] == 'img'  : Returns the absolute difference from a supplied
                                            bkg img. Bkg img is read into parameters['bkg_img'].
                                            bkg img must be in the same folder as the processed
                                            video with name = {video_name}_bkgimg.png
                                            A helpful script meanbkg_img.py can be used to average
                                            all the frames of a video together. If you have lots
                                            of small objects moving around and the video is long
                                            enough you can get a pretty good background estimate
                                            without having to take a bkg.

    parameters['variance bkg norm'] == True: will stretch the range of the largest difference to 255

    :param frame: grayscale image
    :param parameters: parameters dictionary

    :return: image of absolute difference from mean
    '''
    method_key = get_method_key('variance', call_num=call_num)
    params = parameters['preprocess'][method_key]


    if params['variance_type'] == 'mean':
        mean_val = int(np.mean(frame))
        subtract_frame = mean_val*np.ones(np.shape(frame), dtype=np.uint8)
    elif params['variance_type'] == 'img':
        temp_params = {}
        temp_params['preprocess'] = {'blur':{'kernel':get_param_val(params['variance_blur_kernel'])}}
        if parameters['experiment']['bkg_img'] is None:
            name = parameters['experiment']['video_filename']
            subtract_frame = cv2.imread(name[:-4] + '_bkgimg.png',-1)
        else:
            subtract_frame = cv2.imread(parameters['experiment']['bkg_img'])
        frame = blur(frame, temp_params)
        subtract_frame = blur(subtract_frame, temp_params)
    elif params['variance_type'] == 'zeros':
        subtract_frame = np.zeros(np.shape(frame))

    frame1 = cv2.subtract(subtract_frame, frame)
    frame1 = cv2.normalize(frame1, frame1 ,0,255,cv2.NORM_MINMAX)
    frame2 = cv2.subtract(frame, subtract_frame)
    frame2 = cv2.normalize(frame2, frame2,0,255,cv2.NORM_MINMAX)
    frame = cv2.add(frame1, frame2)

    if params['variance_bkg_norm'] == True:
        frame = cv2.normalize(frame, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

    return frame

def flip(frame, parameters=None, call_num=None):
    '''
    Inverts a binary frame

    :param frame: binary frame
    :param parameters: parameters dictionary

    :return: inverted binary frame
    '''
    return ~frame

def threshold(frame, parameters=None, call_num=None):
    '''
    Apply a global image threshold

    This takes a cutoff threshold value and returns white above and
    black below this value.

    option:
    parameters['threshold'] : sets the value of the cutoff threshold
    parameters['th_mode] : Can be used to invert the above behaviour

    :param frame: grayscale img
    :param parameters: parameters dictionary

    :return: binary image
    '''
    method_key = get_method_key('threshold', call_num=call_num)
    params = parameters['preprocess'][method_key]

    threshold = get_param_val(params['threshold'])
    mode = get_param_val(params['th_mode'])
    ret, out = cv2.threshold(frame,threshold,255,mode)
    return out

def adaptive_threshold(frame, parameters=None, call_num=None):
    '''
    Adaptive threshold

    This applies an adaptive threshold. This differs from global threshold
    in that for each pixel the cutoff threshold is defined based on a block of local
    pixels around it. This enables you to cope with gradual changes in illumination
    across the image etc.

    options:
    parameters['adaptive threshold']['block size'] : Size of local block of pixels to calculate threshold on
    parameters['adaptive threshold']['C'] : The mean-c value see here: http://homepages.inf.ed.ac.uk/rbf/HIPR2/adpthrsh.htm
    parameters['adaptive threshold']['ad_mode'] : inverts behaviour

    :param frame: grayscale image
    :param parameters: parameters dictionary

    :return: binary image
    '''
    method_key = get_method_key('adaptive_threshold', call_num=call_num)
    params = parameters['preprocess'][method_key]

    block = get_param_val(params['block_size'])
    const = get_param_val(params['C'])
    invert = get_param_val(params['ad_mode'])

    if invert == 1:
        out = cv2.adaptiveThreshold(frame,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, block, const)
    else:
        out = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block, const)
    return out

def blur(frame, parameters=None, call_num=None):
    '''
    Gaussian blur

    Applies a gaussian blur to the image (https://en.wikipedia.org/wiki/Gaussian_blur)
    Usually useful to apply before subtracting 2 images.

    options:
    parameters['blur kernel'] specifies the dimensions of a square kernel

    :param frame: grayscale image
    :param parameters: parameters dictionary

    :return: blurred image
    '''
    method_key = get_method_key('blur', call_num=call_num)
    params = parameters['preprocess'][method_key]
    kernel = get_param_val(params['kernel'])
    out = cv2.GaussianBlur(frame, (kernel, kernel), 0)

    return out

def medianblur(frame, parameters=None, call_num=None):
    '''
    Median blur

    Applies a median blur to the image (https://en.wikipedia.org/wiki/Median_filter)
    Good for removing speckle noise

    options:
    parameters['blur_kernel'] specifies the dimensions of a square kernel

    :param frame: grayscale image
    :param parameters: parameters dictionary

    :return: blurred image
    '''
    method_key = get_method_key('medianblur', call_num=call_num)
    params = parameters['preprocess'][method_key]

    kernel = get_param_val(params['kernel'])
    out = cv2.medianBlur(frame, (kernel,kernel))
    return out

def gamma(image, parameters=None, call_num=None):
    '''
    Gamma correction

    generates a lookup table which maps the values 0-255 to 0-255
    however not in a linear way. The mapping follows a power law
    with exponent gamma.

    :param image: grayscale image
    :param parameters: parameters dictionary

    :return: image
    '''
    method_key = get_method_key('gamma', call_num=call_num)
    params = parameters['preprocess'][method_key]

    gamma = get_param_val(params['gamma'])/100.0
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")

    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)

def resize(frame, parameters=None, call_num=None):
    '''
    Resize an image

    resizes an input image by the scale specified

    options:
    parameters['resize scale'] : factor for scale operation

    :param frame: colour, grayscale or binary image
    :param parameters: parameters dictionary

    :return: image
    '''
    method_key = get_method_key('resize', call_num=call_num)
    params = parameters['preprocess'][method_key]

    scale = get_param_val(params['scale'])/100
    return cv2.resize(frame, scale)

