import tensorflow as tf
from tensorflow.keras.models import Sequential,load_model
from tensorflow.keras.layers import  Dense,Conv2D,MaxPooling2D
from tensorflow.keras.preprocessing.image import  ImageDataGenerator
from tensorflow.keras.preprocessing import  image
from sklearn.preprocessing import  LabelEncoder
from sklearn.model_selection import  train_test_split
import image_processing
import numpy as np

class ArtificalIntelligence:
    def __init__(self,epochs=None,
                 patience=None,
                 factor=None,
                 dataset_path=None,
                 horizontal_flip=None,
                 zoom_range=None,
                 augomention=None,
                 valitation_split=None,
                 rotation_range=None,
                 test_shuffle=None,
                 target_size=None,
                 batch_size=None,
                 actived_callbacks=None):
        self.epochs = epochs
        self.patience = patience
        self.factor = factor
        self.dataset_path = dataset_path
        self.horizontal_flip = horizontal_flip
        self.zoom_range = zoom_range
        self.augomention = augomention
        self.validation_split = valitation_split
        self.rotation_range = rotation_range
        self.test_shuffle = test_shuffle
        self.target_size = target_size
        self.batch_size = batch_size
        self.actived_callbacks = actived_callbacks

    def returnModelSummary(self,filepath):
        try:
            if isinstance(filepath,str) and filepath.endswith('.h5'):
                model = load_model(filepath)
                arr,string = [],''

                summary = model.summary(print_fn=lambda x: arr.append(x + '\n'))

                return (string.join(arr),0)

            else:
                return (f'Model dosyasının .h5 ile bitmesine dikkat edin. Ve seçtiğiniz modelin bozuk veya çalışır olup olmadığından emin olunuz. Model şu anda erişilebilir bir durumda değil\nHata kodu: 1\nModel yolu: {filepath}',1)

        except Exception as e0:
            return (f'Model bilgileri çekilirken bir sorun ile karşılaşıldı....\nHata kodu: 2\nException:{e0}',2)

    def predictModel(self,model,matlike,mode,batch_size):
        artifical_intelligence_model = model

        if artifical_intelligence_model is not None:
            if matlike is not None:
                try:
                    image_matrix = image_processing.İmageProcesser().to_matrix(matlike)
                    predict_output = artifical_intelligence_model.predict(x=image_matrix,batch_size=batch_size)

                    print(predict_output)

                    return predict_output
                except Exception as e:
                    print(e)
                    return image_matrix
