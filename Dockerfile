FROM python:3.9

RUN pip3 install --upgrade pip
RUN pip3 install Flask torch rembg Pillow numpy ultralytics onnxruntime

RUN apt-get update
RUN apt-get install chromium -y

WORKDIR /app
COPY . /app
ENTRYPOINT [ "python3" ]
CMD ["app.py" ]
