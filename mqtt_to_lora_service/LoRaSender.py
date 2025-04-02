from constants import *
from LoRa import LoRa

class LoRaSender(LoRa):
    def __init__(self, verbose=False):
        super(LoRaSender, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0, 0, 0, 0, 0, 0])
        self.rx_callback = None
        self.set_mode(MODE.RXCONT)

    def on_tx_done(self):
        print("Message sent.")
        self.clear_irq_flags(TxDone=1)
        self.set_mode(MODE.STDBY)

    def on_rx_done(self):
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        try:
            message = bytes(payload).decode()
            print(f"Received LoRa: {message}")
            if self.rx_callback:
                self.rx_callback(message)
        except Exception as e:
            print(f"Failed to decode payload: {e}")
        self.set_mode(MODE.RXCONT)

    def set_rx_callback(self, callback):
        self.rx_callback = callback