# 📂 PROJE YAPISI - KİM NE İŞE YARAR?

Bu dosya, projedeki klasör ve dosyaların "bilale anlatır gibi" açıklamalarını içerir.

---

## 📂 KLASÖRLER (Odanın Bölümleri)

### 📂 .github (Otomasyon Robotu)
Kodunu internete (GitHub'a) attığında arkada gizlice çalışan robotların ofisi. "Kod bozuk mu?" diye kontrol eden testler burada durur.

### 📂 config (Ayar Merkezi)
Kodun beynini açıp ameliyat yapmamak için; değiştirilmesi gereken tüm ayarların (dosya yolları, sabit sayılar) tutulduğu yerdir. Kumanda merkezi.

### 📂 logs (Kara Kutu / Günlük)
Program çalışırken ne yaptı, nerede hata verdi, saat kaçta patladı? Her şeyin kaydının tutulduğu yer. Dedektifler hata ararken önce buraya bakar.

### 📂 research (Karalama Defteri)
Burası laboratuvar. Kodun son halini almadan önceki deneme-yanılma çalışmaların (Jupyter not defterlerin) burada durur. Ortalık dağınık olabilir, serbest bölge.

### 📂 src (Beyin Takımı)
Projenin asıl çalışan, iş yapan, temiz kodları buradadır. Projenin kalbi ve zekası bu klasörün içindedir.

### 📂 templates (Kalıplar)
Eğer bir web sitesi yapıyorsan, sitenin iskelet tasarımı (HTML dosyaları) burada durur.

---

## 📄 DOSYALAR (Kağıt Kürek İşleri)

### 🛑 .gitignore (Çöp Filtresi)
İnternete yüklenmemesi gereken; gereksiz, gizli veya çok şişko dosyaların listesidir. Git'e "Bunları görmezden gel, yükleme" der.

### 🗺️ dvc.yaml (İş Haritası)
Veri işleme hattının haritasıdır. Hangi adımdan sonra ne çalışacak, veri nereden girip nereden çıkacak bu dosya yönetir. Trafik polisi gibidir.

### ▶️ main.py (Başlat Düğmesi)
Tüm projeyi ayağa kaldıran ana dosya. Buna basarsın (çalıştırırsın), sistem işlemeye başlar.

### ⚙️ params.yaml (İnce Ayarlar)
Modelin öğrenme hızı, tekrar sayısı gibi hassas parametreleri buradadır. Yemeğin tuzu biberi buradan ayarlanır.

### 📖 README.md (Vitrin / Kullanma Kılavuzu)
Proje nedir, nasıl kurulur, kim yaptı? Projeye ilk bakan kişi önce bunu okur.

### 🛒 requirements.txt (Alışveriş Listesi)
Bu projenin çalışması için bilgisayara yüklenmesi gereken malzemelerin (kütüphanelerin) listesidir. "Markete git şunları al gel" listesi.

### 📦 setup.py (Paketleyici)
Bu projeyi başkaları da bilgisayarına kolayca kurabilsin diye projenin kimlik bilgilerini ve sürümünü içeren dosyadır.

### 🏗️ template.py (İnşaat Ustası)
(Genelde proje başında kullanılır) Bu gördüğün klasör yapısını tek tek elle açmak yerine, tek tıkla otomatik oluşturmak için yazılmış yardımcı bir kod parçasıdır.