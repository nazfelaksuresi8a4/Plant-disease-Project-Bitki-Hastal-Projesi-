import cv2 as cv
import skimage
import numpy as np

class İmageProcesser:
    def __init__(self):
        self.status = True

    @staticmethod
    def to_matrix(rootpath):
        try:
            return  cv.resize(cv.cvtColor(cv.imread(rootpath),cv.COLOR_BGR2RGB),dsize=(224,224))

        except Exception as e0:
            print(e0)

