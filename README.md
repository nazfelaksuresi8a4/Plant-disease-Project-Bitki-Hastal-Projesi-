[plant_disease_projesi_durum_raporu.pdf]([plant_disease_projesi_durum_raporu.pdf](https://github.com/user-attachments/files/25222305/plant_disease_projesi_durum_raporu.pdf)
)## LEAF SCANNER PROJESİ DETAYLARI



| Özellik                          | Açıklama |
|----------------------------------|----------|
| Kullanılan Datasetler            | PlantVillage & PlantDoc|
| Datasetlerin URL'si              | https://www.kaggle.com/datasets/emmarex/plantdisease  &  https://www.kaggle.com/datasets/abdulhasibuddin/plant-doc-dataset|
| Proje İsmi                       | Plant Disease Project |
| Kullanılan AI Modelleri          | DC Model & DF model   |
| Modellerin Sinir Ağı Türü           | CNN (Convolutional Neural Networks) |
| Kullanılan AI Modelinin İsmi     | Leaf Model |
| Hazır Model Mi?                  | Kısmen |
| 1'dan Eğitilen Model Mi?         | Hayır  |
| Model Türü                       | ResNet50 (Residual Networks 50) |
| Proje Geliştiricisi              | Ahmet Efe Y- |
| Overfitting Durumu               | Şu anlık Gözükmüyor(Başlangıç saptandı) |
| Underfitting Durumu              | Şu anlık gözükmüyor(+) |
| Overfitting Risk durumu          | Düşük seviyede risk taşıyor(+)|
| Underfitting Durumu              | Çok düşük seviyede risk taşıyor(+)|
| Çıkış                            | SIGMOID & Softmax|
| Tensorflow Sürümü                | 2.20.0|
| Keras Sürümü                     | 3.13.0|
| Desteklenen model formatları     | .h5   |
| Desteklenen görsel boyutları     | 224x224 |
| Desteklenen görsel boyutu:       | 1,224,224 |
| Batch Dimension:                 | EVET       |
| 0-255 arası görsel normalizasyonu: | HAYIR    |

                                  **Model eğitim grafikleri:  (DC MODEL)*

<img width="503" height="469" alt="image" src="https://github.com/user-attachments/assets/bd17f139-0f28-4709-ab88-abd50642bb49" />

                          DETAYLI BILGILENDIRME BELGESI

[plant_disease_projesi_durum_raporu.pdf](https://github.com/user-attachments/files/25222305/plant_disease_projesi_durum_raporu.pdf)




                  **PROGRAM DİZİN YAPISI**

<img width="193" height="905" alt="image" src="https://github.com/user-attachments/assets/e5be3339-5c1b-45ee-bc62-37f8220b78f3" />

                          ONEMLİ DETAY

Bu projedeki harici-dahili model sistemindeki harici verilecek modeller için; girdi modellerinin **Tensorflow'un *2.20.0* sürümünde** ve **Keras'ın ise *3.13.0* sürümünde** kaydedilmiş olması önemlidir
Aksi halde program size model sürümü uyuşmazlığı benzeri bir hata verecektir veya çoğu zaman sessiz bir şekilde model tanımlanamamasına rağmen hata vermeyecektir ancak tahmin yaparken kesinlike "Model dosyası Bozuk" hatasını sizlere verecektir
Özetle; Lütfen yukarıda belirttiğim kriterlere uyacak modelleri harici olarak programa vermeye özen gösterin harici modeliniz yok ise programda eğittiğim modelleri kullanmanız çok daha sağlıklıdır hatta teknik olarak eğittiğim modelleri kullanmanız harici model kullanmanızdan çok daha basit ve etkili olabilir çoğu zamanda tabi istisnalarda olabilir ayrıca program sadece .h5 formatlı modeller ile çalışabilir


MODEL AÇILIMLARI
----------------------------------------------------------
(+)DC Model -> Disease Classification Model => Sigmoid 0-1
________________________________________________________________
(+)DF Model -> Disease Finding Model => Softmax Multiclass
________________________________________________________________
