LEAF SCANNER PROJESİ DETAYLARI

Kullanılan Dataset: PlantVillage
Dataset URL'si: PlantDisease Dataset - Kaggle

Proje İsmi: Leaf Scanner
Kullanılan AI Modeli: Leaf Model
Kullanılan Modelin Sinir Ağı Türü: CNN (Convolutional Neural Networks)
Kullanılan AI Modelinin İsmi: Leaf Model
Hazır Model Mi?: Hayır
0'dan Eğitilen Model Mi?: Evet
Model Türü: Sıralı Model (Sequential)
Proje Geliştiricisi: Ahmet Efe Y-
Overfitting Durumu: Yok
Underfitting Durumu: Yok

Model Eğitim Grafikleri:

<img width="1366" height="671" alt="image" src="https://github.com/user-attachments/assets/2ee85f3d-e9e7-40e4-932a-cc94f182f82c" />


MODEL ÖZELLİKLERİ

Layer (Type)	Output Shape	Param #
Conv2D	(None, 223, 223, 16)	208
MaxPooling2D	(None, 111, 111, 16)	0
Conv2D_1	(None, 110, 110, 32)	2,080
MaxPooling2D_1	(None, 55, 55, 32)	0
Conv2D_2	(None, 54, 54, 64)	8,256
MaxPooling2D_2	(None, 27, 27, 64)	0
Flatten	(None, 46,656)	0
Dense	(None, 128)	5,972,096
Dense_1	(None, 1)	129
