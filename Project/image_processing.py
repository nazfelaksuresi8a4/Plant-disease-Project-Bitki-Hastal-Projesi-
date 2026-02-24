'''25.02.2026-00:47:27'''

import cv2 as cv
import numpy as np
from tensorflow.keras.applications.resnet import preprocess_input

class İmageProcesser:
    def __init__(self):
        self.status = True
        self.current_matrix = None
        self.flag_statement = True

    @staticmethod
    def to_matrix(img,mode):
        if mode == 'prediction':
            try:
                print(img)
                if isinstance(img, str):
                    preprocessed_img = np.expand_dims(cv.resize(cv.cvtColor(cv.imread(img), cv.COLOR_BGR2RGB), dsize=(224, 224)),axis=0)
                    preprocessed_img = preprocess_input(preprocessed_img)
                    return preprocessed_img
                else:
                    preprocessed_img = np.expand_dims(cv.resize(cv.cvtColor(img, cv.COLOR_BGR2RGB), dsize=(224, 224)),axis=0)
                    preprocessed_img = preprocess_input(preprocessed_img)
                    return preprocessed_img

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
    
    def realtimeImageCaptureSystem(self,callbackfunc):
        capture = cv.VideoCapture(0)

        while self.flag_statement:
            ret,frame = capture.read()
            frame = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
            callbackfunc(frame,None)
