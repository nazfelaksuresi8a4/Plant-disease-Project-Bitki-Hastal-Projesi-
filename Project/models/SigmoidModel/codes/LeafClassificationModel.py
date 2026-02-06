'''IMPORTS'''

import tensorflow as tf 
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.resnet import ResNet50,preprocess_input
from tensorflow.keras.layers import Dense,GlobalAveragePooling2D,BatchNormalization,Dropout
from tensorflow.keras.callbacks import ReduceLROnPlateau,EarlyStopping
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import loggerx 

'''SETTINGS'''
dataset_path = r'C:\Users\alper\Desktop\Plant Disease Project\datasets\LeafClassificationDataset'
train_path = dataset_path + '\Train'
validation_path = dataset_path + '\Test'

TARGET_SIZE = (224,224)
INPUT_SHAPE = (224,224,3)
BATCH_SIZE = 16
CLASS_MODE = 'binary'

'''GENERATORS'''
train_data_generator = ImageDataGenerator(preprocessing_function=preprocess_input,
                                          horizontal_flip = True,
                                          rotation_range = 13,
                                          zoom_range = 0.15,
                                          width_shift_range = 0.15,
                                          height_shift_range = 0.15,
                                          brightness_range = (0.3,0.8))

validation_data_generator = ImageDataGenerator(preprocessing_function=preprocess_input)


'''FLOWS'''
train_flow = train_data_generator.flow_from_directory(directory=train_path,
                                                      target_size=TARGET_SIZE,
                                                      batch_size=BATCH_SIZE,
                                                      class_mode=CLASS_MODE)

validation_flow = validation_data_generator.flow_from_directory(directory=validation_path,
                                                                target_size=TARGET_SIZE,
                                                                batch_size=BATCH_SIZE,
                                                                class_mode=CLASS_MODE,
                                                                shuffle=False)

'''CALLBACKS'''
reduceLro = ReduceLROnPlateau(monitor='val_loss',
                              factor=0.6,
                              patience=2,
                              verbose=True)

earlyStop = EarlyStopping(monitor='val_loss',
                          patience=6,
                          verbose=True,
                          min_delta=1e-4,
                          restore_best_weights=True)


'''BACKBONE'''
base_model = ResNet50(weights='imagenet',
                      include_top=False,
                      input_shape=INPUT_SHAPE)

base_model.trainable = False


'''FUNCTIONAL API'''
inputs = tf.keras.Input(INPUT_SHAPE)
x = base_model(inputs,training=False)
x = GlobalAveragePooling2D()(x)
x = BatchNormalization()(x)
x = Dense(256,activation='relu')(x)
x = Dropout(0.5)(x)
outputs = Dense(1,activation='sigmoid')(x)

model = tf.keras.models.Model(inputs,outputs)

'''HEAD'''
model.compile(optimizer=Adam(learning_rate=1e-4),
                   loss='binary_crossentropy',
                   metrics=['accuracy'])

model.fit(x=train_flow,validation_data=validation_flow,epochs=10,callbacks=[reduceLro])


'''FINE TUNING'''
for layer in base_model.layers[-40:]:
    layer.trainable = True

model.compile(optimizer=Adam(learning_rate=5e-6),
              loss='binary_crossentropy',
              metrics=['accuracy'])


'''FITTING'''
fit_history = model.fit(x=train_flow,validation_data=validation_flow,epochs=16,callbacks=[reduceLro,earlyStop])

print(fit_history.history)
model.save('LeafClassificationModelMainxc.h5')

logger = loggerx.Logger(logfile_path=r"C:\Users\alper\Desktop\Plant Disease Project\logs\SigmoidModelLogs\datas.txt",
                        evaulate_path=r"C:\Users\alper\Desktop\Plant Disease Project\logs\SigmoidModelLogs\evaulates.txt",
                        history=fit_history,
                        model=model,
                        test_data=None).writeLog()

