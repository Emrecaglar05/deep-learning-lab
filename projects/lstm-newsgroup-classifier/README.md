# 📰 LSTM ile 20 Newsgroups Metin Sınıflandırma

> Derin öğrenme tabanlı bir NLP projesi — LSTM ağı kullanarak 20 farklı haber kategorisini otomatik olarak sınıflandırır.

---

## 📌 Proje Özeti

Bu proje, **scikit-learn**'ün klasik benchmark veri seti olan **20 Newsgroups**'u kullanarak metin sınıflandırma problemi çözer. Ham metin verisini tokenize edip pad'ledikten sonra Keras ile inşa edilen **LSTM** modeline besler.

| Parametre | Değer |
|---|---|
| Veri seti | 20 Newsgroups (18 846 metin) |
| Kategori sayısı | 20 |
| Model | Embedding → LSTM → Dropout → Dense |
| Kayıp fonksiyonu | Sparse Categorical Crossentropy |
| Optimizer | Adam |
| Max kelime | 10 000 |
| Dizi uzunluğu | 100 token |

---

## 🗂️ Proje Yapısı

```
lstm-newsgroup-classifier/
│
├── notebooks/
│   └── lstm_newsgroup_classifier.py   # Ana notebook (Colab'da çalıştır)
│
├── outputs/
│   └── training_history.png           # Eğitim grafikleri (otomatik oluşur)
│
├── requirements.txt                   # Bağımlılıklar
└── README.md
```

---

## 🚀 Hızlı Başlangıç

### ▶️ Google Colab'da Çalıştırma (Önerilen)

1. [Google Colab](https://colab.research.google.com/) → **File → Upload notebook** ile `.py` dosyasını yükleyin  
   *ya da doğrudan GitHub'dan açın:*

   ```
   https://colab.research.google.com/github/<KULLANICI_ADINIZ>/lstm-newsgroup-classifier/blob/main/notebooks/lstm_newsgroup_classifier.py
   ```

2. Colab'da GPU'yu etkinleştirin:  
   **Runtime → Change runtime type → T4 GPU**

3. Bağımlılıkları yükleyin (ilk hücre olarak ekleyin):

   ```python
   !pip install -r requirements.txt
   ```

4. Tüm hücreleri çalıştırın: **Runtime → Run all**

---

### 💻 Yerel Ortamda Çalıştırma

```bash
# 1. Repoyu klonla
git clone https://github.com/<KULLANICI_ADINIZ>/lstm-newsgroup-classifier.git
cd lstm-newsgroup-classifier

# 2. Sanal ortam oluştur ve aktive et
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Bağımlılıkları yükle
pip install -r requirements.txt

# 4. Jupyter ile çalıştır
jupyter notebook notebooks/lstm_newsgroup_classifier.py
```

---

## 🧠 Model Mimarisi

```
┌─────────────────────────────────────────────────────┐
│  Input        (batch, 100)  — token dizisi          │
├─────────────────────────────────────────────────────┤
│  Embedding    (batch, 100, 64)  — kelime vektörleri │
├─────────────────────────────────────────────────────┤
│  LSTM         (batch, 64)   — bağlamı öğrenir       │
├─────────────────────────────────────────────────────┤
│  Dropout 0.5  — aşırı öğrenmeyi engeller            │
├─────────────────────────────────────────────────────┤
│  Dense (20)   Softmax  — sınıf olasılıkları         │
└─────────────────────────────────────────────────────┘
```

---

## 📊 Çıktılar

Eğitim tamamlandıktan sonra `outputs/` klasöründe şunlar oluşur:

- **`training_history.png`** — Loss ve Accuracy eğrileri (eğitim / doğrulama)

Konsola yazdırılanlar:

- Test Loss / Test Accuracy / Test F1 Score
- Sınıflandırma raporu (per-class precision, recall, F1)
- Örnek tahminler

---

## ⚙️ Hiperparametreler

Dosyanın üst kısmındaki sabitler kolayca değiştirilebilir:

```python
MAX_WORDS      = 10_000   # Sözlük büyüklüğü
MAX_LEN        = 100      # Giriş dizisi uzunluğu
EMBEDDING_DIM  = 64       # Embedding boyutu
LSTM_UNITS     = 64       # LSTM hücre sayısı
DROPOUT_RATE   = 0.5      # Dropout oranı
EPOCHS         = 10       # Maksimum epoch
BATCH_SIZE     = 32       # Batch boyutu
PATIENCE       = 5        # EarlyStopping sabrı
```

---

## 🔧 Kullanılan Teknolojiler

| Kütüphane | Kullanım Amacı |
|---|---|
| `scikit-learn` | Veri seti, LabelEncoder, train/test split |
| `TensorFlow / Keras` | LSTM modeli, Tokenizer, pad_sequences |
| `NumPy / Pandas` | Veri işleme |
| `Matplotlib / Seaborn` | Görselleştirme |

---

## 📝 Notlar

- **EarlyStopping** ile `val_accuracy` 5 epoch boyunca iyileşmezse eğitim otomatik durur ve en iyi ağırlıklar geri yüklenir.
- Model ilk eğitimde ~%70-75 test doğruluğuna ulaşabilir; daha yüksek başarı için `Bi-LSTM`, `pre-trained embeddings (GloVe/FastText)` veya **Transformer** mimarisi denenebilir.
- `predict_category()` fonksiyonu ile eğitilmiş modeli yeni metinler üzerinde kolayca test edebilirsiniz.

---

## 📄 Lisans

MIT License — dilediğiniz gibi kullanabilir ve geliştirebilirsiniz.
