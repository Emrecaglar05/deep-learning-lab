import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image
import os



class PredictionPipeline:
    def __init__(self, filename):
        self.filename = filename


    
    def predict(self):
        # Eğitilmiş modeli yükle (artifacts/training/model.h5 veya model/ klasöründen)
        try:
            # Önce artifacts klasöründen dene
            model_path = os.path.join("artifacts", "training", "model.h5")
            if not os.path.exists(model_path):
                # Yoksa model klasöründen dene
                model_path = os.path.join("model", "model.h5")
            
            print(f"Model yükleniyor: {model_path}")
            
            # Eski Keras modellerini yüklemek için compile=False kullan
            model = keras.models.load_model(model_path, compile=False)
            
            # Modeli yeniden compile et
            model.compile(
                optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )
            
        except Exception as e:
            print(f"Model yükleme hatası: {e}")
            raise

        imagename = self.filename
        
        # Görüntüyü yükle ve ön işleme
        test_image = image.load_img(imagename, target_size=(224, 224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        test_image = test_image / 255.0  # Normalizasyon
        
        # Tahmin yap
        prediction = model.predict(test_image)
        result = np.argmax(prediction, axis=1)
        
        print(f"Tahmin olasılıkları: {prediction}")
        print(f"Tahmin sonucu: {result}")

        # Sonucu döndür
        # result[0] == 0: Coccidiosis (Hastalıklı)
        # result[0] == 1: Healthy (Sağlıklı)
        if result[0] == 1:
            prediction_label = 'Healthy'
            return [{"image": prediction_label}]
        else:
            prediction_label = 'Coccidiosis'
            return [{"image": prediction_label}]