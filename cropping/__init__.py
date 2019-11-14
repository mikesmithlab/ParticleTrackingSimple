from Generic import images
from ParticleTrackingSimple.cropping.crop_methods import crop_box
from Generic.images.basics import display

from Generic.video import ReadVideo


class ReadCropVideo(ReadVideo):

    def __init__(self, parameters=None,filename=None):
        ReadVideo.__init__(self, filename=filename)
        self.crop_method = parameters['crop_method']
        self.crop_coords = parameters['crop_coords']
        #self.read_next_frame()

    def read_next_frame(self):
        print('read')
        '''reads the next available frame'''
        if self.filetype == 'video':
            ret, frame = self.read_vid.read()
        elif self.filetype == 'img_seq':
            ret = True
            frame = self.read_vid[self.frame_num]
        else:
            ret = False
        self.frame_num = self.frame_num + 1

        if ret:
            if self.grayscale:
                frame = images.bgr_2_grayscale(frame)
        else:
            print('Error reading the frame. Check path and filename carefully')

        if self.crop_method is None:
            return frame
        elif self.crop_method == 'crop_box':
            cropped_frame, mask_img, coords=crop_box(frame, crop_coords=self.crop_coords)
            if self.crop_coords is None:
                self.crop_coords = coords
            return cropped_frame, mask_img, coords
        else:
            pass





