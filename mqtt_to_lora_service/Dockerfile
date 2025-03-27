FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    python3-rpi.gpio \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install spidev RPI.GPIO

CMD ["python3", "sender.py"]
