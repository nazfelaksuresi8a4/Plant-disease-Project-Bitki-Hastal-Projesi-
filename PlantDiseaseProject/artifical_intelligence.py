import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import  Dense,Conv2D,MaxPooling2D
from tensorflow.keras.preprocessing.image import  ImageDataGenerator
from tensorflow.keras.preprocessing import  image
from sklearn.preprocessing import  LabelEncoder
from sklearn.model_selection import  train_test_split

class ArtificalIntelligence:
    def __init__(self,epochs,patience,factor,dataset_path,horizontal_flip,zoom_range,augomention,valitation_split,rotation_range,test_shuffle,target_size,batch_size,actived_callbacks):
        pass