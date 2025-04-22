import face_recognition
import io
import threading
import time
import os
import json
import base64
from PIL import Image


class MessageHandler:
    def __init__(self):
        self.client = None
        self.latest_frame = None
        self.frame_lock = threading.Lock()
        self.frame_ready = threading.Event()
        self.handlers = {
            "webcam/feed": self.handle_webcam_feed,
            "hub/user/register": self.handle_user_registration,
            "hub/users/get": self.handle_get_users,
        }
        self.init_storage()

        threading.Thread(target=self.recognition_worker, daemon=True).start()

    def init_storage(self):
        if not os.path.exists("users.json"):
            with open("users.json", "w") as f:
                json.dump([], f)

    def set_client(self, client):
        self.client = client
    def handle_message(self, topic: str, payload) -> None:
        if topic in self.handlers:
            self.handlers[topic](payload)
        else:
            print(f"No handler found for topic: {topic}")


    # Incoming webcam feed
    def handle_webcam_feed(self, payload) -> None:
        with self.frame_lock:
            self.latest_frame = payload.encode() if isinstance(payload, str) else payload
        self.frame_ready.set()
    def process_frame(self, jpeg_bytes):
        try:
            image = face_recognition.load_image_file(io.BytesIO(jpeg_bytes))
            face_landmarks_list = face_recognition.face_landmarks(image)
            print(face_landmarks_list)
            if len(face_landmarks_list):
                print('face', flush=True)
                self.client.publish("lora/send/D1/open_servo", 180)
            else:
                print('no face', flush=True)
        except Exception as e:
            print(f"Error processing frame: {e}", flush=True)
    def recognition_worker(self):
        print("Recognition worker started", flush=True)
        while True:
            self.frame_ready.wait()
            while True:
                time.sleep(.33)

                with self.frame_lock:
                    frame_to_process = self.latest_frame
                    self.latest_frame = None
                    self.frame_ready.clear()
                if frame_to_process:
                    self.process_frame(frame_to_process)
                else:
                    break

    # Users
    def handle_user_registration(self, payload):
        try:
            data = json.loads(payload.decode())

            with open('users.json', 'r') as f:
                users = json.load(f)

            face_encodings = []
            for base64_image in data['images']:
                if ',' in base64_image:
                    base64_image = base64_image.split(',')[1]

                image_bytes = base64.b64decode(base64_image)
                image = face_recognition.load_image_file(io.BytesIO(image_bytes))
                encodings = face_recognition.face_encodings(image)
                print(encodings)
                if not encodings:
                    continue

                print(encodings)
                face_encodings.append(encodings[0].tolist())

            users.append({
                "id": data['id'],
                "name": data['name'],
                "images": data['images'],
                "encodings": face_encodings
            })

            with open('users.json', 'w') as f:
                json.dump(users, f, indent=2)

            self.client.publish(f"hub/user/register/{data['id']}/confirm", json.dumps({
                "success": True,
            }))

        except Exception as e:
            print(f"Error registering user: {e}")
    def handle_get_users(self, payload):
        with open('users.json', 'r') as f:
            users = json.load(f)

        response = []
        for user in users:
            response.append({
                "id": user['id'],
                "name": user['name'],
                "preview": user["images"][0]
            })

        self.client.publish("hub/users/get/response", json.dumps(response))
