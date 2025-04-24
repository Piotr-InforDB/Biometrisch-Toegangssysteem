import face_recognition
import io
import threading
import time
import os
import json
import base64
import numpy as np
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
        os.makedirs('users_images', exist_ok=True)

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
            face_encodings = face_recognition.face_encodings(image)

            face = False
            recognized = False
            recognized_user = None

            if face_encodings:
                face = True
                with open('users.json', 'r') as f:
                    users = json.load(f)

                for user in users:
                    user_encodings = user['encodings']
                    matches = face_recognition.compare_faces(user_encodings, face_encodings[0], tolerance=0.75)
                    print(matches)


                    if True in matches:
                        recognized = True
                        recognized_user = self.create_user_instance(user)
                        print(f'Recognized user: {recognized_user}', flush=True)
                        self.client.publish("lock/open", '180')

            self.client.publish('facial_recognition/status', json.dumps({
                "face": face,
                "recognized": recognized,
                "user": recognized_user,
            }))

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
        print("User registration started", flush=True)
        try:
            data = json.loads(payload.decode())

            with open('users.json', 'r') as f:
                users = json.load(f)

            face_encodings = []
            for index, base64_image in enumerate(data['images']):
                try:
                    if ',' in base64_image:
                        base64_image = base64_image.split(',')[1]

                    image_filename = f"users_images/{data['id']}_{index}.jpg"
                    compressed_image_bytes = self.compress_image(base64_image, max_size_kb=75)
                    with open(image_filename, "wb") as f:
                        f.write(compressed_image_bytes)

                    with Image.open(image_filename) as img:
                        img.verify()

                    with Image.open(image_filename) as img:
                        img = img.convert('RGB')
                        np_image = np.array(img)

                    encodings = face_recognition.face_encodings(np_image)
                    print(f"Encodings for {image_filename}: {encodings}")

                    if not encodings:
                        print(f"No face found in {image_filename}, skipping.")
                        continue

                    face_encodings.append(encodings[0].tolist())
                except Exception as e:
                    print(f"Failed processing {image_filename}: {e}")
                    continue

            users.append({
                "id": data['id'],
                "name": data['name'],
                "images": data['images'],
                "encodings": face_encodings
            })

            with open('users.json', 'w') as f:
                json.dump(users, f, indent=2)

            print(f"hub/user/register/{data['id']}/confirm", {
                "success": True,
            })

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
            response.append(self.create_user_instance(user))

        self.client.publish("hub/users/get/response", json.dumps(response))
    def create_user_instance(self, user):
        return {
            "id": user['id'],
            "name": user['name'],
            "preview": user["images"][0]
        }

    # Utility
    def compress_image(self, base64_image: str, max_size_kb: int = 100) -> bytes:
        image_bytes = base64.b64decode(base64_image)
        img = Image.open(io.BytesIO(image_bytes)).convert('RGB')

        quality = 85
        output = io.BytesIO()

        while True:
            output.seek(0)
            output.truncate(0)
            img.save(output, format='JPEG', quality=quality)
            size_kb = output.tell() / 1024

            if size_kb <= max_size_kb or quality <= 30:
                break
            quality -= 5

        return output.getvalue()
