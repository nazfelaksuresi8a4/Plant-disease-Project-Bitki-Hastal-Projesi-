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
| Çıkış                            | SIGMOID|
| Tensorflow Sürümü                | 2.20.0|
| Keras Sürümü                     | 3.13.0|
| Desteklenen model formatları     | .h5   |

**Model eğitim grafikleri:**


<img width="1226" height="627" alt="image" src="https://github.com/user-attachments/assets/df9bdf23-f517-4590-a964-4e226e15524d" />


                          DETAYLI BILGILENDIRME BELGESI

[plant_disease_projesi_durum_raporu.pdf](https://github.com/user-attachments/files/24870976/plant_disease_projesi_durum_raporu.pdf)


                          ONEMLİ DETAY


Bu projedeki harici-dahili model sistemindeki harici verilecek modeller için; girdi modellerinin **Tensorflow'un *2.20.0* sürümünde** ve **Keras'ın ise *3.13.0* sürümünde** kaydedilmiş olması önemlidir
Aksi halde program size model sürümü uyuşmazlığı benzeri bir hata verecektir veya çoğu zaman sessiz bir şekilde model tanımlanamamasına rağmen hata vermeyecektir ancak tahmin yaparken kesinlike "Model dosyası Bozuk" hatasını sizlere verecektir
Özetle; Lütfen yukarıda belirttiğim kriterlere uyacak modelleri harici olarak programa vermeye özen gösterin harici modeliniz yok ise programda eğittiğim modelleri kullanmanız çok daha sağlıklıdır hatta teknik olarak eğittiğim modelleri kullanmanız harici model kullanmanızdan çok daha basit ve etkili olabilir çoğu zamanda tabi istisnalarda olabilir ayrıca program sadece .h5 formatlı modeller ile çalışabilir
