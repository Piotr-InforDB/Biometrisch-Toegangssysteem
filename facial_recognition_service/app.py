import paho.mqtt.client as mqtt
import face_recognition
import threading
import io
import time
from PIL import Image

MQTT_BROKER = 'accesscontrol'
MQTT_PORT = 1883
MQTT_TOPIC = 'webcam/feed'
MQTT_USERNAME = 'facial_recognition_service'
MQTT_PASSWORD = 'admin'

latest_frame = None
frame_lock = threading.Lock()
frame_ready = threading.Event()

def on_connect(client, userdata, flags, rc, properties=None):
    print('Connected with result code ' + str(rc), flush=True)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global latest_frame
    with frame_lock:
        latest_frame = msg.payload
    frame_ready.set()

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
    global latest_frame
    print("Recognition worker started", flush=True)
    while True:
        frame_ready.wait()
        while True:

            time.sleep(.33)

            with frame_lock:
                frame_to_process = latest_frame
                latest_frame = None
                frame_ready.clear()
            if frame_to_process:
                process_frame(frame_to_process)
            else:
                break

threading.Thread(target=recognition_worker, daemon=True).start()

client = mqtt.Client(client_id="facial_recognition_service")
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_forever()
