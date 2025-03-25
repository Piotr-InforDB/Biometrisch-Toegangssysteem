FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y build-essential cmake libgl1 libglib2.0-0 && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

CMD ["python", "facial_recognition.py"]
