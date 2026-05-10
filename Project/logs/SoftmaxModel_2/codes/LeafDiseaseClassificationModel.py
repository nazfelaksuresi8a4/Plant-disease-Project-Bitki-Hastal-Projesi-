import tensorflow as tf
from keras.src.layers import GlobalAveragePooling2D, BatchNormalization
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
from tensorflow.keras import layers, models

# =====================
# PATHS
# =====================
dataset_path = r"C:\Users\alper\Desktop\Plant Disease Project\datasets\LeafDiseaseClassificationDataset"
train_path = dataset_path + r"\Train"
validation_path = dataset_path + r"\Test"

IMG_SIZE = (224, 224)
BATCH_SIZE = 16
NUM_CLASSES = 4

train_data_generator = ImageDataGenerator(preprocessing_function=preprocess_input,
                                          horizontal_flip=True,
                                          zoom_range=0.5,
                                          rotation_range=2)

validation_data_generator = ImageDataGenerator(preprocessing_function=preprocess_input)

train_flow = train_data_generator.flow_from_directory(directory=train_path,
                                                      target_size=IMG_SIZE,
                                                      batch_size=BATCH_SIZE,
                                                      class_mode='categorical'
                                                      )

validation_flow = validation_data_generator.flow_from_directory(directory=validation_path,
                                                                target_size=IMG_SIZE,
                                                                batch_size=BATCH_SIZE,
                                                                class_mode='categorical',
                                                                shuffle=False)

base_model = ResNet50(include_top=False,
                      input_shape=(224,224,3),
                      weights='imagenet')


base_model.trainable = False

inputs = tf.keras.Input(shape=(224,224,3))
x = base_model(inputs,training=False)
x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = tf.keras.layers.BatchNormalization()(x)
x = tf.keras.layers.Dense(256,activation='relu')(x)
x = tf.keras.layers.Dropout(0.5)(x)
outputs = tf.keras.layers.Dense(NUM_CLASSES,activation='softmax')(x)

model = models.Model(inputs,outputs)

reduceLro = ReduceLROnPlateau(monitor='val_loss',
                              patience=1,
                              factor=0.9,
                              verbose=1)

earlyStop = EarlyStopping(monitor='val_loss',
                          patience=6,
                          restore_best_weights=True,
                          verbose=1)


model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

fit_history2 = model.fit(
    train_flow,
    validation_data = validation_flow,
    callbacks=[reduceLro,earlyStop],
    epochs=6
)

model.summary()


for layer in base_model.layers[-36:]:
    layer.trainable = True

fit_history = model.fit(
    train_flow,
    validation_data = validation_flow,
    callbacks=[reduceLro,earlyStop],
    epochs=16
)

import logger

try:
    logger.Logger(logfile_path=r"C:\Users\alper\Desktop\datasetler\log.txt",
                evaulate_path=None,
                history=fit_history,
                model=model,
                test_data=None).writeLog()
except Exception as e:
    print(e)

finally:
    print(fit_history.history)

try:
    logger.Logger(logfile_path=r"C:\Users\alper\Desktop\datasetler\log.txt",
                evaulate_path=None,
                history=fit_history2,
                model=model,
                test_data=None).writeLog()
except Exception as e:
    print(e)

finally:
    print(fit_history.history)

model.save('LeafDiseaseClassificationModelmainX.h5')
