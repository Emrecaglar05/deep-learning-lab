import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SimpleRNN, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

import keras_tuner as kt
from keras_tuner.tuners import RandomSearch

from sklearn.metrics import classification_report, roc_curve, auc


# =========================
# 1. VERİ YÜKLEME 
# =========================
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=10000)

# padding
maxlen = 100
x_train = pad_sequences(x_train, maxlen=maxlen)
x_test = pad_sequences(x_test, maxlen=maxlen)


# =========================
# 2. MODEL FONKSİYONU
# =========================
def build_model(hp):
    model = Sequential()  # Modeli sıralı katmanlarla oluştur

    model.add(Embedding(
        input_dim=10000,  # Kelime haznesi (top 10.000 kelime)
        output_dim=hp.Int("embedding_output", min_value=32, max_value=128, step=32),  # Kelime vektör boyutu (tunable)
        input_length=maxlen  # Her input cümlesinin uzunluğu
    ))

    model.add(SimpleRNN(
        units=hp.Int("rnn_units_1", min_value=32, max_value=128, step=32),  # RNN hücre sayısı (tunable)
        return_sequences=True # Sonraki RNN katmanına input olarak tüm diziyi döndür
    ))
   
    model.add(SimpleRNN(
        units=hp.Int("rnn_units_2", min_value=64, max_value=256, step=64)  # RNN hücre sayısı (tunable)
    ))


    model.add(Dropout(
        rate=hp.Float("dropout_rate", min_value=0.2, max_value=0.5, step=0.1)  # Overfitting azaltma
    ))

    model.add(Dense(1, activation="sigmoid"))  # Binary classification (0/1 sentiment)

    model.compile(
        optimizer=hp.Choice("optimizer", ["adam", "rmsprop"]),  # Optimizasyon algoritması seçimi
        loss="binary_crossentropy",  # Binary sınıflandırma kaybı
        metrics=["accuracy", tf.keras.metrics.AUC()]  # Accuracy + ROC-AUC metriği
    )

    return model  # Modeli geri döndür (Keras Tuner kullanacak)


# =========================
# 3. KERAS TUNER
# =========================
tuner = RandomSearch(
    build_model,
    objective="val_loss",
    max_trials=10,
    executions_per_trial=1,
    directory="rnn_tuner_directory",
    project_name="imdb_rnn_final"
)

early_stopping = EarlyStopping(
    monitor="val_loss",
    patience=3,
    restore_best_weights=True
)


# =========================
# 4. MODEL ARAMA (TRAINING)
# =========================
tuner.search(
    x_train, y_train,
    epochs=5,
    validation_split=0.2,
    callbacks=[early_stopping],
    verbose=1
)


# =========================
# 5. EN İYİ MODEL
# =========================
best_model = tuner.get_best_models(num_models=1)[0]


# =========================
# 6. MODEL DEĞERLENDİRME
# =========================
loss, accuracy, auc_score = best_model.evaluate(x_test, y_test)

print(f"\nTest Loss: {loss:.4f}")
print(f"Test Accuracy: {accuracy:.4f}")
print(f"Test AUC: {auc_score:.4f}")


# =========================
# 7. TAHMİN + CLASSIFICATION REPORT
# =========================
y_pred_prob = best_model.predict(x_test)
y_pred = (y_pred_prob > 0.5).astype(int)

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))


# =========================
# 8. ROC CURVE
# =========================
fpr, tpr, _ = roc_curve(y_test, y_pred_prob)
roc_auc = auc(fpr, tpr)

plt.figure()
plt.plot(fpr, tpr, color="darkorange", lw=2,
         label="ROC Curve (AUC = %0.2f)" % roc_auc)

plt.plot([0, 1], [0, 1], color="blue", lw=2, linestyle="--")

plt.xlim([0, 1])
plt.ylim([0, 1.05])

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve - IMDB Sentiment Analysis")
plt.legend()
plt.show()