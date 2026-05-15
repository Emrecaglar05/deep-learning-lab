# 📁 config/ Klasörü - Konfigürasyon Dosyaları

## 📌 Bu Klasör Ne İşe Yarar?

`config/` klasörü, projenin **ayar dosyalarını** içerir. Burada kod içinde sabit değer (hard-code) yazmak yerine, tüm ayarları YAML formatında saklarız.

**Analoji:** Bir telefonun ayarlar menüsü gibi. Her şeyi kod içinde yazmak yerine, ayarları değiştirmek için sadece bu dosyayı düzenleriz.

---

## 📂 İçindeki Dosyalar

```
config/
└── config.yaml    # Tüm proje ayarları (veri yolları, model ayarları)
```

---

## 🔍 config.yaml Detaylı Açıklama

### **Tam İçerik:**

```yaml
artifacts_root: artifacts    # Tüm çıktılar bu klasöre kaydedilir


data_ingestion:
  root_dir: artifacts/data_ingestion                     # Veri indirme klasörü
  source_URL: https://github.com/entbappy/Branching-tutorial/raw/master/Chicken-fecal-images.zip
  local_data_file: artifacts/data_ingestion/data.zip     # İndirilen zip dosyası
  unzip_dir: artifacts/data_ingestion                    # Zip açılacak yer


prepare_base_model:
  root_dir: artifacts/prepare_base_model                 # Model hazırlama klasörü
  base_model_path: artifacts/prepare_base_model/base_model.h5           # Orijinal VGG16
  updated_base_model_path: artifacts/prepare_base_model/base_model_updated.h5  # Özelleştirilmiş


prepare_callbacks:
  root_dir: artifacts/prepare_callbacks                  # Callback klasörü
  tensorboard_root_log_dir: artifacts/prepare_callbacks/tensorboard_log_dir  # TensorBoard logları
  checkpoint_model_filepath: artifacts/prepare_callbacks/checkpoint_dir/model.h5  # En iyi model


training:
  root_dir: artifacts/training                           # Eğitim klasörü
  trained_model_path: artifacts/training/model.h5        # Final eğitilmiş model


evaluation:
  root_dir: artifacts/evaluation                         # Değerlendirme klasörü
  model_path: artifacts/training/model.h5                # Değerlendirilecek model
  all_params: params.yaml                                # Parametre dosyası yolu
  mlflow_uri: https://dagshub.com/entbappy/Chicken-Disease-Classification.mlflow  # MLflow sunucusu
  params_image_size: [224, 224, 3]                       # Test görüntü boyutu
  params_batch_size: 16                                  # Test batch size
```

---

## 📖 Her Bölüm Ne Anlama Gelir?

### **1. artifacts_root**

```yaml
artifacts_root: artifacts
```

**Açıklama:**
- Projenin tüm çıktıları (modeller, veriler, loglar) bu klasöre kaydedilir
- Bu klasör `.gitignore` ile Git'ten çıkarılmıştır (çünkü çok büyük dosyalar içerir)

**Oluşan Yapı:**
```
artifacts/
├── data_ingestion/
├── prepare_base_model/
├── prepare_callbacks/
├── training/
└── evaluation/
```

---

### **2. data_ingestion**

```yaml
data_ingestion:
  root_dir: artifacts/data_ingestion
  source_URL: https://github.com/entbappy/Branching-tutorial/raw/master/Chicken-fecal-images.zip
  local_data_file: artifacts/data_ingestion/data.zip
  unzip_dir: artifacts/data_ingestion
```

**Açıklama:**

| Parametre | Ne İşe Yarar? |
|-----------|---------------|
| `root_dir` | Veri indirme işlemlerinin yapılacağı ana klasör |
| `source_URL` | Veri setinin indirileceği internet adresi (GitHub veya Google Drive) |
| `local_data_file` | İndirilen ZIP dosyasının kaydedileceği yer |
| `unzip_dir` | ZIP dosyasının açılacağı klasör |

**İşlem Akışı:**
```
1. source_URL'den indir
   ↓
2. local_data_file'a kaydet (data.zip)
   ↓
3. unzip_dir'e açar
   ↓
4. Chicken-fecal-images/
   ├── Healthy/
   └── Coccidiosis/
```

**URL Değiştirme:**
Eğer farklı bir veri seti kullanmak isterseniz:
```yaml
source_URL: https://drive.google.com/file/d/YOUR_FILE_ID/view
```

---

### **3. prepare_base_model**

```yaml
prepare_base_model:
  root_dir: artifacts/prepare_base_model
  base_model_path: artifacts/prepare_base_model/base_model.h5
  updated_base_model_path: artifacts/prepare_base_model/base_model_updated.h5
```

**Açıklama:**

| Parametre | Ne İşe Yarar? |
|-----------|---------------|
| `root_dir` | Model hazırlama işlemlerinin klasörü |
| `base_model_path` | İndirilen orijinal VGG16 modelinin kaydedileceği yer |
| `updated_base_model_path` | Özelleştirilmiş modelin kaydedileceği yer |

**Model Hazırlama Süreci:**
```
1. VGG16'yı ImageNet ağırlıklarıyla indir
   ↓
2. base_model.h5 olarak kaydet (1000 sınıf)
   ↓
3. Son katmanı 2 sınıfa (Healthy/Coccidiosis) dönüştür
   ↓
4. base_model_updated.h5 olarak kaydet
```

**Dosya Boyutları:**
- `base_model.h5`: ~528 MB (orijinal VGG16)
- `base_model_updated.h5`: ~528 MB (özelleştirilmiş)

---

### **4. prepare_callbacks**

```yaml
prepare_callbacks:
  root_dir: artifacts/prepare_callbacks
  tensorboard_root_log_dir: artifacts/prepare_callbacks/tensorboard_log_dir
  checkpoint_model_filepath: artifacts/prepare_callbacks/checkpoint_dir/model.h5
```

**Açıklama:**

| Parametre | Ne İşe Yarar? |
|-----------|---------------|
| `root_dir` | Callback dosyalarının ana klasörü |
| `tensorboard_root_log_dir` | TensorBoard eğitim grafiklerinin kaydedileceği yer |
| `checkpoint_model_filepath` | Eğitim sırasında en iyi modelin kaydedileceği yer |

**Callbacks Nedir?**
Eğitim sırasında otomatik çalışan özel fonksiyonlar:

1. **TensorBoard Callback:**
   - Her epoch'ta loss ve accuracy değerlerini kaydeder
   - Grafikler `tensorboard_root_log_dir` klasöründe saklanır
   - Komut: `tensorboard --logdir=artifacts/prepare_callbacks/tensorboard_log_dir`

2. **ModelCheckpoint Callback:**
   - Eğitim sırasında en iyi modeli kaydeder
   - Örneğin 5. epoch'ta accuracy 0.95 oldu → model kaydedilir
   - 8. epoch'ta 0.97 oldu → yeni model üzerine yazılır

---

### **5. training**

```yaml
training:
  root_dir: artifacts/training
  trained_model_path: artifacts/training/model.h5
```

**Açıklama:**

| Parametre | Ne İşe Yarar? |
|-----------|---------------|
| `root_dir` | Eğitim çıktılarının klasörü |
| `trained_model_path` | Final eğitilmiş modelin kaydedileceği yer |

**Eğitim Süreci:**
```
1. base_model_updated.h5'i yükle
   ↓
2. Tavuk görüntüleri ile eğit
   ↓
3. trained_model_path'e kaydet (model.h5)
```

**Kullanım:**
Bu `model.h5` dosyası:
- Web uygulamasında tahmin için kullanılır
- Değerlendirme için test edilir
- Dağıtım (deployment) için hazırdır

---

### **6. evaluation**

```yaml
evaluation:
  root_dir: artifacts/evaluation
  model_path: artifacts/training/model.h5
  all_params: params.yaml
  mlflow_uri: https://dagshub.com/entbappy/Chicken-Disease-Classification.mlflow
  params_image_size: [224, 224, 3]
  params_batch_size: 16
```

**Açıklama:**

| Parametre | Ne İşe Yarar? |
|-----------|---------------|
| `root_dir` | Değerlendirme çıktılarının klasörü |
| `model_path` | Test edilecek modelin yolu |
| `all_params` | Tüm parametrelerin bulunduğu dosya (MLflow için) |
| `mlflow_uri` | MLflow sunucu adresi (deney takibi için) |
| `params_image_size` | Test görüntülerinin boyutu |
| `params_batch_size` | Test batch size |

**MLflow Nedir?**
- Model deneyleri takip eden bir araç
- Farklı parametrelerle yapılan eğitimleri karşılaştırır
- Her deneyde hangi parametrelerle ne kadar doğruluk elde edildiğini saklar

**DagHub:**
- MLflow'u ücretsiz barındıran platform
- `mlflow_uri` adresinde deney sonuçlarını görebilirsiniz

---

## 🛠️ YAML Formatı Nedir?

YAML (Yet Another Markup Language), ayar dosyaları için kullanılan basit bir formattır.

### **Temel Kurallar:**

1. **Key-Value Çiftleri:**
```yaml
key: value
name: "Tavuk Projesi"
```

2. **İç İçe Yapılar (Indentation):**
```yaml
parent:
  child: value
  another_child: value
```

3. **Listeler:**
```yaml
items:
  - item1
  - item2
  - item3
```

4. **Yorumlar:**
```yaml
# Bu bir yorumdur
key: value  # Satır sonu yorumu
```

### **Önemli Notlar:**
- **Tab kullanmayın!** Sadece **boşluk** (space) kullanın
- Girinti (indentation) çok önemlidir
- String'leri tırnak içine almak isteğe bağlı

---

## 🔧 config.yaml'ı Nasıl Kullanırız?

### **Python'da Okuma:**

```python
from cnnClassifier.utils.common import read_yaml
from cnnClassifier.constants import CONFIG_FILE_PATH

# YAML dosyasını oku
config = read_yaml(CONFIG_FILE_PATH)

# Değerlere erişim
print(config.artifacts_root)           # "artifacts"
print(config.data_ingestion.root_dir)  # "artifacts/data_ingestion"
print(config.training.trained_model_path)  # "artifacts/training/model.h5"
```

### **ConfigBox Kullanımı:**

```python
from box import ConfigBox

# Normal dict
config_dict = {"name": "test", "value": 123}
print(config_dict["name"])  # "test"

# ConfigBox (dict gibi ama nokta ile erişim)
config_box = ConfigBox(config_dict)
print(config_box.name)  # "test" (daha temiz!)
```

---

## 🎯 Neden config.yaml Kullanıyoruz?

### **1. Hard-code Yerine Konfigürasyon**

**Kötü Yöntem (Hard-code):**
```python
def download_data():
    url = "https://example.com/data.zip"  # Değiştirmek için kodu düzenlemeli
    path = "artifacts/data.zip"           # Her yerde aynı path
```

**İyi Yöntem (Konfigürasyon):**
```python
def download_data(config):
    url = config.source_URL     # YAML'den okur
    path = config.local_data_file  # YAML'den okur
```

### **2. Merkezi Yönetim**

Tüm yollar tek bir dosyada:
- Değişiklik yapmak kolay
- Hata riski az
- Kod daha temiz

### **3. Farklı Ortamlar**

```yaml
# Development (geliştirme)
artifacts_root: artifacts

# Production (canlı)
artifacts_root: /var/www/artifacts
```

---

## 🐛 Sık Karşılaşılan Hatalar

### **1. Girinti (Indentation) Hatası**

**Yanlış:**
```yaml
data_ingestion:
root_dir: artifacts/data_ingestion  # Hatalı girinti!
```

**Doğru:**
```yaml
data_ingestion:
  root_dir: artifacts/data_ingestion  # 2 boşluk girinti
```

### **2. Tab Kullanımı**

**Yanlış:**
```yaml
data_ingestion:
→ root_dir: artifacts  # Tab karakteri (görünmez)
```

**Doğru:**
```yaml
data_ingestion:
  root_dir: artifacts  # 2 boşluk
```

### **3. Özel Karakter Hatası**

**Yanlış:**
```yaml
name: Tavuk: Hastalık  # İki nokta üst üste sorun yaratır
```

**Doğru:**
```yaml
name: "Tavuk: Hastalık"  # Tırnak içine al
```

---

## 📝 config.yaml Değiştirme Örnekleri

### **Örnek 1: Farklı Veri Seti Kullanma**

```yaml
data_ingestion:
  source_URL: https://drive.google.com/file/d/YOUR_NEW_FILE_ID/view
```

### **Örnek 2: Farklı Model Yolu**

```yaml
training:
  trained_model_path: artifacts/models/final_model.h5
```

### **Örnek 3: Yerel Veri Kullanma**

```yaml
data_ingestion:
  source_URL: file:///C:/Users/MyUser/data/images.zip
```

---

## 🎯 Özet

| Özellik | Açıklama |
|---------|----------|
| **Dosya Adı** | `config.yaml` |
| **Amaç** | Proje ayarlarını saklamak |
| **Format** | YAML (Key-Value çiftleri) |
| **Kullanım** | `read_yaml()` ile okunur |
| **Avantaj** | Kod değiştirmeden ayar değiştirme |

---

**Önemli:** `config.yaml` dosyasını düzenlerken girinti (indentation) kurallarına dikkat edin. YAML formatı boşluklara çok duyarlıdır!
