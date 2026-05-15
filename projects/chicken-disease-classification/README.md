<div align="center">

# 🐔 Chicken Disease Classification 🐔

**Tavuk dışkı görüntülerinden hastalıkları (özellikle Koksidiyoz) tespit eden uçtan uca bir Derin Öğrenme projesi.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?style=for-the-badge&logo=tensorflow)](https://www.tensorflow.org/)
[![DVC](https://img.shields.io/badge/DVC-Data_Versioning-purple?style=for-the-badge&logo=dvc)](https://dvc.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

---

### 📖 Projeye Genel Bakış

Bu proje, tavukların dışkı görüntülerinden sağlık durumlarını analiz etmek için bir Evrişimli Sinir Ağı (CNN) modeli kullanır. Özellikle, kanatlı endüstrisinde ciddi ekonomik kayıplara neden olan **Koksidiyoz** hastalığının erken teşhisine odaklanmaktadır. Proje, veri toplama, model eğitimi, değerlendirme ve tahmin adımlarını içeren tam bir MLOps (Makine Öğrenmesi Operasyonları) boru hattı olarak tasarlanmıştır.

---

### 🎯 Çözülen Problem

Kanatlı hayvan yetiştiriciliğinde hastalıkların hızlı bir şekilde yayılması, ciddi verim kayıplarına ve ekonomik zararlara yol açar. Koksidiyoz gibi paraziter hastalıkların erken teşhisi, salgınları önlemek ve hayvan refahını sağlamak için kritik öneme sahiptir. Bu proje, hastalık teşhis sürecini otomatikleştirmeyi ve veteriner hekimlere karar destek sistemi sunmayı amaçlamaktadır.

---

### ✨ Temel Özellikler

- **Uçtan Uca Pipeline:** Veri indirmeden model değerlendirmesine kadar tüm süreç otomatize edilmiştir.
- **Modüler Tasarım:** Her bir aşama (veri, temel model, eğitim) bağımsız bileşenler olarak geliştirilmiştir.
- **Yapılandırma Odaklı:** Tüm parametreler ve yollar, kod değişikliği gerektirmeden `YAML` dosyaları üzerinden yönetilir.
- **Veri ve Model Versiyonlama:** `DVC` (Data Version Control) entegrasyonu ile veri setleri ve model çıktıları versiyonlanır, bu da deneylerin tekrarlanabilirliğini sağlar.
- **Görselleştirilmiş Performans:** Eğitim süreci `TensorBoard` ile izlenebilir.

---

### 🚀 Proje Mimarisi ve Çalışma Akışı

Proje, birbirini takip eden dört ana aşamadan oluşur. Her aşama, bir önceki aşamanın çıktısını girdi olarak kullanır.

```mermaid
graph TD;
    A[Başlangıç: main.py] --> B{1. Veri Toplama};
    B --> C{2. Temel Model Hazırlama};
    C --> D{3. Model Eğitimi};
    D --> E{4. Model Değerlendirme};
    E --> F[Sonuç: a. Eğitilmiş Model (.h5) <br> b. Değerlendirme Skorları (scores.json)];

    subgraph "Aşama 1: Veri Toplama"
        B_1[URL'den veriyi indir] --> B_2[Zip'ten çıkar] --> B_3[Veriyi 'artifacts' klasörüne kaydet];
    end

    subgraph "Aşama 2: Temel Model Hazırlama"
        C_1[VGG16 modelini yükle] --> C_2[Modelin son katmanını güncelle] --> C_3[Hazır modeli 'artifacts'e kaydet];
    end

    subgraph "Aşama 3: Model Eğitimi"
        D_1[Hazır modeli ve veriyi yükle] --> D_2[Modeli eğit (Callbacks ile)] --> D_3[Eğitilmiş modeli (.h5) kaydet];
    end

    subgraph "Aşama 4: Model Değerlendirme"
        E_1[Eğitilmiş modeli yükle] --> E_2[Test verisi ile performansı ölç] --> E_3[Doğruluk ve Kayıp skorlarını .json olarak kaydet];
    end
```

---

### 🛠️ Kurulum ve Başlangıç

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin.

#### 1. Ön Gereksinimler
- Python 3.8 veya üstü
- `conda` veya `venv` gibi bir sanal ortam yöneticisi

#### 2. Projeyi Klonlayın
```bash
git clone https://github.com/KULLANICI_ADINIZ/Chicken-Disease-Classification.git
cd Chicken-Disease-Classification
```

#### 3. Sanal Ortam Oluşturun ve Aktive Edin
```bash
# conda kullanarak
conda create -n cnncls python=3.8 -y
conda activate cnncls

# venv kullanarak
python -m venv venv
source venv/bin/activate  # Linux/Mac için
# venv\Scripts\activate  # Windows için
```

#### 4. Gerekli Kütüphaneleri Yükleyin
```bash
pip install -r requirements.txt
```

---

### ⚡ Kullanım

#### Pipeline'ı Çalıştırma
Tüm adımları (veri toplama, eğitim, değerlendirme) baştan sona çalıştırmak için:
```bash
python main.py
```
Bu komut, `main.py` içindeki tüm aşamaları sırasıyla tetikleyecektir.

#### DVC ile Aşamaları Çalıştırma (Önerilen)
`DVC`, sadece değişen kısımları çalıştırarak zaman kazandırır.
```bash
# Tüm aşamaları dvc repro komutuyla çalıştırmak için (dvc.yaml yapılandırıldıktan sonra)
dvc repro
```
Bu komut, `dvc.yaml` dosyasındaki bağımlılıkları kontrol eder ve yalnızca güncel olmayan aşamaları yeniden çalıştırır.

---

### 💻 Kullanılan Teknolojiler

- **Python:** Ana programlama dili
- **TensorFlow & Keras:** Derin öğrenme modeli oluşturma ve eğitme
- **DVC:** Veri ve model versiyonlama
- **MLflow:** Deney takibi ve model yönetimi (entegrasyona hazır)
- **Matplotlib:** Veri görselleştirme
- **Scikit-learn:** Model değerlendirme metrikleri
- **YAML:** Yapılandırma yönetimi
- **Flask:** (İsteğe bağlı) Modelin web arayüzü ile sunulması için

---

### 🤝 Katkıda Bulunma

Katkılarınız projeyi daha da ileriye taşıyacaktır! Lütfen bir `issue` açın veya bir `pull request` gönderin.

1. Projeyi Fork'layın.
2. Yeni bir `feature` branch'i oluşturun (`git checkout -b feature/yeni-ozellik`).
3. Değişikliklerinizi commit'leyin (`git commit -m 'Yeni bir özellik eklendi'`).
4. Branch'inizi push'layın (`git push origin feature/yeni-ozellik`).
5. Bir Pull Request açın.

---

### 📄 Lisans

Bu proje **MIT Lisansı** altındadır. Detaylar için `LICENSE` dosyasına bakınız.

---
<div align="center">
    Geliştiren: [Adınız] - [GitHub Profil Linkiniz]
</div>
