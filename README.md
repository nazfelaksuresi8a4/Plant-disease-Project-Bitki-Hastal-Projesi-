## LEAF SCANNER PROJESİ DETAYLARI

| Özellik                          | Açıklama |
|----------------------------------|----------|
| Kullanılan Dataset               | PlantVillage |
| Dataset URL'si                   | https://www.kaggle.com/datasets/emmarex/plantdisease |
| Proje İsmi                       | Leaf Scanner |
| Kullanılan AI Modeli             | Leaf Model |
| Modelin Sinir Ağı Türü           | CNN (Convolutional Neural Networks) |
| Kullanılan AI Modelinin İsmi     | Leaf Model |
| Hazır Model Mi?                  | Hayır |
| 0'dan Eğitilen Model Mi?         | Evet |
| Model Türü                       | Sequential (Sıralı Model) |
| Proje Geliştiricisi              | Ahmet Efe Y- |
| Overfitting Durumu               | Şu anlık Gözükmüyor |
| Underfitting Durumu              | Şu anlık gözükmüyor |
| Overfitting Risk durumu          | Düşük seviyede risk taşıyor|
| Underfitting Durumu              | Çok düşük seviyede risk taşıyor|

Model eğitim grafikleri:


## LEAF SCANNER PROJESİ DETAYLARI

| Özellik                          | Açıklama |
|----------------------------------|----------|
| Kullanılan Dataset               | PlantVillage |
| Dataset URL'si                   | https://www.kaggle.com/datasets/emmarex/plantdisease |
| Proje İsmi                       | Leaf Scanner |
| Kullanılan AI Modeli             | Leaf Model |
| Modelin Sinir Ağı Türü           | CNN (Convolutional Neural Networks) |
| Kullanılan AI Modelinin İsmi     | Leaf Model |
| Hazır Model Mi?                  | Hayır |
| 0'dan Eğitilen Model Mi?         | Evet |
| Model Türü                       | Sequential (Sıralı Model) |
| Proje Geliştiricisi              | Ahmet Efe Y- |
| Overfitting Durumu               | Şu anlık Gözükmüyor |
| Underfitting Durumu              | Şu anlık gözükmüyor |
| Overfitting Risk durumu          | Düşük seviyede risk taşıyor|
| Underfitting Durumu              | Çok düşük seviyede risk taşıyor|

Model eğitim grafikleri:


<img width="1366" height="671" alt="learning_graph" src="https://github.com/user-attachments/assets/0e9c105e-8da5-4cd9-bffa-8e248e57155e" />


                          MODEL ÖZELLİKLERİ
| Layer (type)                     | Output Shape            | Param # |
|----------------------------------|-------------------------|---------|
| Conv2D                           | (None, 223, 223, 16)    | 208     |
| MaxPooling2D                    | (None, 111, 111, 16)    | 0       |
| Conv2D                           | (None, 110, 110, 32)    | 2,080   |
| MaxPooling2D                    | (None, 55, 55, 32)      | 0       |
| Conv2D                           | (None, 54, 54, 64)      | 8,256   |
| MaxPooling2D                    | (None, 27, 27, 64)      | 0       |
| Conv2D                           | (None, 26, 26, 128)     | 32,896  |
| MaxPooling2D                    | (None, 13, 13, 128)     | 0       |
| Flatten                          | (None, 21,632)          | 0       |
| Dense (ReLU)                     | (None, 8)               | 173,064 |
| Dense (Sigmoid)                 | (None, 1)               | 9       |
| **Total Parameters**             |                         | **649,541** |
| **Trainable Parameters**         |                         | **216,513** |
| **Non-trainable Parameters**     |                         | **0** |




                          MODEL ÖZELLİKLERİ
| Layer (type)                     | Output Shape            | Param # |
|----------------------------------|-------------------------|---------|
| Conv2D                           | (None, 223, 223, 16)    | 208     |
| MaxPooling2D                    | (None, 111, 111, 16)    | 0       |
| Conv2D                           | (None, 110, 110, 32)    | 2,080   |
| MaxPooling2D                    | (None, 55, 55, 32)      | 0       |
| Conv2D                           | (None, 54, 54, 64)      | 8,256   |
| MaxPooling2D                    | (None, 27, 27, 64)      | 0       |
| Conv2D                           | (None, 26, 26, 128)     | 32,896  |
| MaxPooling2D                    | (None, 13, 13, 128)     | 0       |
| Flatten                          | (None, 21,632)          | 0       |
| Dense (ReLU)                     | (None, 8)               | 173,064 |
| Dense (Sigmoid)                 | (None, 1)               | 9       |
| **Total Parameters**             |                         | **649,541** |
| **Trainable Parameters**         |                         | **216,513** |
| **Non-trainable Parameters**     |                         | **0** |

