import  tensorflow as tf        #tensorflow importu
from keras.src.layers import Flatten  #2D konvensiyonel ağı flatten etmek için
from tensorflow.keras.preprocessing.image import  ImageDataGenerator  #flow(akış) ile dosya sınıflarını alabilmek için
#from tensorflow.keras.preprocessing import  image
from tensorflow.keras.layers import  Dense,Conv2D,MaxPooling2D   #Dense düğümler Conv2D konvensiyonel ağlar ve MaxPooling2D ise 2D Konvensiyonel ağda girdi verilerini Pooling yapmak için
from tensorflow.keras.models import  Sequential  #Sıralı Hazır model
import cv2 as cv  #Görüntü girdisini modele dayalı preprocess etmek için
import numpy as np  #Matematiksel görsel işlemleri için(Burada batch'e çevirmek için kullanıldı)

image_path = r"C:\Users\alper\Downloads\j38kgf1_curry-leaves_625x300_20_March_24.webp" #Girdimiz

img = cv.imread(image_path)  #Matlike'a çevirdik

rgb = cv.cvtColor(img,cv.COLOR_BGR2RGB) #Matlike'ı RGB ye çevirdik

norm = rgb.astype('float32') / 255.0 #veri tipini np.float32 yaptık ve 0-255.0 arası normalize ettik

resized = cv.resize(norm,dsize=(224,224)) #224x224 büyüklüğünde yeniden boyutlandırdık

batch_dim = np.expand_dims(resized,axis=0) #batch'e çevirdik

shape = batch_dim.shape #olası durumlar için kontrol edebilmek için shape'i bir değişkene atadık

print(shape) #(1,224,224,3)
base_url = r'C:\Users\alper\Desktop\PlantVillage' #Dataset yolu
train_url = base_url + r'\train' #training klasörü
test_url = base_url + r'\test'   #test klasörü

datagen = ImageDataGenerator(    #Her görseli modele aktarırken Augmention uygulamak için
    rescale=1./255,
    rotation_range=20,
    horizontal_flip=True,
    zoom_range=0.2
)

train_data = datagen.flow_from_directory(   #Sınıfları Akış halinde almak ve gerekli preprocess işlemlerini uygulamak için
    directory=train_url,
    target_size=(224,224),
    batch_size=16,
    class_mode='binary'
)

test_data = datagen.flow_from_directory(
    directory=test_url,
    target_size=(224,224),
    batch_size=16,
    class_mode='binary'
)

model = Sequential(    #Sıralı model oluşturduk
    layers=[Conv2D(filters=16,kernel_size=(2,2),strides=(1,1),activation='relu',input_shape=(224,224,3)),  #16 filtrelik konvensiyonel sinir ağı ve (2,2)'lik pooling  ve (224,224,3) lük RGB girdi verisi boyutu
            MaxPooling2D(2,2),

            Conv2D(filters=32,kernel_size=(2,2),strides=(1,1),activation='relu'),  #32 filtrelik konvensiyonel sinir ağı ve (2,2)'lik pooling
            MaxPooling2D(2,2),

            Conv2D(filters=64, kernel_size=(2, 2), strides=(1, 1), activation='relu'),  #64 filtrelik konvensiyonel sinir ağı ve (2,2)'lik pooling
            MaxPooling2D(2, 2),

            Flatten(),    #konvesnsiyonel ağın 2D boyutunu 1D vektöre indirgemek için kullanılan Flatten() fonksiyonu
            Dense(64,activation='relu'),   #128 unitelik düğüm ve relu aktivasyon fonksiyonu
            Dense(1,activation='sigmoid')   #0-1 aralığındaki SİGMOİD fonksiyonu çıktısı ve 1 unitelik düğüm
            ]
)
model.compile(optimizer='adam',        #modeli compile etmek için(derlemek için) kullanılan fonksiyon(optmizer adam seçildi metrics'e sadece accuracy verildi ve loss(kayıp fonksiyonu) binary_crossentropy seçildi)
              metrics=['accuracy'],
              loss='binary_crossentropy'
              )

history = model.fit(x=train_data,batch_size=16,validation_data=test_data,epochs=16) #Model eğitimi için

import matplotlib.pyplot as plt

# Training history for accuracy and loss
history_dict = history.history


fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Accuracy grafiği
axs[0, 0].plot(history_dict['accuracy'], label='Training Accuracy', color='blue')
axs[0, 0].plot(history_dict['val_accuracy'], label='Validation Accuracy', color='orange')
axs[0, 0].set_title('Accuracy over Epochs')
axs[0, 0].set_xlabel('Epochs')
axs[0, 0].set_ylabel('Accuracy')
axs[0, 0].axhline(y=0.5, color='gray', linestyle='--')
axs[0, 0].axvline(x=len(history_dict['accuracy']) // 2, color='gray', linestyle='--')
axs[0, 0].legend()

# Loss grafiği
axs[0, 1].plot(history_dict['loss'], label='Training Loss', color='blue')
axs[0, 1].plot(history_dict['val_loss'], label='Validation Loss', color='orange')
axs[0, 1].set_title('Loss over Epochs')
axs[0, 1].set_xlabel('Epochs')
axs[0, 1].set_ylabel('Loss')
axs[0, 1].axhline(y=0.5, color='gray', linestyle='--')  #
axs[0, 1].axvline(x=len(history_dict['loss']) // 2, color='gray', linestyle='--')
axs[0, 1].legend()

# Accuracy Scatter plot
axs[1, 0].scatter(range(1, len(history_dict['accuracy']) + 1), history_dict['accuracy'], label='Training Accuracy', color='blue', s=10)
axs[1, 0].scatter(range(1, len(history_dict['val_accuracy']) + 1), history_dict['val_accuracy'], label='Validation Accuracy', color='orange', s=10)
axs[1, 0].set_title('Accuracy Scatter Plot')
axs[1, 0].set_xlabel('Epochs')
axs[1, 0].set_ylabel('Accuracy')
axs[1, 0].axhline(y=0.5, color='gray', linestyle='--')
axs[1, 0].axvline(x=len(history_dict['accuracy']) // 2, color='gray', linestyle='--')
axs[1, 0].legend()

# Loss Scatter plot
axs[1, 1].scatter(range(1, len(history_dict['loss']) + 1), history_dict['loss'], label='Training Loss', color='blue', s=10)
axs[1, 1].scatter(range(1, len(history_dict['val_loss']) + 1), history_dict['val_loss'], label='Validation Loss', color='orange', s=10)
axs[1, 1].set_title('Loss Scatter Plot')
axs[1, 1].set_xlabel('Epochs')
axs[1, 1].set_ylabel('Loss')
axs[1, 1].axhline(y=0.5, color='gray', linestyle='--')  #
axs[1, 1].axvline(x=len(history_dict['loss']) // 2, color='gray', linestyle='--')
axs[1, 1].legend()

# Layout ayarları
plt.tight_layout()
plt.show()


pred = model.predict(x=batch_dim, #İlk başta belirttiğimiz görseli modele verip modele tahmin yaptırmak için
              batch_size=16,
              )
print(model.summary())

print(pred[0][0]) # Modelin sonucuna ulaşmak için

#NOT: BU KODDAN SONRA MODEL leaf_model.h5 OLARAK KAYDEDİLMİŞTİR VE AKTİF OLARAK EGİTİME DEVAM EDİLMEK ÜZERE HALEN GELİŞTİRİLİYOR
