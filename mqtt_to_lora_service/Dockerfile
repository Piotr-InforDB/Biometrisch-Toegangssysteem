FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    python3-rpi.gpio \
    && rm -rf /var/lib/apt/lists/*


COPY . .

RUN pip install spidev RPI.GPIO paho-mqtt

CMD ["python", "-u", "sender.py"]
