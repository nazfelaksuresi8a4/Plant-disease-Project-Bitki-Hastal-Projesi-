from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet import preprocess_input
import numpy as np 
import cv2 as cv
import matplotlib.pyplot as plt

model_path = r"C:\Users\alper\Desktop\Plant Disease Project\models\SoftmaxModel\model\LeafDiseaseClassificationModel.h5"
image_path = r"C:\Users\alper\Desktop\gorsel_ayirt_etme_sistemi\tomato-early-blight1x2400.jpg"

model = load_model(model_path)

matlike = cv.imread(image_path)

transformed_colorspace = cv.cvtColor(matlike,cv.COLOR_BGR2RGB)
resized_matlike = cv.resize(transformed_colorspace,dsize=(224,224))
batch_dim = np.expand_dims(resized_matlike,axis=0)
x = preprocess_input(batch_dim)

dct = {0: 'pepper_ball_bacterial_spot', 
1: 'potato_early_blight', 
2: 'potato_late_blight', 
3: 'tomato_bacterial_spot', 
4: 'tomato_early_blight', 
5: 'tomato_late_blight', 
6: 'tomato_leaf_mod', 
7: 'tomato_mosaic_virus', 
8: 'tomato_septoria_leaf_spot', 
9: 'tomato_spider_mites', 
10: 'tomato_target_spot'}


pred = np.argmax(model.predict(x,batch_size=16)[0])

print(dct[pred])

