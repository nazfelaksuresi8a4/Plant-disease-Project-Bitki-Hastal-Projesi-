import cv2 as cv
import skimage
import numpy as np


class İmageProcesser:
    def __init__(self):
        self.status = True

    @staticmethod
    def to_matrix(img):
        try:
            print(img)
            if isinstance(img, str):
                return cv.resize(cv.cvtColor(cv.imread(img), cv.COLOR_BGR2RGB), dsize=(224, 224))
            else:
                return cv.resize(cv.cvtColor(img, cv.COLOR_BGR2RGB), dsize=(224, 224))

        except Exception as e0:
            print(e0)

