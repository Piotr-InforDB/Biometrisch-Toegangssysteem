from LoRa import LoRa
from config import BOARD
from constants import *

import time


class LoRaSender(LoRa):
    def __init__(self, verbose=False):
        super(LoRaSender, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([1, 0, 0, 0, 0, 0])  # DIO0 will trigger TxDone interrupt

    def on_tx_done(self):
        print("Message sent.")
        self.clear_irq_flags(TxDone=1)
        self.set_mode(MODE.STDBY)


# Setup
BOARD.setup()
BOARD.reset()

lora = LoRaSender(verbose=False)
lora.set_mode(MODE.STDBY)

# LoRa parameters (must match ESP)
lora.set_freq(433.0)
lora.set_spreading_factor(7)
lora.set_bw(BW.BW125)
lora.set_coding_rate(CODING_RATE.CR4_5)
lora.set_preamble(8)
lora.set_sync_word(0x12)
lora.set_rx_crc(True)
lora.set_pa_config(pa_select=1, max_power=7, output_power=14)

print("LoRa Transmitter ready")

try:
    counter = 0
    while True:
        message = f"Hello from Pi #{counter}"
        print(f"Sending: {message}")

        lora.write_payload([ord(c) for c in message])
        lora.set_mode(MODE.TX)

        counter += 1
        time.sleep(3)

except KeyboardInterrupt:
    print("Transmitter stopped")
    BOARD.teardown()
