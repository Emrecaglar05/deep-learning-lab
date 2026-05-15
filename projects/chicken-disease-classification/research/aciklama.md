# 📁 research/ Klasörü - Jupyter Notebook Denemeleri

## 📌 Bu Klasör Ne İşe Yarar?

`research/` klasörü, **deneysel çalışmaların** yapıldığı yerdir. Burada Jupyter Notebook dosyaları bulunur. Bu dosyalarda:
- Kod parçaları adım adım test edilir
- Sonuçlar görsel olarak incelenir
- Hata ayıklama yapılır
- Başarılı kodlar `src/` klasörüne taşınır

**Analoji:** Bir aşçının mutfağında yeni tarif denemesi gibi. Burada deneyler yapılır, başarılı olanlar ana menüye (src/) eklenir.

---

## 📂 İçindeki Dosyalar

```
research/
├── 01_data_ingestion.ipynb                # Veri indirme denemeleri
├── 02_prepare_base_model.ipynb            # Model hazırlama denemeleri
├── 03_model_training.ipynb                # Eğitim denemeleri
├── 04_model_evaluation_with_mlflow.ipynb  # Değerlendirme denemeleri
├── trials.ipynb                           # Çeşitli denemeler
└── logs/                                  # Notebook logları (varsa)
```

---

## 🔍 Her Notebook Ne Yapar?

### **1. 01_data_ingestion.ipynb**

#### **Amaç:**
Veri indirme ve hazırlama sürecini test eder.

#### **İçerik:**
```python
# Cell 1: Kütüphaneleri içe aktar
import os
from dataclasses import dataclass
from pathlib import Path

# Cell 2: Çalışma dizinini değiştir
os.chdir("../")

# Cell 3: Veri yapısını tanımla
@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path

# Cell 4: ConfigurationManager sınıfı
class ConfigurationManager:
    ...

# Cell 5: DataIngestion sınıfı
class DataIngestion:
    def download_file(self): ...
    def extract_zip_file(self): ...

# Cell 6: Pipeline'ı çalıştır
config = ConfigurationManager()
data_ingestion = DataIngestion(config=config.get_data_ingestion_config())
data_ingestion.download_file()
data_ingestion.extract_zip_file()
```

#### **Ne Öğrenilir?**
- Google Drive'dan dosya indirme (`gdown` kütüphanesi)
- Zip dosyası açma
- Klasör yapısı oluşturma
- Logger kullanımı

#### **Çıktı:**
```
artifacts/data_ingestion/
├── data.zip
└── Chicken-fecal-images/
    ├── Healthy/
    └── Coccidiosis/
```

---

### **2. 02_prepare_base_model.ipynb**

#### **Amaç:**
VGG16 modelini yükleyip tavuk hastalık tespitine özelleştirmeyi test eder.

#### **İçerik:**
```python
# Cell 1: Kütüphaneleri içe aktar
import tensorflow as tf
from tensorflow import keras

# Cell 2: PrepareBaseModelConfig tanımla
@dataclass(frozen=True)
class PrepareBaseModelConfig:
    root_dir: Path
    base_model_path: Path
    updated_base_model_path: Path
    params_image_size: list
    params_learning_rate: float
    params_classes: int

# Cell 3: PrepareBaseModel sınıfı
class PrepareBaseModel:
    def get_base_model(self):
        # VGG16'yı yükle
        self.model = keras.applications.vgg16.VGG16(...)
    
    def update_base_model(self):
        # Son katmanı özelleştir
        layers.Dense(2, activation="softmax")

# Cell 4: Pipeline'ı çalıştır
```

#### **Ne Öğrenilir?**
- Transfer Learning kavramı
- VGG16 modeli kullanımı
- Model katmanlarını özelleştirme
- Model kaydetme (.h5 formatı)

#### **Çıktı:**
```
artifacts/prepare_base_model/
├── base_model.h5           # Orijinal VGG16
└── base_model_updated.h5   # Özelleştirilmiş
```

---

### **3. 03_model_training.ipynb**

#### **Amaç:**
Hazırlanan modeli tavuk görüntüleri ile eğitmeyi test eder.

#### **İçerik:**
```python
# Cell 1: TrainingConfig tanımla
@dataclass(frozen=True)
class TrainingConfig:
    root_dir: Path
    trained_model_path: Path
    base_model_path: Path
    training_data: Path
    params_epochs: int
    params_batch_size: int

# Cell 2: Callbacks hazırla
# TensorBoard, ModelCheckpoint

# Cell 3: Training sınıfı
class Training:
    def get_base_model(self): ...
    def train_valid_generator(self): ...
    def train(self): ...

# Cell 4: Pipeline'ı çalıştır
training.train()
```

#### **Ne Öğrenilir?**
- ImageDataGenerator (veri artırma)
- Callbacks (TensorBoard, ModelCheckpoint)
- fit() metodu
- Eğitim sırasında model kaydetme

#### **Çıktı:**
```
artifacts/training/
└── model.h5    # Eğitilmiş model

artifacts/prepare_callbacks/
├── tensorboard_log_dir/    # TensorBoard logları
└── checkpoint_dir/         # Checkpoint'ler
```

#### **TensorBoard Kullanımı:**
```bash
tensorboard --logdir=artifacts/prepare_callbacks/tensorboard_log_dir
# http://localhost:6006 adresinde grafikler görülür
```

---

### **4. 04_model_evaluation_with_mlflow.ipynb**

#### **Amaç:**
Eğitilmiş modelin performansını ölçer ve MLflow'a kaydeder.

#### **İçerik:**
```python
# Cell 1: MLflow'u içe aktar
import mlflow
import mlflow.keras

# Cell 2: EvaluationConfig tanımla
@dataclass(frozen=True)
class EvaluationConfig:
    model_path: Path
    test_data_path: Path
    mlflow_uri: str

# Cell 3: Evaluation sınıfı
class Evaluation:
    def evaluation(self):
        # Model test edilir
        loss, accuracy = self.model.evaluate(self.test_generator)
    
    def log_into_mlflow(self):
        # MLflow'a kaydet
        mlflow.log_params(self.config.all_params)
        mlflow.log_metrics({"loss": loss, "accuracy": accuracy})
        mlflow.keras.log_model(self.model, "model")

# Cell 4: Pipeline'ı çalıştır
```

#### **Ne Öğrenilir?**
- Model değerlendirme (`evaluate()` metodu)
- MLflow kullanımı
- Parametre ve metrik kaydetme
- Model versiyonlama

#### **Çıktı:**
```
artifacts/evaluation/
└── scores.json    # {"loss": 0.15, "accuracy": 0.95}

# MLflow'a kaydedilen bilgiler:
- Parametreler (EPOCHS, BATCH_SIZE, vb.)
- Metrikler (loss, accuracy)
- Model dosyası
```

#### **MLflow UI Başlatma:**
```bash
mlflow ui
# http://localhost:5000 adresinde arayüz açılır
```

---

### **5. trials.ipynb**

#### **Amaç:**
Hızlı denemeler ve test kodları için kullanılır.

**Örnek içerikler:**
- Görüntü okuma ve gösterme
- Preprocessing denemeleri
- Küçük kod parçaları test etme
- Kütüphane fonksiyonlarını deneme

---

## 🎓 Jupyter Notebook Nasıl Kullanılır?

### **Notebook'u Açma:**
```bash
# Chicken ortamını aktive et
conda activate chicken

# Jupyter Lab'ı başlat
jupyter lab

# Veya Jupyter Notebook
jupyter notebook
```

### **VS Code'da Açma:**
1. `.ipynb` dosyasına tıkla
2. VS Code otomatik olarak notebook görünümünde açar
3. Kernel olarak "chicken" ortamını seç

### **Hücreleri Çalıştırma:**
- **Shift + Enter**: Hücreyi çalıştır ve bir sonrakine geç
- **Ctrl + Enter**: Hücreyi çalıştır ve aynı hücrede kal
- **Alt + Enter**: Hücreyi çalıştır ve altına yeni hücre ekle

---

## 🔄 Research → src Workflow

### **Adımlar:**
1. **research/** klasöründe notebook'ta kod yaz ve test et
2. Kod başarılı çalıştı mı? ✅
3. Kodu temizle ve düzenle
4. **src/components/** klasörüne Python dosyası olarak taşı
5. **src/pipeline/** ile entegre et
6. **main.py** ile tüm pipeline'ı çalıştır

**Örnek:**
```
01_data_ingestion.ipynb (deneme)
    ↓ (başarılı)
src/components/data_ingestion.py (final kod)
    ↓
src/pipeline/stage_01_data_ingestion.py
    ↓
main.py
```

---

## 🛠️ Notebook'lardaki Önemli Hücreler

### **Çalışma Dizinini Değiştirme:**
```python
import os
os.chdir("../")  # Proje kök dizinine git
```

**Neden?**
- Notebook'lar `research/` klasöründe
- Ancak config dosyaları kök dizinde
- Bu nedenle bir üst dizine çıkmalıyız

### **Logger Kullanımı:**
```python
from cnnClassifier import logger

logger.info("İşlem başarılı!")
logger.error("Hata oluştu!")
```

### **ConfigBox Kullanımı:**
```python
from box import ConfigBox

config = ConfigBox({"name": "test", "value": 123})
print(config.name)  # "test" (dict gibi ama nokta ile erişim)
```

---

## 🐛 Sık Karşılaşılan Hatalar

### **1. Import Hatası**
```python
ModuleNotFoundError: No module named 'cnnClassifier'
```

**Çözüm:**
```python
import sys
sys.path.append("../src")  # src klasörünü path'e ekle

# veya
os.chdir("../")  # Kök dizine git
```

### **2. Dosya Bulunamadı**
```python
FileNotFoundError: config/config.yaml
```

**Çözüm:**
```python
%pwd  # Mevcut dizini kontrol et
os.chdir("../")  # Gerekirse kök dizine git
```

### **3. YAML Parse Hatası**
```python
yaml.scanner.ScannerError: mapping values are not allowed here
```

**Çözüm:**
- YAML dosyasında girinti (indentation) hatası var
- Boşlukları kontrol et (tab değil space kullan)

---

## 📊 Notebook Çıktılarını Anlama

### **Logger Çıktısı:**
```
[2026-01-13 10:30:45: INFO: data_ingestion: Downloading data...]
[2026-01-13 10:31:20: INFO: data_ingestion: Downloaded successfully]
```

### **Eğitim Çıktısı:**
```
Epoch 1/10
50/50 [==============================] - 45s 900ms/step 
loss: 0.6543 - accuracy: 0.7234 - val_loss: 0.5432 - val_accuracy: 0.8123
```

**Anlamı:**
- **loss**: Eğitim hatası (düşmeli)
- **accuracy**: Eğitim doğruluğu (artmalı)
- **val_loss**: Doğrulama hatası
- **val_accuracy**: Doğrulama doğruluğu

---

## 🎯 Özet

| Notebook | Görev | Çıktı |
|----------|-------|-------|
| `01_data_ingestion.ipynb` | Veri indirme | `artifacts/data_ingestion/` |
| `02_prepare_base_model.ipynb` | Model hazırlama | `artifacts/prepare_base_model/` |
| `03_model_training.ipynb` | Model eğitimi | `artifacts/training/model.h5` |
| `04_model_evaluation_with_mlflow.ipynb` | Değerlendirme | `artifacts/evaluation/scores.json` |
| `trials.ipynb` | Hızlı denemeler | - |

---

**Önemli:** Notebook'lar **deneme amaçlıdır**. Production (canlı) ortamda `main.py` ve `src/` klasörü kullanılır. Notebook'lar, kod geliştirme ve öğrenme sürecinde kullanılır.
