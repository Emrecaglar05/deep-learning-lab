#  %% Veri setini iceriye aktar ve preprocessing : normalizasyon, one - hot encoding

import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras.datasets import cifar10 # veri seti
from tensorflow.keras.utils import to_categorical # encoding
from tensorflow.keras.models import Sequential # siralı model
from tensorflow.keras.layers import Conv2D, MaxPooling2D # Özellik cıkarmak icin kullanılır
from tensorflow.keras.layers import Flatten, Dense, Dropout # sınıflandırmada kullanılır
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator # Veri arttirimi 

from sklearn.metrics import classification_report

import warnings
warnings.filterwarnings("ignore")

# %%
# Veri setini yükleme
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# gorsellestirme
class_labels = ["Airplane", "Automobile", "Bird", "Cat", "Deer", "Dog", "Frog", "Horse", "Ship", "Truck"]

# bazi goruntuleri ve etiketleri gorsellestir
fig, axes = plt.subplots(1, 5, figsize = (15,10))

for i in range(5):
    axes[i].imshow(x_train[i])
    label = class_labels[int(y_train[i])]
    axes[i].set_title(label)
    axes[i].axis("off")
    
plt.show()


# veri seti normalizasyonu
x_train = x_train.astype("float32")/255
x_test = x_test.astype("float32")/255

# one *- hot encoding
y_train = to_categorical(y_train, 10) # 10 sınıf var bundan dolayı 10 yazdık
y_test = to_categorical(y_test, 10)


# %% veri arttirimi (Data Augmentation)

datagen = ImageDataGenerator(
    rotation_range = 20, # 20 dereceye kadar dondurme saglar
    width_shift_range = 0.2, # görüntüyü yatayda %20 kaydırma
    height_shift_range = 0.2, # görüntüyü dikeyde %20 kaydırma
    shear_range = 0.2,  # görüntü üzerinde kaydirma
    zoom_range = 0.2,  # görüntüye zoom uygulama
    horizontal_flip = True, # Görüntüyü yatayda ters cevirme simetrigini alma
    fill_mode = "nearest" # bos alanları doldurmak icin en yakın pikselleri kullanma
    
    )

datagen.fit(x_train) # egitim verileri üzerinde uygula



# %% create, compile and train model

# modeli tanımla
model = Sequential()

# ÖZELLİK CIKARMA : CONV -> RELU -> CONV -> RELU -> POOL -> DROPOUT
 # 32 tane filtre ve boyutu 3*3 lük bir özellik cıkarma eklliyoruz ilk katman oldugu icin x_train 32 32 3 lük kısmı alıyoruz
model.add(Conv2D(32, (3,3), padding= "same", activation = "relu", input_shape = x_train.shape[1:]))
model.add(Conv2D(32, (3,3), activation = "relu"))
model.add(MaxPooling2D(pool_size = (2,2)))
model.add(Dropout(0.25)) # baglantiların %25 ni rasgele olarak kapat overfittingi engeller

# ÖZELLİK CIKARMA : CONV -> RELU -> CONV -> RELU -> POOL -> DROPOUT

model.add(Conv2D(64, (3,3), padding= "same", activation = "relu"))
model.add(Conv2D(64, (3,3), activation = "relu"))
model.add(MaxPooling2D(pool_size = (2,2)))
model.add(Dropout(0.25)) # baglantiların %25 ni rasgele olarak kapat

# Classification : FLATTEN , DENSE , RELU , DROPOUT, DENSE (OUTPUT LAYER)
model.add(Flatten()) # vektör olustur
model.add(Dense(512, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(10, activation="softmax")) # output katmanı

model.summary()

#model derleme
model.compile(optimizer = RMSprop(learning_rate = 0.0001, decay=1e-6),
              loss = "categorical_crossentropy",
              metrics = ["accuracy"])

# model eğitimi
# Modeli eğitmeye başlat
history = model.fit(

    # Data augmentation uygulanmış eğitim verilerini modele gönder
    # x_train : eğitim görüntüleri
    # y_train : görüntü etiketleri
    # batch_size = 64 : model her adımda 64 görüntü görerek öğrenir
    datagen.flow(x_train, y_train, batch_size = 64),

    # Model tüm veri setini 50 kez dolaşarak eğitim yapar
    epochs = 50,

    # Her epoch sonunda test verileri ile doğrulama yapılır
    # x_test : test görüntüleri
    # y_test : test etiketleri
    validation_data = (x_test, y_test)

)
# %% Test model and evaluate performance

# modelin test seti üzerinden tahminini yap
y_pred = model.predict(x_test)

# tahmin edilen sınıflari al
y_pred_class = np.argmax(y_pred, axis=1)

# gerçek sınıflari al
y_true = np.argmax(y_test, axis=1)

# classification report hesapla
report = classification_report(y_true, y_pred_class, target_names=class_labels)

plt.figure()

# kayıp grafikleri
plt.subplot(1, 2, 1)
plt.plot(history.history["loss"], label="Train Loss")
plt.plot(history.history["val_loss"], label="Validation Loss")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.title("Training and Validation Loss")
plt.legend()
plt.grid()

# accuracy görselleştirme
plt.subplot(1, 2, 2)
plt.plot(history.history["accuracy"], label="Train Accuracy")
plt.plot(history.history["val_accuracy"], label="Validation Accuracy")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.title("Training and Validation Accuracy")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
