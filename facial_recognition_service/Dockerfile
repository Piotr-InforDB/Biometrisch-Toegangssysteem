FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y build-essential cmake libgl1 libglib2.0-0 && \
    pip install --upgrade pip && \
    pip install paho-mqtt face_recognition opencv-python numpy

COPY . .

CMD ["python", "app.py"]
