from time import sleep

import paho.mqtt.client as mqtt
import face_recognition
import os
import time
import threading
import queue
from pathlib import Path
import io
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

MQTT_BROKER = 'accesscontrol'
MQTT_PORT = 1883
MQTT_TOPIC = 'webcam/feed'
MQTT_USERNAME = 'facial_recognition_service'
MQTT_PASSWORD = 'admin'

executor = ThreadPoolExecutor(max_workers=2)

latest_frame = None
frame_lock = threading.Lock()

def on_connect(client, userdata, flags, rc, properties=None):
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global latest_frame
    with frame_lock:
        latest_frame = msg.payload

def process_frame(jpeg_bytes):
    try:
        image = face_recognition.load_image_file(io.BytesIO(jpeg_bytes))
        face_landmarks_list = face_recognition.face_landmarks(image)
        print(face_landmarks_list)
        if len(face_landmarks_list):
            print('face', flush=True)
        else:
            print('no face', flush=True)
    except Exception as e:
        print(f"Error processing frame: {e}", flush=True)

def recognition_worker():
    print("Recognition worker started")
    last_frame = None
    while True:
        time.sleep(1)
        with frame_lock:
            current_frame = latest_frame
        if current_frame is not None and current_frame != last_frame:
            last_frame = current_frame
            executor.submit(process_frame, current_frame)

recognition_thread = threading.Thread(target=recognition_worker, daemon=True)
print("Starting recognition thread")
recognition_thread.start()

client = mqtt.Client(client_id="facial_recognition_service")
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_forever()
