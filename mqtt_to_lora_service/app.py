from LoRaSender import  LoRaSender
from config import BOARD
from constants import *

import time
import threading
import paho.mqtt.client as mqtt

MQTT_USERNAME = 'mqtt_to_lora_service'
MQTT_PASSWORD = 'admin'
MQTT_BROKER = 'accesscontrol.home'
MQTT_PORT = 1883

LORA_TX_TIME = 0.5

print('Board setup')
BOARD.setup()
print('Board reset')
BOARD.reset()

print('lora sender')
lora = LoRaSender(verbose=False)
print('lora standby')
lora.set_mode(MODE.STDBY)

print('lora sets')
lora.set_freq(433.0)
lora.set_spreading_factor(10)
lora.set_bw(BW.BW125)
lora.set_coding_rate(CODING_RATE.CR4_5)
lora.set_preamble(8)
lora.set_sync_word(0x12)
lora.set_rx_crc(True)
lora.set_pa_config(pa_select=1, max_power=7, output_power=14)
lora.set_mode(MODE.RXCONT)

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

    try:
        payload = data.decode("utf-8")
        send_through_lora(device_id, command, payload)
    except UnicodeDecodeError as e:
        print(f"Failed to decode payload: {e}")
        return


client = mqtt.Client(client_id=MQTT_USERNAME)
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
client.connect(MQTT_BROKER, 1883)


def send_through_lora(device_id, command, payload):
    message = f"{device_id}:{command}:{payload}"
    print(f"Sending to LoRa: {message}")

    bytes = list(message.encode())
    lora.tx_time = time.time()

    lora.write_payload(bytes)
    lora.set_mode(MODE.TX)

def on_lora_message(message):
    print(message)
    message_parts = message.split(":")
    device_id = message_parts[0]
    topic = message_parts[1]
    message = message_parts[2]

    print(f"Received LoRa message: {message}")
    print(f"Sending to MQTT: {topic} : {message}")

    client.publish(topic, message)

def show_mode():
    while True:
        if lora.mode == 131 and lora.tx_time and time.time() - lora.tx_time > LORA_TX_TIME:
            print("Setting mode to RX")
            lora.set_mode(MODE.RXCONT)
        time.sleep(0.5)

threading.Thread(target=show_mode, daemon=True).start()
lora.set_rx_callback(on_lora_message)
client.loop_forever()
