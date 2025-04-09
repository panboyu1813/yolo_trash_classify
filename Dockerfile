FROM python:3.9

# 更新 pip
RUN pip3 install --upgrade pip

# 安裝必要的系統依賴（libGL.so.1）
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# 安裝 Python 依賴
RUN pip3 install Flask torch rembg Pillow numpy ultralytics onnxruntime

# 設置工作目錄
WORKDIR /app

# 複製當前目錄的文件到容器內部
COPY . /app

# 設定容器啟動命令
ENTRYPOINT [ "python3" ]
CMD ["app.py"]
