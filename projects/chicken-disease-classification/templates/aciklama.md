# 📁 templates/ Klasörü - Web Arayüzü Dosyaları

## 📌 Bu Klasör Ne İşe Yarar?

`templates/` klasörü, **Flask web uygulaması** için HTML sayfalarını içerir. Burası, kullanıcıların tarayıcıdan modeli kullanabilmeleri için gerekli arayüz dosyalarının bulunduğu yerdir.

**Analoji:** Bir mağazanın vitrin ve iç tasarımı gibi. Arka planda model çalışır (src/), ama kullanıcılar bu arayüzü görür.

---

## 📂 İçindeki Dosyalar

```
templates/
└── index.html    # Ana sayfa (görüntü yükleme ve tahmin sonucu)
```

---

## 🌐 Flask Nedir?

Flask, Python ile web uygulaması geliştirmek için kullanılan hafif bir framework'tür.

**Çalışma Mantığı:**
```
Kullanıcı Tarayıcısı (index.html)
        ↓
    Flask Server (app.py)
        ↓
Model (artifacts/training/model.h5)
        ↓
    Tahmin Sonucu
        ↓
Kullanıcıya Gösterilir (index.html)
```

---

## 🔍 index.html Detaylı İnceleme

### **Sayfa Yapısı**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Tavuk Hastalık Tespiti</title>
    <style>
        /* CSS stilleri */
    </style>
</head>
<body>
    <h1>🐔 Tavuk Hastalık Sınıflandırma</h1>
    
    <!-- Görüntü Yükleme Formu -->
    <form action="/predict" method="post" enctype="multipart/form-data">
        <input type="file" name="image" accept="image/*" required>
        <button type="submit">Tahmin Et</button>
    </form>
    
    <!-- Sonuç Gösterimi -->
    {% if prediction %}
        <div class="result">
            <h2>Tahmin Sonucu:</h2>
            <p>{{ prediction }}</p>
            <p>Güven Skoru: {{ confidence }}%</p>
        </div>
    {% endif %}
</body>
</html>
```

---

## 🎨 HTML Bileşenleri

### **1. Başlık (Header)**

```html
<head>
    <title>Tavuk Hastalık Tespiti</title>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
    </style>
</head>
```

**Açıklama:**
- Sayfa başlığı tarayıcı sekmesinde görünür
- CSS ile sayfa tasarımı yapılır
- Responsive tasarım için meta tag eklenebilir

---

### **2. Form (Görüntü Yükleme)**

```html
<form action="/predict" method="post" enctype="multipart/form-data">
    <label for="image">Tavuk Dışkısı Görüntüsü Seçin:</label>
    <input type="file" 
           id="image" 
           name="image" 
           accept="image/*" 
           required>
    <button type="submit">🔍 Tahmin Et</button>
</form>
```

**Parametreler:**

| Parametre | Açıklama |
|-----------|----------|
| `action="/predict"` | Form gönderildiğinde `/predict` endpoint'ine gider |
| `method="post"` | POST isteği gönderir (dosya yükleme için gerekli) |
| `enctype="multipart/form-data"` | Dosya yüklemeye izin verir |
| `accept="image/*"` | Sadece görüntü dosyaları seçilebilir |
| `required` | Boş gönderilmesini engeller |

---

### **3. Jinja2 Şablonu (Sonuç Gösterimi)**

```html
{% if prediction %}
    <div class="result {{ 'healthy' if prediction == 'Healthy' else 'sick' }}">
        <h2>📊 Tahmin Sonucu</h2>
        
        <div class="prediction-box">
            <p class="label">Durum:</p>
            <p class="value">{{ prediction }}</p>
        </div>
        
        <div class="confidence-box">
            <p class="label">Güven Oranı:</p>
            <p class="value">{{ confidence }}%</p>
        </div>
        
        {% if prediction == "Healthy" %}
            <p class="message">✅ Tavuk sağlıklı görünüyor!</p>
        {% else %}
            <p class="message">⚠️ Koksidiyoz tespit edildi. Veterinere danışın!</p>
        {% endif %}
    </div>
{% endif %}
```

**Jinja2 Syntax:**

| Syntax | Açıklama | Örnek |
|--------|----------|-------|
| `{{ variable }}` | Değişkeni yazdır | `{{ prediction }}` → "Healthy" |
| `{% if condition %}` | Koşul kontrolü | `{% if prediction == "Healthy" %}` |
| `{% for item in list %}` | Döngü | `{% for result in results %}` |
| `{% endif %}` | Koşul bitişi | `{% endif %}` |

---

## 🔗 Flask Backend ile Entegrasyon

### **app.py (Backend)**

```python
from flask import Flask, render_template, request
from tensorflow import keras
import numpy as np
from PIL import Image

app = Flask(__name__)

# Modeli yükle
model = keras.models.load_model("artifacts/training/model.h5")
class_names = ["Healthy", "Coccidiosis"]

@app.route("/")
def index():
    """Ana sayfayı göster"""
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    """Tahmin yap ve sonucu göster"""
    # Görüntüyü al
    image_file = request.files["image"]
    
    # Görüntüyü işle
    img = Image.open(image_file).resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    # Tahmin yap
    predictions = model.predict(img_array)
    predicted_class = class_names[np.argmax(predictions)]
    confidence = np.max(predictions) * 100
    
    # Sonucu HTML'e gönder
    return render_template(
        "index.html",
        prediction=predicted_class,
        confidence=f"{confidence:.2f}"
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
```

---

## 🎨 CSS Styling Önerileri

### **Modern Tasarım**

```css
/* Genel Stil */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* Container */
.container {
    background: white;
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    max-width: 500px;
    width: 90%;
}

/* Başlık */
h1 {
    text-align: center;
    color: #333;
    margin-bottom: 30px;
    font-size: 2em;
}

/* Form */
form {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

input[type="file"] {
    padding: 10px;
    border: 2px dashed #667eea;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.3s;
}

input[type="file"]:hover {
    border-color: #764ba2;
    background: #f8f9fa;
}

/* Buton */
button {
    padding: 15px 30px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 1.1em;
    cursor: pointer;
    transition: transform 0.2s;
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

/* Sonuç Kutusu */
.result {
    margin-top: 30px;
    padding: 20px;
    border-radius: 10px;
    animation: slideIn 0.5s ease;
}

.result.healthy {
    background: #d4edda;
    border: 2px solid #28a745;
}

.result.sick {
    background: #f8d7da;
    border: 2px solid #dc3545;
}

/* Animasyon */
@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Responsive Tasarım */
@media (max-width: 600px) {
    .container {
        padding: 20px;
    }
    
    h1 {
        font-size: 1.5em;
    }
}
```

---

## 📱 Responsive Tasarım

### **Mobil Uyumluluk**

```html
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
```

**Ekran Boyutlarına Göre:**

| Cihaz | Genişlik | Tasarım |
|-------|----------|---------|
| Telefon | < 600px | Tek sütun, büyük butonlar |
| Tablet | 600-900px | Orta boyut |
| Masaüstü | > 900px | Geniş layout |

---

## 🔧 İleri Düzey Özellikler

### **1. Görüntü Önizleme**

```javascript
<script>
function previewImage(event) {
    const file = event.target.files[0];
    const reader = new FileReader();
    
    reader.onload = function(e) {
        const preview = document.getElementById('preview');
        preview.src = e.target.result;
        preview.style.display = 'block';
    };
    
    reader.readAsDataURL(file);
}
</script>

<input type="file" onchange="previewImage(event)">
<img id="preview" style="display:none; max-width:300px; margin-top:20px;">
```

### **2. Loading Spinner**

```html
<style>
.spinner {
    border: 4px solid #f3f3f3;
    border-top: 4px solid #667eea;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    display: none;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>

<div class="spinner" id="spinner"></div>

<script>
document.querySelector('form').onsubmit = function() {
    document.getElementById('spinner').style.display = 'block';
};
</script>
```

### **3. Hata Mesajları**

```html
{% if error %}
    <div class="error-message">
        ⚠️ {{ error }}
    </div>
{% endif %}
```

---

## 🚀 Flask Uygulamasını Çalıştırma

### **1. Backend Oluşturma (app.py)**

```python
# app.py dosyası oluştur (proje kök dizininde)
# Yukarıdaki Flask kodu kullanılabilir
```

### **2. Çalıştırma**

```bash
# Chicken ortamını aktive et
conda activate chicken

# Flask'ı çalıştır
python app.py
```

### **3. Tarayıcıda Açma**

```
http://localhost:5000
veya
http://127.0.0.1:5000
```

---

## 🐛 Sık Karşılaşılan Sorunlar

### **1. Template Not Found**

**Hata:**
```
jinja2.exceptions.TemplateNotFound: index.html
```

**Çözüm:**
- `templates/` klasörünün `app.py` ile aynı dizinde olması gerekir
```
project/
├── app.py
└── templates/
    └── index.html
```

### **2. Static Dosyalar Yüklenmiyor**

**Çözüm:**
```
project/
├── app.py
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```

```html
<!-- HTML'de kullanım -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
<script src="{{ url_for('static', filename='js/script.js') }}"></script>
```

---

## 🌐 Production Deployment

### **Render.com'da Deploy**

**render.yaml:**
```yaml
services:
  - type: web
    name: chicken-disease-classifier
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn app:app"
```

### **Heroku'da Deploy**

**Procfile:**
```
web: gunicorn app:app
```

**requirements.txt:**
```
Flask==3.1.2
tensorflow==2.20.0
Pillow
gunicorn
```

---

## 🎯 Özet

| Özellik | Açıklama |
|---------|----------|
| **Dosya** | `index.html` |
| **Amaç** | Kullanıcı arayüzü |
| **Framework** | Flask + Jinja2 |
| **Özellikler** | Görüntü yükleme, tahmin gösterme |
| **Stil** | CSS (inline veya external) |

---

**Önemli:** `templates/` klasörü Flask'ın otomatik olarak HTML dosyalarını aradığı özel bir klasördür. İsmi değiştirilmemelidir!
