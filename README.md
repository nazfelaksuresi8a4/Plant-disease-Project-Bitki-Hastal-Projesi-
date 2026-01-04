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
| Overfitting Durumu               | Yok |
| Underfitting Durumu              | Yok |


Model eğitim grafikleri:
<img width="545" height="307" alt="image" src="https://github.com/user-attachments/assets/96180f8b-1dcf-423e-81ff-0a15421cf046" />

                          MODEL ÖZELLİKLERİ
| **Layer (type)**                  | **Output Shape**        | **Param #**   |
|------------------------------------|-------------------------|---------------|
| **conv2d (Conv2D)**               | (None, 223, 223, 16)     | 208           |
| **max_pooling2d (MaxPooling2D)**  | (None, 111, 111, 16)     | 0             |
| **conv2d_1 (Conv2D)**             | (None, 110, 110, 32)     | 2,080         |
| **max_pooling2d_1 (MaxPooling2D)**| (None, 55, 55, 32)       | 0             |
| **conv2d_2 (Conv2D)**             | (None, 54, 54, 64)       | 8,256         |
| **max_pooling2d_2 (MaxPooling2D)**| (None, 27, 27, 64)       | 0             |
| **flatten (Flatten)**             | (None, 46656)            | 0             |
| **dense (Dense)**                 | (None, 128)             | 5,972,096     |
| **dense_1 (Dense)**               | (None, 1)               | 129           |
