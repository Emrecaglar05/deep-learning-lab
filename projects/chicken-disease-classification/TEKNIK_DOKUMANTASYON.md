# 🐔 Tavuk Hastalığı Sınıflandırma Projesi - Teknik Dokümantasyon

## 📋 İçindekiler
1. [Proje Özeti](#-proje-özeti)
2. [Mimari Yapı](#-mimari-yapı)
3. [Veri Akışı ve Haberleşme](#-veri-akışı-ve-haberleşme)
4. [Modüller Arası İlişkiler](#-modüller-arası-ilişkiler)
5. [Pipeline Aşamaları](#-pipeline-aşamaları)
6. [Konfigürasyon Yönetimi](#-konfigürasyon-yönetimi)
7. [Model Mimarisi](#-model-mimarisi)
8. [Kullanılan Teknolojiler](#-kullanılan-teknolojiler)
9. [Önemli Teknik Detaylar](#-önemli-teknik-detaylar)

---

## 🎯 Proje Özeti

Bu proje, **tavuk dışkı görüntülerinden hastalık tespiti** yapan uçtan uca (end-to-end) bir derin öğrenme pipeline'ıdır. Transfer Learning kullanarak VGG16 modeli ile **Coccidiosis (hastalıklı)** ve **Healthy (sağlıklı)** sınıflandırması yapar.

### Temel Özellikler:
- ✅ Modüler ve ölçeklenebilir mimari
- ✅ Konfigürasyon tabanlı parametre yönetimi
- ✅ MLflow ile deney takibi
- ✅ Transfer Learning (VGG16)
- ✅ Data Augmentation desteği
- ✅ Logging sistemi

---

## 🏗 Mimari Yapı

```
Chicken-Disease-Classification/
│
├── main.py                          # Ana çalıştırma dosyası (orchestrator)
├── params.yaml                      # Hiperparametreler
├── config/
│   └── config.yaml                  # Sistem konfigürasyonları
│
├── src/cnnClassifier/
│   ├── __init__.py                  # Logger tanımı
│   ├── constants/                   # Sabit dosya yolları
│   ├── entity/                      # Veri yapıları (dataclass)
│   ├── config/                      # Konfigürasyon yönetimi
│   ├── components/                  # İş mantığı (business logic)
│   ├── pipeline/                    # Pipeline aşamaları
│   └── utils/                       # Yardımcı fonksiyonlar
│
├── artifacts/                       # Üretilen dosyalar (model, veri)
├── logs/                            # Log dosyaları
└── templates/                       # Web arayüzü şablonları
```

### Katmanlı Mimari:

```
┌─────────────────────────────────────────────────────────────┐
│                        main.py                               │
│                    (Orchestrator Layer)                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Pipeline Layer                            │
│  stage_01_data_ingestion.py  │  stage_02_prepare_base_model │
│  stage_03_model_training.py  │  stage_04_model_evaluation   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Components Layer                           │
│    data_ingestion.py    │    prepare_base_model.py          │
│    model_training.py    │    model_evaluation_mlflow.py     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                Configuration Layer                           │
│         configuration.py  ←→  config_entity.py              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Utils & Constants                          │
│              common.py  │  constants/__init__.py            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Veri Akışı ve Haberleşme

### Genel Akış Diyagramı:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   config/    │     │   params.    │     │  constants/  │     │    utils/    │
│ config.yaml  │     │    yaml      │     │ __init__.py  │     │  common.py   │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │                    │
       └────────────────────┼────────────────────┘                    │
                            │                                         │
                            ▼                                         │
              ┌─────────────────────────┐                             │
              │   ConfigurationManager  │◄────────────────────────────┘
              │    (configuration.py)   │     read_yaml(), create_directories()
              └───────────┬─────────────┘
                          │
          ┌───────────────┼───────────────┬───────────────┐
          │               │               │               │
          ▼               ▼               ▼               ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
    │DataInges │   │PrepBase  │   │Training  │   │Evaluation│
    │tionConfig│   │ModelConf │   │Config    │   │Config    │
    └────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘
         │              │              │              │
         ▼              ▼              ▼              ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
    │  Data    │   │ Prepare  │   │ Training │   │Evaluation│
    │Ingestion │   │BaseModel │   │          │   │          │
    └────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘
         │              │              │              │
         ▼              ▼              ▼              ▼
┌────────────────────────────────────────────────────────────────┐
│                        artifacts/                               │
│  data_ingestion/  │  prepare_base_model/  │  training/         │
│  └── images/      │  ├── base_model.h5    │  └── model.h5      │
│                   │  └── base_model_      │                     │
│                   │      updated.h5       │                     │
└────────────────────────────────────────────────────────────────┘
```

### Modüller Nasıl Haberleşiyor?

#### 1. **YAML → ConfigurationManager → Config Entity → Component**

```python
# 1. constants/__init__.py - Dosya yollarını tanımlar
CONFIG_FILE_PATH = Path("config/config.yaml")
PARAMS_FILE_PATH = Path("params.yaml")

# 2. ConfigurationManager - YAML dosyalarını okur
class ConfigurationManager:
    def __init__(self):
        self.config = read_yaml(CONFIG_FILE_PATH)   # config.yaml'ı oku
        self.params = read_yaml(PARAMS_FILE_PATH)   # params.yaml'ı oku

# 3. Config Entity - Tip güvenli veri yapısı oluşturur
@dataclass(frozen=True)
class TrainingConfig:
    root_dir: Path
    trained_model_path: Path
    params_epochs: int
    params_learning_rate: float
    # ... diğer parametreler

# 4. Component - İş mantığını çalıştırır
class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config  # Konfigürasyonu al ve kullan
```

#### 2. **Pipeline → Component İlişkisi**

```python
# Pipeline katmanı (stage_03_model_training.py)
class ModelTrainingPipeline:
    def main(self):
        # 1. Konfigürasyon yöneticisini başlat
        config = ConfigurationManager()
        
        # 2. Training konfigürasyonunu al
        training_config = config.get_training_config()
        
        # 3. Training component'ini konfigürasyonla başlat
        training = Training(config=training_config)
        
        # 4. İşlemleri sırayla çalıştır
        training.get_base_model()
        training.train_valid_generator()
        training.train()
```

---

## 🔗 Modüller Arası İlişkiler

### Detaylı İlişki Haritası:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              main.py                                     │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  from cnnClassifier.pipeline.stage_01_data_ingestion import ... │    │
│  │  from cnnClassifier.pipeline.stage_02_prepare_base_model import │    │
│  │  from cnnClassifier.pipeline.stage_03_model_training import ... │    │
│  │  from cnnClassifier.pipeline.stage_04_model_evaluation import . │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ imports
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        pipeline/ katmanı                                 │
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ stage_01_data_ingestion.py                                        │  │
│  │   └── from cnnClassifier.config.configuration import ...          │  │
│  │   └── from cnnClassifier.components.data_ingestion import ...     │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ stage_02_prepare_base_model.py                                    │  │
│  │   └── from cnnClassifier.config.configuration import ...          │  │
│  │   └── from cnnClassifier.components.prepare_base_model import ... │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│  ... (diğer stage'ler benzer yapıda)                                    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ imports
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        components/ katmanı                               │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │ model_training.py                                                  │ │
│  │   import tensorflow as tf                                          │ │
│  │   from cnnClassifier.entity.config_entity import TrainingConfig    │ │
│  │                                                                    │ │
│  │   class Training:                                                  │ │
│  │       def __init__(self, config: TrainingConfig):                  │ │
│  │           self.config = config  # Dependency Injection             │ │
│  └────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ imports
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         entity/ katmanı                                  │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │ config_entity.py                                                   │ │
│  │                                                                    │ │
│  │   @dataclass(frozen=True)     # Immutable veri yapısı              │ │
│  │   class TrainingConfig:                                            │ │
│  │       root_dir: Path          # Tip güvenliği sağlar               │ │
│  │       trained_model_path: Path                                     │ │
│  │       params_epochs: int                                           │ │
│  │       params_learning_rate: float                                  │ │
│  └────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Pipeline Aşamaları

### Stage 1: Data Ingestion (Veri İndirme)

```
┌─────────────────────────────────────────────────────────────────┐
│                     DATA INGESTION                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Girdi:                                                          │
│    • source_URL (GitHub/Google Drive)                           │
│                                                                  │
│  İşlem:                                                          │
│    1. URL'den ZIP dosyasını indir                               │
│    2. ZIP'i artifacts/data_ingestion/ altına çıkart             │
│                                                                  │
│  Çıktı:                                                          │
│    • artifacts/data_ingestion/Chicken-fecal-images/             │
│        ├── Coccidiosis/  (hastalıklı görüntüler)                │
│        └── Healthy/      (sağlıklı görüntüler)                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Kod Akışı:**
```python
# data_ingestion.py
class DataIngestion:
    def download_file(self):
        # 1. URL kontrolü (Google Drive mi, GitHub mı?)
        if "drive.google.com" in dataset_url:
            gdown.download(...)        # Google Drive için gdown
        else:
            requests.get(dataset_url)  # GitHub için requests

    def extract_zip_file(self):
        # 2. ZIP'i çıkart
        with zipfile.ZipFile(self.config.local_data_file) as zip_ref:
            zip_ref.extractall(unzip_path)
```

---

### Stage 2: Prepare Base Model (Temel Model Hazırlama)

```
┌─────────────────────────────────────────────────────────────────┐
│                   PREPARE BASE MODEL                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Girdi:                                                          │
│    • ImageNet ağırlıkları (otomatik indirilir)                  │
│                                                                  │
│  İşlem:                                                          │
│    1. VGG16 modelini yükle (top katmanlar hariç)                │
│    2. Flatten + Dense katmanları ekle                           │
│    3. Modeli compile et (SGD optimizer)                         │
│    4. Tüm katmanları dondur (freeze_all=True)                   │
│                                                                  │
│  Çıktı:                                                          │
│    • artifacts/prepare_base_model/base_model.h5                 │
│    • artifacts/prepare_base_model/base_model_updated.h5         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Transfer Learning Mantığı:**
```python
# prepare_base_model.py
@staticmethod
def _prepare_full_model(model, classes, freeze_all, freeze_till, learning_rate):
    # 1. Katmanları dondur (transfer learning)
    if freeze_all:
        for layer in model.layers:
            model.trainable = False  # Ağırlıkları güncelleme
    
    # 2. Yeni katmanlar ekle
    flatten_in = tf.keras.layers.Flatten()(model.output)
    prediction = tf.keras.layers.Dense(
        units=classes,      # 2 sınıf: Coccidiosis, Healthy
        activation="softmax"
    )(flatten_in)
    
    # 3. Modeli compile et
    full_model.compile(
        optimizer=tf.keras.optimizers.SGD(learning_rate=learning_rate),
        loss=tf.keras.losses.CategoricalCrossentropy(),
        metrics=["accuracy"]
    )
```

**VGG16 Mimarisi:**
```
Input (224x224x3)
       │
       ▼
┌─────────────────┐
│  VGG16 Bloğu    │  ← ImageNet ağırlıkları (dondurulmuş)
│  (14,714,688    │
│   parametre)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Flatten      │  (7x7x512 = 25,088 nöron)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Dense(2)       │  ← Eğitilebilir (50,178 parametre)
│  Softmax        │
└────────┬────────┘
         │
         ▼
   [Coccidiosis, Healthy]
```

---

### Stage 3: Model Training (Model Eğitimi)

```
┌─────────────────────────────────────────────────────────────────┐
│                      MODEL TRAINING                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Girdi:                                                          │
│    • base_model_updated.h5                                      │
│    • Chicken-fecal-images/ (görüntüler)                         │
│                                                                  │
│  İşlem:                                                          │
│    1. Modeli yükle ve YENİDEN COMPILE ET                        │
│    2. ImageDataGenerator ile veri artırma                       │
│    3. %80 train, %20 validation split                           │
│    4. Model eğitimi (model.fit)                                 │
│                                                                  │
│  Çıktı:                                                          │
│    • artifacts/training/model.h5                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Data Augmentation (Veri Artırma):**
```python
# model_training.py
if self.config.params_is_augmentation:
    train_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
        rotation_range=40,       # ±40 derece döndürme
        horizontal_flip=True,    # Yatay çevirme
        width_shift_range=0.2,   # %20 yatay kaydırma
        height_shift_range=0.2,  # %20 dikey kaydırma
        shear_range=0.2,         # Kesme dönüşümü
        zoom_range=0.2,          # %20 yakınlaştırma
        rescale=1./255           # Piksel normalizasyonu [0,1]
    )
```

**⚠️ Kritik Fix - Optimizer Sorunu:**
```python
# model_training.py - get_base_model metodu
def get_base_model(self):
    # Model yükle (compile=False ile!)
    self.model = tf.keras.models.load_model(
        self.config.updated_base_model_path,
        compile=False  # ÖNEMLİ: Eski optimizer'ı yükleme!
    )
    
    # Yeni optimizer oluştur ve compile et
    optimizer = tf.keras.optimizers.SGD(learning_rate=self.config.params_learning_rate)
    self.model.compile(
        optimizer=optimizer,
        loss=tf.keras.losses.CategoricalCrossentropy(),
        metrics=["accuracy"]
    )
```

> **Neden?** Keras 3.x'te kaydedilmiş optimizer'ın dahili değişken referansları geçersiz hale geliyor. Yeni optimizer oluşturmak bu sorunu çözüyor.

---

### Stage 4: Model Evaluation (Model Değerlendirme)

```
┌─────────────────────────────────────────────────────────────────┐
│                     MODEL EVALUATION                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Girdi:                                                          │
│    • artifacts/training/model.h5                                │
│    • Test verileri (%30 validation split)                       │
│                                                                  │
│  İşlem:                                                          │
│    1. Eğitilmiş modeli yükle                                    │
│    2. Test verileri üzerinde değerlendir                        │
│    3. Loss ve Accuracy hesapla                                  │
│    4. MLflow'a logla (opsiyonel)                                │
│                                                                  │
│  Çıktı:                                                          │
│    • scores.json (loss, accuracy)                               │
│    • MLflow metrics                                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Konfigürasyon Yönetimi

### İki Tip Konfigürasyon Dosyası:

#### 1. `config/config.yaml` - Sistem Konfigürasyonu
```yaml
# Dosya yolları ve sistem ayarları
artifacts_root: artifacts

data_ingestion:
  root_dir: artifacts/data_ingestion
  source_URL: https://github.com/.../Chicken-fecal-images.zip
  local_data_file: artifacts/data_ingestion/data.zip
  unzip_dir: artifacts/data_ingestion

prepare_base_model:
  root_dir: artifacts/prepare_base_model
  base_model_path: artifacts/prepare_base_model/base_model.h5
  updated_base_model_path: artifacts/prepare_base_model/base_model_updated.h5

training:
  root_dir: artifacts/training
  trained_model_path: artifacts/training/model.h5
```

#### 2. `params.yaml` - Hiperparametreler
```yaml
# Model ve eğitim parametreleri
AUGMENTATION: True          # Veri artırma kullanılsın mı?
IMAGE_SIZE: [224, 224, 3]   # Girdi boyutu (VGG16 standardı)
BATCH_SIZE: 16              # Mini-batch boyutu
INCLUDE_TOP: False          # VGG16 sınıflandırma katmanları çıkarılsın mı?
EPOCHS: 1                   # Eğitim döngüsü sayısı
CLASSES: 2                  # Sınıf sayısı
WEIGHTS: imagenet           # Önceden eğitilmiş ağırlıklar
LEARNING_RATE: 0.01         # Öğrenme hızı
```

### ConfigBox Kullanımı:
```python
# utils/common.py
from box import ConfigBox

def read_yaml(path_to_yaml: Path) -> ConfigBox:
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
        return ConfigBox(content)  # Dict'i nesne gibi kullan

# Kullanım:
config = read_yaml("params.yaml")
print(config.EPOCHS)         # 1 (dict['EPOCHS'] yerine)
print(config.LEARNING_RATE)  # 0.01
```

---

## 🧠 Model Mimarisi

### VGG16 + Custom Head

```
┌─────────────────────────────────────────────────────────────────────┐
│                        MODEL MİMARİSİ                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    INPUT LAYER                                 │  │
│  │                  (224 x 224 x 3)                               │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                              │                                       │
│                              ▼                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │               VGG16 BACKBONE (Dondurulmuş)                     │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │ Block 1: Conv(64) → Conv(64) → MaxPool                  │  │  │
│  │  │ Block 2: Conv(128) → Conv(128) → MaxPool                │  │  │
│  │  │ Block 3: Conv(256) → Conv(256) → Conv(256) → MaxPool    │  │  │
│  │  │ Block 4: Conv(512) → Conv(512) → Conv(512) → MaxPool    │  │  │
│  │  │ Block 5: Conv(512) → Conv(512) → Conv(512) → MaxPool    │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  │                   14,714,688 parametre (frozen)                │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                              │                                       │
│                              ▼                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    CUSTOM HEAD (Eğitilebilir)                  │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │ Flatten: 7 x 7 x 512 = 25,088 nöron                     │  │  │
│  │  │ Dense: 25,088 → 2 (Softmax)                             │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  │                   50,178 parametre (trainable)                 │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                              │                                       │
│                              ▼                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                       OUTPUT                                   │  │
│  │              [Coccidiosis, Healthy] probabilities              │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  TOPLAM: 14,764,866 parametre                                       │
│  Eğitilebilir: 50,178 parametre (%0.34)                             │
│  Dondurulmuş: 14,714,688 parametre (%99.66)                         │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Transfer Learning Avantajı:
- Sadece **50,178** parametre eğitiliyor (toplam 14.7M yerine)
- ImageNet'ten öğrenilmiş özellikler (kenarlar, dokular, şekiller) kullanılıyor
- Küçük veri setiyle bile yüksek doğruluk elde ediliyor

---

## 🛠 Kullanılan Teknolojiler

| Kategori | Teknoloji | Açıklama |
|----------|-----------|----------|
| **Deep Learning** | TensorFlow/Keras | Model oluşturma ve eğitim |
| **Base Model** | VGG16 | ImageNet ön eğitimli CNN |
| **Data Handling** | ImageDataGenerator | Veri artırma ve yükleme |
| **Config Management** | PyYAML, python-box | YAML dosya işleme |
| **Experiment Tracking** | MLflow | Deney takibi ve model registry |
| **Logging** | Python logging | Loglama sistemi |
| **Type Safety** | dataclasses | Tip güvenli konfigürasyon |
| **Package Management** | setuptools | Python paketi oluşturma |

---

## 📝 Önemli Teknik Detaylar

### 1. Dependency Injection Pattern
```python
# Component'ler konfigürasyonu constructor'dan alır
class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config  # Bağımlılık enjeksiyonu
```

### 2. Immutable Config (frozen=True)
```python
@dataclass(frozen=True)  # Değiştirilemez
class TrainingConfig:
    params_epochs: int
    # config.params_epochs = 10  # HATA! Değiştirilemez
```

### 3. Type Annotations
```python
@ensure_annotations  # Tip kontrolü zorla
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    # path_to_yaml string olursa HATA verir
```

### 4. Logger Singleton
```python
# src/cnnClassifier/__init__.py
logger = logging.getLogger("cnnClassifierLogger")

# Her yerden aynı logger'ı kullan
from cnnClassifier import logger
logger.info("Mesaj")
```

### 5. Keras 3.x Optimizer Fix
```python
# YANLIŞ (eski yöntem):
self.model = tf.keras.models.load_model(path)  # Optimizer uyumsuzluğu!

# DOĞRU:
self.model = tf.keras.models.load_model(path, compile=False)
self.model.compile(optimizer=tf.keras.optimizers.SGD(...), ...)
```

---

## 📊 Sonuçlar

| Metrik | Değer |
|--------|-------|
| **Validation Accuracy** | %90.62 |
| **Test Accuracy** | %93.10 |
| **Loss** | 0.33 |
| **Eğitim Süresi** | ~22 saniye (1 epoch) |

---

## 🚀 Çalıştırma

```bash
# 1. Bağımlılıkları yükle
pip install -r requirements.txt

# 2. Pipeline'ı çalıştır
python main.py

# 3. Logları kontrol et
cat logs/running_logs.log
```

---

## 📁 Artifacts Yapısı (Çıktılar)

```
artifacts/
├── data_ingestion/
│   ├── data.zip                        # İndirilen ZIP
│   └── Chicken-fecal-images/
│       ├── Coccidiosis/                # 195 hastalıklı görüntü
│       └── Healthy/                    # 195 sağlıklı görüntü
│
├── prepare_base_model/
│   ├── base_model.h5                   # VGG16 (top hariç)
│   └── base_model_updated.h5           # VGG16 + Custom Head
│
└── training/
    └── model.h5                        # Eğitilmiş final model
```

---

**Proje Sahibi:** [Emre Çağlar]  
**Tarih:** Ocak 2026  
**Versiyon:** 1.0.0
