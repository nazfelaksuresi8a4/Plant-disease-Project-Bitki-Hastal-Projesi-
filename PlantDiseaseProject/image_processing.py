import cv2 as cv
import skimage
import numpy as np


class İmageProcesser:
    def __init__(self):
        self.status = True

    @staticmethod
    def to_matrix(img,mode):
        if mode == 'prediction':
            try:
                print(img)
                if isinstance(img, str):
                    return np.expand_dims(cv.resize(cv.cvtColor(cv.imread(img), cv.COLOR_BGR2RGB), dsize=(224, 224)),axis=0) / 255
                else:
                    return np.expand_dims(cv.resize(cv.cvtColor(img, cv.COLOR_BGR2RGB), dsize=(224, 224)),axis=0) / 255

            except Exception as e0:
                print(e0)
                return e0
        
        elif mode == 'matrix returner':
            try:
                print(img)
                if isinstance(img, str):
                    return cv.resize(cv.cvtColor(cv.imread(img), cv.COLOR_BGR2RGB), dsize=(224, 224))
                else:
                    return cv.resize(cv.cvtColor(img, cv.COLOR_BGR2RGB), dsize=(224, 224))

            except Exception as e0:
                print(e0)
                return e0
