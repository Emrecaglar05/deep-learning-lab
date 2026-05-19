# 🍎 Meyve Sınıflandırması – Transfer Öğrenmesi ile VGG16

> **VGG16** ve transfer öğrenmesi kullanılarak **fruits-360** veri seti üzerinde eğitilmiş bir meyve görüntüsü sınıflandırıcısı.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/KULLANICI_ADIN/REPO_ADIN/blob/main/Fruit_Classification_VGG16_Colab.ipynb)
![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?logo=tensorflow)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 Proje Hakkında

Bu proje, **transfer öğrenmesi** yöntemiyle önceden ImageNet üzerinde eğitilmiş **VGG16** modelini meyve görüntülerine uyarlamayı gösterir. İki aşamalı bir eğitim stratejisi izlenir:

1. **Özellik Çıkarma** — VGG16 katmanları dondurulur, yalnızca üste eklenen sınıflandırma katmanları eğitilir.
2. **İnce Ayar (Fine-Tuning)** — VGG16'nın son 5 katmanı açılarak meyveye özgü özellikler öğrenilir.

---

## 🗂️ Proje Yapısı

```
├── Fruit_Classification_VGG16_Colab.ipynb   # Ana notebook (Colab için optimize)
├── README.md
└── fruits-360-original-size/                # İndirilen veri seti (runtime'da oluşur)
    └── fruits-360-original-size/
        ├── Training/
        ├── Validation/
        └── Test/
```

---

## 🚀 Hızlı Başlangıç

### Google Colab (Önerilen)

1. Yukarıdaki **"Open in Colab"** rozetine tıkla
2. `Çalışma Zamanı → Çalışma Zamanı Türünü Değiştir → GPU (T4)` seç
3. `Çalışma Zamanı → Tümünü Çalıştır` ile başlat

> ⏳ Veri seti indirme internet hızına göre **~30 dakika** sürebilir.

### Yerel Ortam

```bash
# Repoyu klonla
git clone https://github.com/KULLANICI_ADIN/REPO_ADIN.git
cd REPO_ADIN

# Gerekli kütüphaneleri kur
pip install tensorflow matplotlib numpy scikit-learn

# Jupyter ile aç
jupyter notebook Fruit_Classification_VGG16_Colab.ipynb
```

---

## 📦 Gereksinimler

| Kütüphane | Versiyon |
|---|---|
| Python | ≥ 3.9 |
| TensorFlow / Keras | ≥ 2.12 |
| NumPy | ≥ 1.24 |
| Matplotlib | ≥ 3.7 |
| scikit-learn | ≥ 1.3 |

---

## 📊 Veri Seti

**Fruits 360 – Original Size**
- **Kaynak:** [IBM Cloud Object Storage](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/4yIRGlIpNfKEGJYMhZV52g/fruits-360-original-size.zip)
- Eğitim, Doğrulama ve Test olmak üzere 3 bölüme ayrılmıştır
- Her sınıf kendi klasöründe yer alır (`Training/apple_braeburn_1/` vb.)

---

## 🧠 Model Mimarisi

```
VGG16 (ImageNet ağırlıkları, include_top=False)
    └── GlobalAveragePooling2D
    └── Dense(256, relu)
    └── BatchNormalization
    └── Dropout(0.3)
    └── Dense(num_classes, softmax)
```

**Eğitim Stratejisi:**

| Aşama | Öğrenme Oranı | Epoch | Açıklama |
|---|---|---|---|
| Özellik Çıkarma | 1e-3 | 5 | Tüm VGG16 dondurulmuş |
| İnce Ayar | 1e-5 | 5 | Son 5 katman açık |

---

## 📋 Notebook Adımları

| Adım | Açıklama |
|---|---|
| 1 | Ortam kurulumu ve GPU kontrolü |
| 2 | Kütüphane kurulumu |
| 3 | Import'lar |
| 4 | Veri setini indir ve çıkart |
| 5 | Klasör yollarını ayarla ve doğrula |
| 6 | Veri üreticilerini kur (augmentation dahil) |
| 7 | VGG16 tabanlı model mimarisini oluştur |
| 8 | Modeli derle |
| 9 | İlk eğitimi çalıştır |
| 10 | İnce ayar (fine-tuning) |
| 11 | Test setinde değerlendir |
| 12 | Eğitim grafiklerini görselleştir |
| 13 | Örnek görüntüler üzerinde tahmin yap |

---

## ⚙️ Callback'ler

- **EarlyStopping** — `val_loss` iyileşmezse eğitimi durdurur, en iyi ağırlıkları geri yükler
- **ReduceLROnPlateau** — Plato tespit edildiğinde öğrenme oranını 0.2 çarpanıyla düşürür

---

## 💡 İpuçları

- **GPU olmadan** çalıştırıyorsan `steps_per_epoch` ve `epochs` değerlerini düşür
- Veri seti büyük olduğu için `batch_size=32` GPU için optimize edilmiştir; CPU'da `batch_size=8`'e düşürülmesi önerilir
- Sınıf benzerliği (örneğin farklı elma türleri) yanlış tahminlere yol açabilir — bu normaldir

---

## 📄 Lisans

Bu proje **MIT Lisansı** altında dağıtılmaktadır.  
Orijinal içerik: © IBM Corporation – Skills Network

---

*⭐ Projeyi beğendiysen yıldız vermeyi unutma!*
