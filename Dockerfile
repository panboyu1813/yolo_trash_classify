FROM python:3.9

RUN pip3 install --upgrade pip
RUN pip3 install Flask torch rembg Pillow numpy ultralytics onnxruntime

WORKDIR /app
COPY . /app
ENTRYPOINT [ "python3" ]
CMD ["app.py" ]
