" MNİST DATASET İLE GÖRÜNTÜ SINIFLANDIRMA ALGORİTMASI " 

# %% Veri setinin hazırlanmasi ve preprocessing.
from keras.datasets import mnist
from keras.utils import to_categorical # Kategorik verilere cevirme
from keras.callbacks import EarlyStopping, ModelCheckpoint # Eğitimi durdurma ve eğitim aşamasındaki parametrelerin kaydedilmesi
from keras.models import Sequential # sirali model
from keras.layers import Dense # Bagli katmanlar

from keras.models import load_model # Modelin geri yüklenmesi

import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# mnist veri setini yukle, egitim ve test veri seti olarak ayri ayri yükle

(x_train, y_train), (x_test, y_test) = mnist.load_data()

plt.figure(figsize=(10,5))

for i in range(6):
    plt.subplot(2, 3 , i+1)
    plt.imshow(x_train[i], cmap="gray")
    plt.title(f"index: {i}, Label: {y_train[i]}")
    plt.axis("off")
plt.show()

# Veri setini normalize edelim, 0-255 aralıgındaki pixel degerlerini 0-1 arasina olceklendırıyoruz
# Bu kod: "Görüntü verilerini düzleştirip, piksel değerlerini 0-1 arasına normalize ederek sinir ağı için uygun hale getirir."
x_train = x_train.reshape((x_train.shape[0], x_train.shape[1] * x_train.shape[2])).astype("float32")/255
x_test = x_test.reshape((x_test.shape[0], x_test.shape[1] * x_test.shape[2])).astype("float32")/255

y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)
# %% ANN modelinin olusturulmasi ve derlenmesi
model = Sequential()

# ikj katman : 512 nörondan oluscak , relu aktivasyon fonk kullancak , input size 28*28=784

model.add(Dense(512, activation="relu", input_shape = (28*28,)))

# ikini katman : 512 cell, relu activation: tanh
model.add(Dense(256, activation="tanh")) 

# output layer : 10 tane olmak zorunda, activation : softmax kullanıcaz ikiden fazla sınıf var cünkü

model.add(Dense(10, activation="softmax"))

model.summary()

# model derlemesi : optimizer (adam : buyuk veri ve kompleks aglar icin idealdir)
# model lermesi : loss (categorical_crossentropy)
# model derlemesi : metrik (accuary)

model.compile(
    optimizer="adam",
    loss = "categorical_crossentropy",
    metrics = ["accuracy"]
    )


# %% Callback'lerin tanimlanmasi ve ANN egitilmesi

# bu callback eğer model belli bir süre iyileşmiyorsa eğitimi durdurarak overfitting önler
# monitor : dogrulama setindeki (val) kaybi (loss) izler
# patience : 3 -> 3 epoch boyunca val loss değişmiyorsa erken durdurma yap
# restore_Best_weights : en iyi modelin agirliklarını geri yükler

early_stopping = EarlyStopping(monitor= "val_loss", patience=3, restore_best_weights=True, verbose=1)

# en iyi modelin agırlıklarını kaydeder
# save_best_only : sadece en iyi performans gösteren modeli kaydeder
checkpoint = ModelCheckpoint("ann_best_model.h5", monitor= "val_loss", save_best_only=True)

# model training = 10 epochs, batch_size = 66, dogrulama seti orani = %20
# model her biri 60 parcadan olusan 60000 'lik  veri setini  1000 kerede train edecek ve biz buna 1 epoch diyecegiz
# ama validayson ayarıda yapıyoruz ondan dolayı 60000 lik verinin belli bir kısmı doğrulama verisi olarak ayrıldı
history = model.fit(x_train, y_train,
          epochs=10,
          batch_size= 60,
          validation_split = 0.2,
          callbacks=[early_stopping, checkpoint]) 

# %% Model Degerlendirme , Görsellestirme , model save and load

# test verisi ile model performansi degerlendirme
# evulate : modelin test verisi üzerindeki loss ve accuracy hesaplar

test_loss, test_acc = model.evaluate(x_test, y_test)

print(f"Test acc : {test_acc}, test loss: {test_loss}")


# Training ve Validation Accuracy
plt.figure(figsize=(8,5))
plt.plot(history.history["accuracy"], marker="o", label="Training Accuracy")
plt.plot(history.history["val_accuracy"], marker="o", label="Validation Accuracy")
plt.title("ANN Accuracy on MNIST Data Set")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.grid(True)
plt.show()

# Training ve Validation Loss
plt.figure(figsize=(8,5))
plt.plot(history.history["loss"], marker="o", label="Training Loss")
plt.plot(history.history["val_loss"], marker="o", label="Validation Loss")
plt.title("ANN Loss on MNIST Data Set")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.grid(True)

plt.show()

#modeli kaydet
model.save("final_mnist_ann_model.h5")

loaded_model = load_model("final_mnist_ann_model.h5")
