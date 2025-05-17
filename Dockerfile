FROM python:3.10-slim

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# 安裝 Python 套件
RUN pip install --upgrade pip
RUN pip install Flask torch rembg Pillow numpy ultralytics onnxruntime

# 設置工作目錄
WORKDIR /app

# 複製所有檔案
COPY . /app

# 啟動 Flask 應用
CMD ["flask", "run", "--host=0.0.0.0"]
