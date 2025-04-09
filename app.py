from flask import Flask, render_template, request, jsonify, abort
import torch
import io
import os
import logging
from rembg import remove
from PIL import Image
import numpy as np
from ultralytics import YOLO

app = Flask(__name__)

# Config
model_path = os.getenv('MODEL_PATH', '/home/whale/idkhowtoteach/runs/classify/train3/weights/best.pt')
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
CLASS_TRANSLATION = {
    "bottle": "寶特瓶",
    "general_waste": "一般垃圾",
    "hard_plastic": "硬塑膠",
    "mixed_waste": "混和垃圾",
    "paper": "紙類",
    "paper_containers": "紙容器",  
    "retort_pouch": "鋁箔包",  
    "soft_plastic": "軟塑膠",
    "tin_and_aluminum_cans": "鐵鋁罐"
}

# 直接在啟動時載入模型（適用於 Flask 2.3+）
model = YOLO(model_path)

def preprocess_image(input_image: bytes, target_size=(512, 512)):
    try:
        output_image = remove(input_image)
        with io.BytesIO(output_image) as buffer:
            img = Image.open(buffer)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img = img.resize(target_size, Image.LANCZOS)
            return img
    except Exception as e:
        logging.error(f"Image preprocessing failed: {str(e)}", exc_info=True)
        raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # 檢查檔案類型
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}):
        return jsonify({'error': 'Unsupported file type'}), 400
    
    # 檢查檔案大小
    file.seek(0, os.SEEK_END)
    if file.tell() > MAX_FILE_SIZE:
        abort(413)
    file.seek(0)
    
    try:
        image_bytes = file.read()
        img_array = np.array(preprocess_image(image_bytes))
        results = model.predict(img_array)
        top1_class = results[0].names[results[0].probs.top1]
        prediction = CLASS_TRANSLATION.get(top1_class, top1_class)
        
        return f'''
        <html>
            <head><meta charset="UTF-8"><title>垃圾分類結果</title></head>
            <body>
                <h1 style="font-size: 96px;">{prediction}</h1>
                <a href="/">再辨識一張</a>
            </body>
        </html>
        '''
    except Exception as e:
        logging.error(f"Prediction error: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='23.146.248.101', port=13579, debug=False)
