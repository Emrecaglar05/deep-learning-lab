# ✈️ Aircraft Damage Classification & Image Captioning

> Önceden eğitilmiş VGG16 ve BLIP modelleri kullanılarak uçak hasarlarının otomatik sınıflandırılması ve görüntü açıklamalarının oluşturulması.

---

## 📌 Proje Özeti

Bu proje iki temel yapay zeka görevini birleştirmektedir:

1. **Görüntü Sınıflandırması** — VGG16 ile transfer öğrenimi kullanarak uçak hasarlarını `çukur (dent)` ve `çatlak (crack)` olarak sınıflandırma.
2. **Görüntü Altyazılama & Özetleme** — Salesforce BLIP modeli ile görüntüler için otomatik açıklama ve özet üretme.

---

## 🗂️ İçindekiler

- [Proje Yapısı](#proje-yapısı)
- [Kullanılan Teknolojiler](#kullanılan-teknolojiler)
- [Veri Seti](#veri-seti)
- [Model Mimarisi](#model-mimarisi)
- [Kurulum](#kurulum)
- [Görevler](#görevler)
- [Sonuçlar](#sonuçlar)
- [Lisans](#lisans)

---

## 📁 Proje Yapısı

```
aircraft-damage-classification/
├── Final_Project_Classification_and_Captioning.ipynb
├── README.md
└── aircraft_damage_dataset_v1/       # Otomatik indirilir
    ├── train/
    │   ├── dent/
    │   └── crack/
    ├── valid/
    │   ├── dent/
    │   └── crack/
    └── test/
        ├── dent/
        └── crack/
```

---

## 🛠️ Kullanılan Teknolojiler

| Kütüphane | Versiyon | Kullanım Amacı |
|-----------|----------|----------------|
| TensorFlow / Keras | 2.17.1 | Model eğitimi & değerlendirme |
| VGG16 (ImageNet) | — | Transfer öğrenimi ile özellik çıkarma |
| BLIP (Salesforce) | transformers 4.38.2 | Görüntü altyazılama & özetleme |
| PyTorch | 2.2.0 (CPU) | BLIP model backend |
| Pillow | 11.1.0 | Görüntü yükleme & işleme |
| Matplotlib | 3.9.2 | Görselleştirme |
| Pandas / NumPy | 2.2.3 / 1.26.4 | Veri işleme |

---

## 📊 Veri Seti

Veri seti, uçak yüzeylerindeki hasarları gösteren etiketli görüntülerden oluşmaktadır.

- **Kaynak:** [Roboflow Aircraft Damage Detection](https://universe.roboflow.com/youssef-donia-fhktl/aircraft-damage-detection-1j9qk)
- **Lisans:** CC BY 4.0
- **Kategoriler:** `dent` (çukur) | `crack` (çatlak)
- **Bölümler:** Eğitim / Doğrulama / Test

Veri seti notebook çalıştırıldığında otomatik olarak indirilir:
```python
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/ZjXM4RKxlBK9__ZjHBLl5A/aircraft-damage-dataset-v1.tar"
```

---

## 🧠 Model Mimarisi

### Bölüm 1 — VGG16 Transfer Öğrenimi

```
VGG16 (ImageNet ağırlıkları, dondurulmuş)
    ↓
Flatten
    ↓
Dense(512, activation='relu')
    ↓
Dropout(0.3)
    ↓
Dense(512, activation='relu')
    ↓
Dropout(0.3)
    ↓
Dense(1, activation='sigmoid')   ← İkili sınıflandırma çıkışı
```

- **Optimizer:** Adam (lr=0.0001)
- **Loss:** Binary Crossentropy
- **Epochs:** 5
- **Batch Size:** 32
- **Görüntü Boyutu:** 224×224

### Bölüm 2 — BLIP Görüntü Altyazılama

```
Görüntü Yolu
    ↓
BlipCaptionSummaryLayer (Özel Keras Katmanı)
    ├── BlipProcessor  →  Görüntü ön işleme
    └── BlipForConditionalGeneration  →  Metin üretme
         ├── Görev: "caption"  →  Kısa açıklama
         └── Görev: "summary"  →  Detaylı özet
```

---

## ⚙️ Kurulum

```bash
# 1. Repo'yu klonlayın
git clone https://github.com/kullanici-adi/aircraft-damage-classification.git
cd aircraft-damage-classification

# 2. Gerekli kütüphaneleri yükleyin
pip install pandas==2.2.3
pip install tensorflow_cpu==2.17.1
pip install pillow==11.1.0
pip install matplotlib==3.9.2
pip install transformers==4.38.2
pip install torch==2.2.0+cpu torchvision==0.17.0+cpu \
    --index-url https://download.pytorch.org/whl/cpu

# 3. Jupyter Notebook'u başlatın
jupyter notebook Final_Project_Classification_and_Captioning.ipynb
```

> **Not:** GPU kullanıyorsanız `tensorflow_cpu` yerine `tensorflow` kurabilirsiniz.

---

## ✅ Görevler

| # | Görev | Açıklama |
|---|-------|----------|
| 1 | `valid_generator` oluşturma | `valid_datagen` ile doğrulama üreteci |
| 2 | `test_generator` oluşturma | `test_datagen` ile test üreteci |
| 3 | VGG16 yükleme | ImageNet ağırlıklı özellik çıkarıcı |
| 4 | Model derleme | Adam optimizer, binary crossentropy |
| 5 | Model eğitimi | 5 epoch, eğitim & doğrulama üreteci |
| 6 | Doğruluk eğrisi | Eğitim & doğrulama doğruluğu grafiği |
| 7 | Tahmin görselleştirme | Test görüntüleri üzerinde tahmin gösterimi |
| 8 | `generate_text` yardımcı işlevi | BlipCaptionSummaryLayer kullanan fonksiyon |
| 9 | BLIP başlık üretme | Test görüntüsü için otomatik altyazı |
| 10 | BLIP özet üretme | Test görüntüsü için detaylı özet |

---

## 📈 Sonuçlar

Modelin eğitim sürecinde elde ettiği temel metrikler:

- **Test Doğruluğu:** model değerlendirme çıktısında görülebilir
- **Loss Eğrisi:** Eğitim ve doğrulama kayıpları notebook içinde görselleştirilmiştir
- **Doğruluk Eğrisi:** Epoch bazında doğruluk karşılaştırması mevcuttur

---

## 🔍 Örnek Kullanım (BLIP)

```python
import tensorflow as tf

image_path = tf.constant("aircraft_damage_dataset_v1/test/dent/ornek_goruntu.jpg")

# Başlık oluşturma
caption = generate_text(image_path, tf.constant("caption"))
print("Caption:", caption.numpy().decode("utf-8"))

# Özet oluşturma
summary = generate_text(image_path, tf.constant("summary"))
print("Summary:", summary.numpy().decode("utf-8"))
```

---

## 📝 Notlar

- BLIP modeli her zaman %100 doğru açıklama üretmeyebilir; model eğitim verisiyle sınırlıdır.
- VGG16 katmanları dondurulmuş (frozen) olduğu için transfer öğrenimi özellik çıkarma olarak uygulanmıştır.
- Tekrarlanabilirlik için `seed=42` kullanılmıştır.

---

## 👤 Yazar

**Vandana Pandey** — IBM / Skills Network  
Katkıda Bulunanlar: Srishti Srivastava, Aman Aggarwal

---

## 📄 Lisans

Bu proje IBM Corporation tarafından oluşturulmuştur. Veri seti CC BY 4.0 lisansı ile sunulmaktadır.
