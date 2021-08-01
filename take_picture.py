# from detect_mask_image import send_image
from pylepton import Lepton
import numpy as np
import cv2

class Cameras:
    def __init__(self):
        self.rgb_cam = cv2.VideoCapture(0)

    def __enter__(self):
        return self

    def take_thermal_photo(self):
        with Lepton() as thermal_cam:
            frame, _ = thermal_cam.capture()
        cv2.normalize(frame, frame, 0, 65535, cv2.NORM_MINMAX)
        np.right_shift(frame, 8, frame)
        return frame

    def take_rgb_photo(self):
        _, frame = self.rgb_cam.read()
        return frame

    def __exit__(self, *err):
        self.rgb_cam.release()
