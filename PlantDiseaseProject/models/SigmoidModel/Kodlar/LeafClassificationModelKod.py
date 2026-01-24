import tensorflow as tf
from tensorflow.keras.models import  Sequential
from tensorflow.keras.layers import  Dense,Dropout,Conv2D,MaxPooling2D,GlobalAveragePooling2D,BatchNormalization
from tensorflow.keras.preprocessing.image import  ImageDataGenerator
from tensorflow.keras.callbacks import  EarlyStopping,ReduceLROnPlateau
import cv2 as cv

dataset_path = r"C:\Users\alper\Desktop\Plant Disease Project\datasets\DiseaseClassificationDataset"
train_path = dataset_path + '\Train'
test_path = dataset_path + '\Test'

train_datagen = ImageDataGenerator(rescale=1./255,
                                   horizontal_flip=True,
                                   zoom_range=0.3,
                                   rotation_range=15)

test_datagen =  ImageDataGenerator(rescale=1./255)

train_data = train_datagen.flow_from_directory(directory=train_path,
                                               target_size=(224,224),
                                               batch_size=16,
                                               class_mode='binary')

test_data = test_datagen.flow_from_directory(directory=test_path,
                                             target_size=(224,224),
                                             batch_size=16,
                                             class_mode='binary',
                                             shuffle=False)

model = Sequential(layers=[Conv2D(32,(3,3),strides=(1,1),activation='relu',input_shape=(224,224,3)),
                           BatchNormalization(),
                           MaxPooling2D(2,2),

                           Conv2D(64,(3,3),strides=(1,1),activation='relu'),
                           BatchNormalization(),
                           MaxPooling2D(2,2),

                           Conv2D(128, (3, 3), strides=(1, 1), activation='relu'),
                           BatchNormalization(),
                           MaxPooling2D(2, 2),

                           Conv2D(256, (3, 3), strides=(1, 1), activation='relu'),
                           BatchNormalization(),
                           MaxPooling2D(2, 2),
                           Dropout(0.3),

                           GlobalAveragePooling2D(data_format='channels_last',
                                                  keepdims=False),
                           Dense(16,activation='relu'),
                           Dense(1, activation='sigmoid')
                           ])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

history = model.fit(x=train_data,epochs=7,validation_data=test_data,callbacks=[EarlyStopping(monitor='val_loss',
                                                                                              patience=7,
                                                                                              restore_best_weights=True),
                                                                                ReduceLROnPlateau(monitor='val_loss',
                                                                                                  factor=0.3,
                                                                                                  patience=0.2,
                                                                                                  )])

with open(r"C:\Users\alper\Desktop\Plant Disease Project\datasets\DiseaseClassificationDataset\datas.txt",mode='w') as logfile:
    for key in history.history:
        logfile.write(f'{key}: {history.history[key]}\n\n')

print(history.history)
model.save('leafClassificationModel.h5')
