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


<img width="1366" height="671" alt="learning_graph" src="https://github.com/user-attachments/assets/0e9c105e-8da5-4cd9-bffa-8e248e57155e" />


                          MODEL ÖZELLİKLERİ
| Layer (type)                    | Output Shape           | Param #      |
|----------------------------------|------------------------|--------------|
| **conv2d (Conv2D)**              | (None, 223, 223, 16)   | 208          |
| **max_pooling2d (MaxPooling2D)** | (None, 111, 111, 16)   | 0            |
| **conv2d_1 (Conv2D)**            | (None, 110, 110, 32)   | 2,080        |
| **max_pooling2d_1 (MaxPooling2D)**| (None, 55, 55, 32)     | 0            |
| **conv2d_2 (Conv2D)**            | (None, 54, 54, 64)     | 8,256        |
| **max_pooling2d_2 (MaxPooling2D)**| (None, 27, 27, 64)     | 0            |
| **flatten (Flatten)**            | (None, 46656)          | 0            |
| **dense (Dense)**                | (None, 64)             | 2,986,048    |
| **dense_1 (Dense)**              | (None, 1)              | 65           |
| **Total params**                 |                        | 8,989,973    |
| **Trainable params**             |                        | 2,996,657    |
| **Non-trainable params**         |                        | 0            |
| **Optimizer params**             |                        | 5,993,316    |

