import qimage2ndarray as qim
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QApplication,
                             QSlider, QHBoxLayout, QCheckBox)
from ParticleTrackingSimple.general.pyqt5_widgets import QtImageViewer, QWidgetMod
from ParticleTrackingSimple.general.imageformat import stack_3, hstack
import numpy as np
import sys


class Gui:

    def __init__(self, tracker):
        self.tracker=tracker
        self.num_frames = self.tracker.cap.num_frames
        self.im=self.tracker.cap.find_frame(0)
        self.im0 = self.im.copy()
        self._display_img(self.im0, self.im0)
        self.read_slideable_parameters()
        self.init_ui()

    def _display_img(self, *ims):
        self.im = hstack(*ims)

    def init_ui(self):
        # Create window and layout
        app = QApplication(sys.argv)
        self.win = QWidgetMod(self.param_dict)
        self.vbox = QVBoxLayout(self.win)

        # Create Image viewer
        self.viewer = QtImageViewer()
        self.viewer.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.viewer.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.viewer.leftMouseButtonPressed.connect(self.get_coords)
        self.viewer.canZoom = True
        self.viewer.canPan = True
        self._update_im()
        self.vbox.addWidget(self.viewer)

        # Create live update checkbox
        cb = QCheckBox('Update')
        cb.toggle()
        cb.stateChanged.connect(self._update_cb)
        self.live_update = True
        self.vbox.addWidget(cb)

        # Add sliders
        self.add_sliders()

        # Finalise window
        self.win.setWindowTitle('ParamGui')
        self.win.setLayout(self.vbox)
        self.win.show()
        sys.exit(app.exec_())

    def add_sliders(self):

        self.sliders = {}
        self.labels = {}

        widget = QWidget()
        hbox = QHBoxLayout()
        self.frame_no=0
        self.frame_lbl = QLabel()
        self.frame_lbl.setText('frame: ' + str(self.frame_no))

        self.frame_slider = QSlider(Qt.Horizontal)
        self.frame_slider.setRange(0, self.num_frames)
        self.frame_slider.setValue(0)
        self.frame_slider.valueChanged.connect(self._update_sliders)
        hbox.addWidget(self.frame_lbl)
        hbox.addWidget(self.frame_slider)
        widget.setLayout(hbox)
        self.vbox.addWidget(widget)


        for key in sorted(self.param_dict.keys()):
            widget = QWidget()
            hbox = QHBoxLayout()

            params = self.param_dict[key]
            val, bottom, top, step = params

            lbl = QLabel()
            lbl.setText(key + ': ' + str(val))

            slider = QSlider(Qt.Horizontal)
            if step == 2:
                length = (top - bottom) / 2
                slider.setRange(0, length)
                slider.setValue((val-bottom)/2)
            else:
                slider.setRange(bottom, top)
                slider.setValue(val)
            slider.valueChanged.connect(self._update_sliders)

            hbox.addWidget(lbl)
            hbox.addWidget(slider)
            self.sliders[key] = slider
            self.labels[key] = lbl
            widget.setLayout(hbox)
            self.vbox.addWidget(widget)

    def read_slideable_parameters(self):
        parameters = self.tracker.parameters
        self.param_dict = {}

        for key in parameters:
            if key is not 'experiment':
                paramsubset = parameters[key]
                paramsubset[key + '_method']
                for subkey in paramsubset[key + '_method']:
                    if type(paramsubset[subkey]) == dict:
                        paramsubsubset = paramsubset[subkey]
                        for subsubkey in paramsubsubset:
                            value = paramsubsubset[subsubkey]
                            if type(value) == list:
                                self.param_dict[subsubkey] = value
        self.update_slideable_parameters()
        return self.param_dict

    def update_slideable_parameters(self):
        parameters = self.tracker.parameters
        for key in parameters:
            if key is not 'experiment':
                paramsubset = parameters[key]
                for subkey in paramsubset[key + '_method']:
                    if type(paramsubset[subkey]) == dict:
                        paramsubsubset = paramsubset[subkey]
                        for subsubkey in paramsubsubset:
                            if subsubkey in self.param_dict.keys():
                                paramsubsubset[subsubkey] = self.param_dict[subsubkey]

    def update(self):
        self.update_slideable_parameters()
        new_frame, annotated_frame = self.tracker.process_frame(self.frame_no)

        if np.size(np.shape(new_frame)) == 2:
            new_frame = stack_3(new_frame)
        if np.size(np.shape(annotated_frame)) == 2:
            annotated_frame = stack_3(annotated_frame)
        self._display_img(new_frame, annotated_frame)
        self._update_im()


    def _update_cb(self, state):
        if state == Qt.Checked:
            self.live_update = True
            self._update_sliders()
        else:
            self.live_update = False

    def _update_sliders(self):
        self.frame_no = self.frame_slider.value()
        self.frame_lbl.setText('frame: ' + str(self.frame_no))
        self.im0 = self.tracker.cap.find_frame(self.frame_no)
        for key in self.param_dict:
            params = self.param_dict[key]
            val, bottom, top, step = params

            val = self.sliders[key].value()
            if params[3] == 2:
                val = 2*val + bottom
            self.labels[key].setText(key + ': ' + str(val))
            self.param_dict[key][0] = val
        if self.live_update == True:
            self.update()
            self._update_im()

    def get_coords(self, x, y):
        print('cursor position (x, y) = ({}, {})'.format(int(x), int(y)))

    def _update_im(self):
        pixmap = QPixmap.fromImage(qim.array2qimage(self.im))
        self.viewer.setImage(pixmap)



