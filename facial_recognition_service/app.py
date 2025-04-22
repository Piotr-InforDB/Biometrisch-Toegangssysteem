import paho.mqtt.client as mqtt
from messageHandler import MessageHandler

#TODO Uncomment
# MQTT_BROKER = 'accesscontrol.home'
MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_USERNAME = 'facial_recognition_service'
MQTT_PASSWORD = 'admin'
MQTT_TOPICS = [
    'webcam/feed',
    'hub/user/register',
    'hub/users/get',
]

messageHandler = MessageHandler()

def on_connect(client, userdata, flags, rc, properties=None):
    print('Connected with result code ' + str(rc), flush=True)
    messageHandler.set_client(client)
    for topic in MQTT_TOPICS:
        client.subscribe(topic)

def on_message(client, userdata, msg):
    messageHandler.handle_message(msg.topic, msg.payload)

client = mqtt.Client(client_id="facial_recognition_service")
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_forever()