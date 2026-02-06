from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet import preprocess_input
import numpy as np 
import cv2 as cv
import matplotlib.pyplot as plt

model_path = r'LeafClassificationModelMainxc.h5'
image_path = r"C:\Users\alper\Desktop\Plant Disease Project - Kopya (2)\datasets\istockphoto-1449566728-2048x2048.jpg"

model = load_model(model_path)

matlike = cv.imread(image_path)

transformed_colorspace = cv.cvtColor(matlike,cv.COLOR_BGR2RGB)
resized_matlike = cv.resize(transformed_colorspace,dsize=(224,224))
batch_dim = np.expand_dims(resized_matlike,axis=0)
x = preprocess_input(batch_dim)

pred = model.predict(x,batch_size=16)

print(pred[0][0])
