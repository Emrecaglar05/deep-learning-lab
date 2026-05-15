# 📁 src/ Klasörü - Kaynak Kod (Source Code)

## 📌 Bu Klasör Ne İşe Yarar?

`src/` klasörü, projenin **tüm çalışan kodlarını** içerir. Burada projenin beyni olan Python modülleri bulunur. "Source" kelimesi "kaynak" anlamına gelir ve yazılım dünyasında kaynak kodların saklandığı klasöre verilen isimdir.

---

## 📂 İçindeki Alt Klasörler ve Dosyalar

```
src/
└── cnnClassifier/                    # Ana Python paketi
    ├── __init__.py                   # Logger (kayıt sistemi) ve paket başlatıcı
    │
    ├── 📁 components/                # Temel bileşenler (her biri bir görevi yapar)
    │   ├── __init__.py
    │   ├── data_ingestion.py         # Veriyi indirir ve hazırlar
    │   ├── prepare_base_model.py     # VGG16 modelini yükler ve özelleştirir
    │   ├── model_training.py         # Modeli eğitir
    │   └── model_evaluation_mlflow.py # Modeli test eder ve sonuçları kaydeder
    │
    ├── 📁 config/                    # Konfigürasyon yönetimi
    │   ├── __init__.py
    │   └── configuration.py          # YAML dosyalarını okuyup ayarları yükler
    │
    ├── 📁 constants/                 # Sabit değerler
    │   └── __init__.py               # config.yaml ve params.yaml dosya yolları
    │
    ├── 📁 entity/                    # Veri yapıları (Data Classes)
    │   ├── __init__.py
    │   └── config_entity.py          # Ayar nesnelerini tanımlar
    │
    ├── 📁 pipeline/                  # Pipeline (iş akışı) dosyaları
    │   ├── __init__.py
    │   ├── stage_01_data_ingestion.py       # Adım 1: Veri toplama
    │   ├── stage_02_prepare_base_model.py   # Adım 2: Model hazırlama
    │   ├── stage_03_model_training.py       # Adım 3: Eğitim
    │   ├── stage_04_model_evaluation.py     # Adım 4: Değerlendirme
    │   └── prediction.py                    # Yeni görüntüler için tahmin
    │
    └── 📁 utils/                     # Yardımcı fonksiyonlar
        ├── __init__.py
        └── common.py                 # YAML okuma, klasör oluşturma, JSON kaydetme vb.
```

---

## 🔍 Detaylı Açıklamalar

### **1. cnnClassifier/__init__.py**
**Ne yapar?** Projenin tüm işlemlerini kayıt altına alan **logger** (kaydedici) sistemini kurar.

**İçeriği:**
```python
import logging

logger = logging.getLogger("cnnClassifierLogger")
```

**Neden önemli?**
- Her işlem (veri indirme, model eğitimi) loglanır
- Hata ayıklama (debugging) kolaylaşır
- `logs/` klasöründe `running_logs.log` dosyasına kaydedilir

**Örnek log çıktısı:**
```
[2026-01-13 10:30:45: INFO: data_ingestion: Downloading data from URL...]
```

---

### **2. components/ Klasörü**

#### **a) data_ingestion.py**
**Görevi:** İnternetten veri indirir ve hazırlar.

**Sınıf:** `DataIngestion`

**Metodlar:**
- `download_file()`: Google Drive'dan veriyi indirir
- `extract_zip_file()`: Zip dosyasını açar

**Kullandığı kütüphane:** `gdown` (Google Drive indirici)

**Çıktı:**
```
artifacts/data_ingestion/
├── data.zip
└── Chicken-fecal-images/
    ├── Healthy/          # Sağlıklı tavuk görüntüleri
    └── Coccidiosis/      # Hasta tavuk görüntüleri
```

---

#### **b) prepare_base_model.py**
**Görevi:** VGG16 modelini yükler ve tavuk hastalık tespitine özelleştirir.

**Sınıf:** `PrepareBaseModel`

**Metodlar:**
- `get_base_model()`: VGG16'yı yükler (ImageNet ağırlıklarıyla)
- `update_base_model()`: Modelin son katmanını değiştirir

**Transfer Learning Nedir?**
- VGG16: 1.4 milyon görüntü ile eğitilmiş hazır model
- Biz sadece son katmanı tavuk hastalığı için eğitiyoruz
- Bu sayede çok daha az veri ile iyi sonuçlar alıyoruz

**Çıktı:**
```
artifacts/prepare_base_model/
├── base_model.h5           # Orijinal VGG16
└── base_model_updated.h5   # Özelleştirilmiş model
```

---

#### **c) model_training.py**
**Görevi:** Modeli tavuk görüntüleri ile eğitir.

**Sınıf:** `Training`

**Önemli Kavramlar:**
- **Epoch**: Tüm veri setinin modele kaç kez gösterileceği
- **Batch Size**: Aynı anda kaç görüntü işlenecek
- **Callback**: Eğitim sırasında yapılan özel işlemler

**Callbacks:**
1. **TensorBoard**: Eğitim grafiklerini gösterir
2. **ModelCheckpoint**: En iyi modeli kaydeder

**Çıktı:**
```
artifacts/training/
└── model.h5    # Eğitilmiş model (tahmin için kullanılır)
```

---

#### **d) model_evaluation_mlflow.py**
**Görevi:** Modelin performansını ölçer ve MLflow'a kaydeder.

**Sınıf:** `Evaluation`

**Metrikler:**
- **Loss**: Hata oranı (düşük olmalı)
- **Accuracy**: Doğruluk oranı (yüksek olmalı)

**MLflow Nedir?**
- Model versiyonlarını takip eder
- Hangi parametrelerle ne kadar doğruluk elde edildiğini saklar
- Farklı denemeleri karşılaştırma imkanı

**Çıktı:**
```
artifacts/evaluation/
└── scores.json    # {"loss": 0.15, "accuracy": 0.95}
```

---

### **3. config/ Klasörü**

#### **configuration.py**
**Görevi:** `config.yaml` ve `params.yaml` dosyalarını okuyup Python nesnelerine dönüştürür.

**Sınıf:** `ConfigurationManager`

**Metodlar:**
```python
get_data_ingestion_config()       # Veri indirme ayarları
get_prepare_base_model_config()   # Model hazırlama ayarları
get_training_config()             # Eğitim ayarları
get_evaluation_config()           # Değerlendirme ayarları
```

**Neden önemli?**
- Kod içinde sabit değer (hard-code) yazmak yerine YAML'den okuruz
- Ayarları değiştirmek için kod değiştirmemiz gerekmez
- Daha modüler ve yönetilebilir kod

---

### **4. constants/ Klasörü**

#### **__init__.py**
**Görevi:** Proje genelinde kullanılan sabit dosya yollarını tanımlar.

```python
from pathlib import Path

CONFIG_FILE_PATH = Path("config/config.yaml")
PARAMS_FILE_PATH = Path("params.yaml")
```

**Kullanım:**
```python
from cnnClassifier.constants import CONFIG_FILE_PATH
config = read_yaml(CONFIG_FILE_PATH)
```

---

### **5. entity/ Klasörü**

#### **config_entity.py**
**Görevi:** Ayar nesnelerini tanımlar (Data Classes).

**Sınıflar:**
```python
@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path
```

**Neden kullanılır?**
- Ayarları düzenli bir yapıda tutar
- Hatalı veri girişini önler (type checking)
- `frozen=True` ile değiştirilemez (immutable) yapar

---

### **6. pipeline/ Klasörü**

#### **Pipeline Dosyaları**
Her dosya, bir aşamayı çalıştırır:

**a) stage_01_data_ingestion.py**
```python
class DataIngestionTrainingPipeline:
    def main(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.download_file()
        data_ingestion.extract_zip_file()
```

**b) stage_02_prepare_base_model.py**
- Model hazırlama pipeline'ını çalıştırır

**c) stage_03_model_training.py**
- Eğitim pipeline'ını çalıştırır

**d) stage_04_model_evaluation.py**
- Değerlendirme pipeline'ını çalıştırır

**e) prediction.py**
- Yeni görüntüler için tahmin yapar

---

### **7. utils/ Klasörü**

#### **common.py**
**Görevi:** Proje boyunca kullanılan yardımcı fonksiyonlar.

**Fonksiyonlar:**

1. **read_yaml(path)**: YAML dosyasını okur
```python
config = read_yaml("config/config.yaml")
```

2. **create_directories(paths)**: Klasör oluşturur
```python
create_directories(["artifacts/data_ingestion"])
```

3. **save_json(path, data)**: JSON dosyası kaydeder
```python
save_json("scores.json", {"accuracy": 0.95})
```

4. **load_json(path)**: JSON dosyası okur

5. **save_bin(data, path)**: Binary dosya kaydeder

6. **load_bin(path)**: Binary dosya okur

7. **get_size(path)**: Dosya boyutunu hesaplar

---

## 🔗 Dosyalar Nasıl Birbiriyle İlişkili?

```
main.py
  ↓
pipeline/stage_01_data_ingestion.py
  ↓
config/configuration.py → constants/ → config.yaml
  ↓
components/data_ingestion.py
  ↓
utils/common.py (yardımcı fonksiyonlar)
  ↓
artifacts/data_ingestion/ (çıktı)
```

---

## 🎯 Özet

| Klasör | Görev |
|--------|-------|
| `components/` | Temel işlevler (indirme, eğitim, değerlendirme) |
| `config/` | Ayarları yönetir |
| `constants/` | Sabit değerler |
| `entity/` | Veri yapıları |
| `pipeline/` | İş akışlarını organize eder |
| `utils/` | Yardımcı fonksiyonlar |

---

**Önemli:** Bu klasördeki kodlar, `main.py` tarafından çağrılır ve sırayla çalıştırılır. Proje modüler yapıda olduğu için her bileşen bağımsız test edilebilir.
