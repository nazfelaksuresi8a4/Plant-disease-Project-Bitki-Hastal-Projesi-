import tensorflow as tf
from tensorflow.keras.models import  Sequential
from tensorflow.keras.layers import (Dense,Dropout,BatchNormalization,
                                     MaxPooling2D,GlobalAveragePooling2D,
                                     Conv2D)
from tensorflow.keras.callbacks import EarlyStopping,ReduceLROnPlateau
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import logger

'''Paths'''
historyX = []
logfile = r"logs\datas.txt"
elogfile = r"logs\evaulates.txt"
dataset_path = r"datasets\DiseaseClassificationDataset"
train_path = dataset_path + '\Train'
test_path = dataset_path + '\Test'

'''Model variables'''
epochs = 7*2

'''Generators'''
train_datagen = ImageDataGenerator(rescale=1./255,
                                   horizontal_flip=True,
                                   zoom_range=0.3,
                                   validation_split=0.3,
                                   rotation_range=15)

test_datagen = ImageDataGenerator(rescale=1./255)

'''Generator flows'''
train_data = train_datagen.flow_from_directory(directory=train_path,
                                               target_size=(224,224),
                                               batch_size=16,
                                               class_mode='binary',
                                               subset='training')

val_data = train_datagen.flow_from_directory(directory=train_path,
                                             target_size=(224,224),
                                             batch_size=16,
                                             class_mode='binary',
                                             subset='validation')

test_data = test_datagen.flow_from_directory(directory=test_path,
                                             target_size=(224,224),
                                             batch_size=16,
                                             class_mode='binary',
                                             shuffle=False)

callbacks = [EarlyStopping(monitor='val_loss',
                           patience=epochs // 2,
                           min_delta=0.0001,
                           restore_best_weights=True),
             ReduceLROnPlateau(monitor='val_loss',
                               patience=2,
                               factor=0.4,
                               )]

model = Sequential(layers=[
    Conv2D(filters=16,kernel_size=(3,3),strides=(1,1),activation='relu',input_shape=(224,224,3)),
    BatchNormalization(),
    MaxPooling2D(),

    Conv2D(filters=32, kernel_size=(3, 3), strides=(1, 1), activation='relu'),
    BatchNormalization(),
    MaxPooling2D(),

    Conv2D(filters=64, kernel_size=(3, 3), strides=(1, 1), activation='relu'),
    BatchNormalization(),
    MaxPooling2D(),

    Conv2D(filters=128, kernel_size=(3, 3), strides=(1, 1), activation='relu'),
    BatchNormalization(),
    MaxPooling2D(),

    Conv2D(filters=256, kernel_size=(3, 3), strides=(1, 1), activation='relu'),
    BatchNormalization(),
    MaxPooling2D(),
    Dropout(0.4),

    GlobalAveragePooling2D(),
    Dense(16,activation='relu'),
    Dense(1,activation='sigmoid')
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

pred_dct = {}
classes = train_data.class_indices

for key in classes:
    pred_dct[classes[key]] = key

history = model.fit(x=train_data,
                    epochs=epochs,
                    validation_data=val_data,
                    callbacks=callbacks)

module = logger.Logger(logfile,elogfile,history,model,test_data).writeLog()

model.save('XLeafClassificationModel.h5')

