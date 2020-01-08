from Generic.filedialogs import BatchProcess
from Generic.video import ReadVideo
import numpy as np
import cv2
import matplotlib.pyplot as plt

def intensity_img(filename):
    readvid = ReadVideo(filename=file)
    frame_init = readvid.read_next_frame()  # .astype(np.int32)


    intensity=[]
    for i in range(int(readvid.num_frames/10) - 1):
        frame = readvid.find_frame(i*10).astype(np.int32)
        intensity.append(np.mean(frame))
    intensity=np.array(intensity)

    print(np.mean(intensity))

    readvid.close()


if __name__ == '__main__':
    for file in BatchProcess(pathfilter='/media/ppzmis/data/ActiveMatter/Microscopy/191126_500nm_particles/StreamDIC002.avi'):
        intensity_img(file)