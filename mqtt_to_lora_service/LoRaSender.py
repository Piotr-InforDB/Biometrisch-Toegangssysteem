from constants import *
from LoRa import LoRa

class LoRaSender(LoRa):
    def __init__(self, verbose=False):
        super(LoRaSender, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([1, 0, 0, 0, 0, 0])

    def on_tx_done(self):
        print("Message sent.")
        self.clear_irq_flags(TxDone=1)
        self.set_mode(MODE.STDBY)