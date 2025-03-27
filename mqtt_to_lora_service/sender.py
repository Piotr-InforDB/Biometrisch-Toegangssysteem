from LoRaSender import  LoRaSender
from config import BOARD
from constants import *
import paho.mqtt.client as mqtt

MQTT_USERNAME = 'mqtt_to_lora_service'
MQTT_PASSWORD = 'admin'
MQTT_BROKER = 'accesscontrol.home'
MQTT_PORT = 1883

# Setup
print('Board setup')
BOARD.setup()
print('Board reset')
BOARD.reset()

print('lora sender')
lora = LoRaSender(verbose=False)
print('lora standby')
lora.set_mode(MODE.STDBY)

# LoRa parameters (must match ESP)
print('lora sets')
lora.set_freq(433.0)
lora.set_spreading_factor(7)
lora.set_bw(BW.BW125)
lora.set_coding_rate(CODING_RATE.CR4_5)
lora.set_preamble(8)
lora.set_sync_word(0x12)
lora.set_rx_crc(True)
lora.set_pa_config(pa_select=1, max_power=7, output_power=14)

print("LoRa Transmitter ready")

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Connected with result code: {rc}")
    client.subscribe("lora/send/+/+")

def on_message(client, userdata, msg):
    print(f"Message received on {msg.topic}")

    topic = msg.topic
    data = msg.payload

    topic_parts = topic.split("/")
    device_id = topic_parts[2]
    command = topic_parts[3]

    send_through_lora(device_id, command, data)


client = mqtt.Client(client_id=MQTT_USERNAME)
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
client.connect(MQTT_BROKER, 1883)


def send_through_lora(device_id, command, payload):
    print(f"Sending to {device_id}, command:{command}, message: {payload}")

    message = f"{device_id}:{command}:{payload}"

    lora.write_payload([ord(c) for c in message])
    lora.set_mode(MODE.TX)

client.loop_forever()
