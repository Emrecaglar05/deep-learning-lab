# Flask Web Uygulaması - Tavuk Hastalığı Tespiti
# Bu dosya, eğitilmiş modeli web arayüzü üzerinden kullanılabilir hale getirir.

import sys
import os
# src klasörünü Python path'ine ekle (modül import için)
sys.path.append(os.path.join(os.getcwd(), "src"))

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from cnnClassifier.pipeline.prediction import PredictionPipeline


os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app)


class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        self.classifier = PredictionPipeline(self.filename)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/train", methods=['GET','POST'])
@cross_origin()
def trainRoute():
    # Eğer modeli web üzerinden eğitmek isterseniz buraya kod ekleyebilirsiniz
    # os.system("python main.py")
    # os.system("dvc repro")
    return "Training done successfully!"


@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRoute():
    try:
        # Dosya yükleme kontrolü
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if file:
            # Yüklenen dosyayı kaydet
            filename = "inputImage.jpg"
            filepath = os.path.join(os.getcwd(), filename)
            file.save(filepath)
            
            print(f"Dosya kaydedildi: {filepath}")
            
            # Tahmin yap
            classifier = PredictionPipeline(filepath)
            result = classifier.predict()
            
            print(f"Tahmin sonucu: {result}")
            
            return jsonify(result)
        
        return jsonify({"error": "File processing failed"}), 400
        
    except Exception as e:
        print(f"Hata detayı: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
