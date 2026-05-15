# 🐔 Tavuk Hastalık Sınıflandırma Projesi - Genel Açıklama

## 📋 Proje Nedir?

Bu proje, tavukların dışkı görüntülerinden **Koksidiyoz** hastalığını tespit eden yapay zeka tabanlı bir sistemdir. Derin öğrenme (Deep Learning) kullanarak görüntüleri analiz eder ve tavuğun sağlıklı mı yoksa hasta mı olduğunu belirler.

---

## 🎯 Neden Bu Proje Yapıldı?

Tavuk çiftliklerinde hastalıklar çok hızlı yayılır ve büyük ekonomik kayıplara yol açar. Bu proje:
- Hastalığı erken tespit ederek yayılmasını önler
- Veteriner hekimlere karar verme sürecinde yardımcı olur
- Manuel kontrol yerine otomatik tespit yaparak zaman kazandırır

---

## 🏗️ Proje Yapısı (Hangi Dosya Ne İşe Yarar?)

```
📁 Chicken-Disease-Classification/
│
├── 📄 README.md                    # Projenin genel açıklaması ve kullanım kılavuzu
├── 📄 main.py                      # Projeyi çalıştıran ana dosya
├── 📄 setup.py                     # Projeyi Python paketi olarak kurma dosyası
├── 📄 requirements.txt             # Gerekli Python kütüphanelerinin listesi
├── 📄 params.yaml                  # Model eğitim parametreleri (epoch, batch size vb.)
├── 📄 dvc.yaml                     # Veri versiyon kontrolü için DVC pipeline tanımları
├── 📄 template.py                  # Proje klasör yapısını otomatik oluşturan script
│
├── 📁 config/                      # Konfigürasyon dosyaları
│   └── config.yaml                 # Veri yolları ve model ayarları
│
├── 📁 src/                         # Kaynak kod (Source Code)
│   └── cnnClassifier/              # Ana paket
│       ├── __init__.py             # Logger (işlem kayıt sistemi) tanımı
│       ├── components/             # Temel bileşenler
│       │   ├── data_ingestion.py          # Veriyi indirip hazırlama
│       │   ├── prepare_base_model.py      # VGG16 modelini hazırlama
│       │   ├── model_training.py          # Modeli eğitme
│       │   └── model_evaluation_mlflow.py # Modeli değerlendirme
│       ├── config/
│       │   └── configuration.py           # Ayarları yükleyen sınıf
│       ├── constants/
│       │   └── __init__.py                # Sabit değerler (config/params dosya yolları)
│       ├── entity/
│       │   └── config_entity.py           # Veri yapılarını tanımlayan sınıflar
│       ├── pipeline/               # Pipeline (İş akışı) dosyaları
│       │   ├── stage_01_data_ingestion.py        # Adım 1: Veri indirme
│       │   ├── stage_02_prepare_base_model.py    # Adım 2: Model hazırlama
│       │   ├── stage_03_model_training.py        # Adım 3: Model eğitimi
│       │   ├── stage_04_model_evaluation.py      # Adım 4: Model değerlendirme
│       │   └── prediction.py                     # Tahmin yapma
│       └── utils/
│           └── common.py                  # Yardımcı fonksiyonlar (YAML okuma vb.)
│
├── 📁 research/                    # Jupyter Notebook deneysel çalışmaları
│   ├── 01_data_ingestion.ipynb           # Veri indirme denemeleri
│   ├── 02_prepare_base_model.ipynb       # Model hazırlama denemeleri
│   ├── 03_model_training.ipynb           # Eğitim denemeleri
│   └── 04_model_evaluation_with_mlflow.ipynb  # Değerlendirme denemeleri
│
├── 📁 artifacts/                   # Eğitim sırasında oluşan çıktılar
│   ├── data_ingestion/             # İndirilen ve çıkarılan veri
│   ├── prepare_base_model/         # Hazırlanan model dosyaları
│   ├── training/                   # Eğitilmiş model (.h5 dosyası)
│   └── evaluation/                 # Model performans sonuçları
│
├── 📁 templates/                   # Web arayüzü HTML dosyaları
│   └── index.html                  # Ana sayfa
│
└── 📁 logs/                        # İşlem kayıtları (log dosyaları)
```

---

## 🚀 Proje Nasıl Çalışır? (4 Adım)

### **Adım 1: Veri Toplama (Data Ingestion)**
- İnternet'ten tavuk dışkı görüntülerini indirir
- Zip dosyasını açar ve `artifacts/data_ingestion/` klasörüne kaydeder
- Görüntüler 2 kategoriye ayrılır: **Healthy** (Sağlıklı) ve **Coccidiosis** (Koksidiyoz)

### **Adım 2: Model Hazırlama (Prepare Base Model)**
- Hazır bir yapay zeka modeli olan **VGG16** kullanılır
- Bu model daha önce 1.4 milyon görüntü ile eğitilmiştir (ImageNet)
- Modelin son katmanı tavuk hastalığı tespitine özelleştirilir

### **Adım 3: Model Eğitimi (Training)**
- Hazırlanan model, tavuk görüntüleri ile eğitilir
- Model, sağlıklı ve hasta görüntüleri ayırt etmeyi öğrenir
- Eğitim sırasında ağırlıklar kaydedilir (`model.h5`)

### **Adım 4: Model Değerlendirme (Evaluation)**
- Eğitilmiş modelin doğruluğu test edilir
- Performans metrikleri (accuracy, loss) kaydedilir
- MLflow ile sonuçlar izlenir ve saklanır

---

## 🔧 Nasıl Kullanılır?

### **1. Ortamı Hazırlama**
```bash
# Chicken sanal ortamını aktive et
conda activate chicken

# Gerekli paketleri yükle (zaten yüklendi)
pip install -r requirements.txt
```

### **2. Projeyi Çalıştırma**
```bash
# Tüm pipeline'ı çalıştır
python main.py
```

### **3. Notebook'larla Deneme Yapma**
- `research/` klasöründeki Jupyter Notebook dosyalarını açarak adım adım deneyebilirsiniz

---

## 📦 Önemli Dosya Açıklamaları

### **config.yaml**
Veri yollarını ve model ayarlarını içerir:
```yaml
artifacts_root: artifacts              # Tüm çıktılar buraya kaydedilir

data_ingestion:
  source_URL: ...                      # Veri indirme linki
  local_data_file: ...                 # İndirilen zip dosyası yolu
```

### **params.yaml**
Model eğitim parametreleri:
```yaml
IMAGE_SIZE: [224, 224, 3]    # Görüntü boyutu
BATCH_SIZE: 16                # Aynı anda işlenecek görüntü sayısı
EPOCHS: 1                     # Eğitim döngü sayısı
LEARNING_RATE: 0.01           # Öğrenme hızı
```

### **main.py**
Tüm pipeline'ı sırayla çalıştırır:
```python
1. Veriyi indir
2. Modeli hazırla
3. Modeli eğit
4. Modeli değerlendir
```

---

## 🛠️ Teknolojiler

- **TensorFlow/Keras**: Derin öğrenme modeli
- **VGG16**: Önceden eğitilmiş CNN modeli
- **DVC**: Veri versiyon kontrolü
- **MLflow**: Model takip ve versiyon yönetimi
- **Flask**: Web arayüzü (tahmin için)
- **Python 3.10**: Ana programlama dili

---

## 📊 Model Performansı

Model, eğitim sonunda şu metrikleri sağlar:
- **Accuracy**: Doğruluk oranı (% kaç tahminin doğru olduğu)
- **Loss**: Hata oranı (düşük olması iyidir)

---

## 🎓 Proje Hakkında Bilmeniz Gerekenler

### **Transfer Learning Nedir?**
VGG16 gibi önceden eğitilmiş bir modeli kullanarak, kendi probleminize uyarlamak. Bu sayede:
- Daha az veri ile iyi sonuçlar alınır
- Eğitim süresi kısalır

### **Pipeline Nedir?**
Veri toplama, model eğitimi gibi adımların sırayla otomatik çalıştırılması.

### **Artifacts Nedir?**
Projenin çalışması sonucu oluşan dosyalar (modeller, veriler, loglar).

---

## 🔍 Sorun Giderme

**Paket eksik hatası:**
```bash
conda activate chicken
pip install -r requirements.txt
```

**Import hatası:**
```bash
# Notebook'ta çalışma dizinini değiştir
os.chdir("../")
```

---

## 📝 Lisans
MIT License - Açık kaynak, özgürce kullanılabilir.

---

**Hazırlayan:** Chicken Disease Classification Project Team  
**Güncelleme:** 13 Ocak 2026
