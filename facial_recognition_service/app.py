import paho.mqtt.client as mqtt
import face_recognition
import os
import threading
import queue
from pathlib import Path

MQTT_BROKER = 'accesscontrol'
MQTT_PORT = 1883
MQTT_TOPIC = 'webcam/feed'
MQTT_USERNAME = 'facial_recognition_service'
MQTT_PASSWORD = 'admin'

frame_queue = queue.Queue(maxsize=1)

def on_connect(client, userdata, flags, rc, properties=None):
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    if frame_queue.full():
        try:
            frame_queue.get_nowait()
        except queue.Empty:
            pass
    frame_queue.put(msg.payload)

def recognition_worker():
    while True:
        jpeg_bytes = frame_queue.get()

        filename = Path("last_frame.jpg")
        with open(filename, "wb") as f:
            f.write(jpeg_bytes)

        image = face_recognition.load_image_file(filename)
        face_landmarks_list = face_recognition.face_landmarks(image)

        if len(face_landmarks_list):
            print('face')
        else:
            print('no face')

        os.remove(filename)

recognition_thread = threading.Thread(target=recognition_worker, daemon=True)
recognition_thread.start()

client = mqtt.Client(client_id="facial_recognition_service")
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_forever()
