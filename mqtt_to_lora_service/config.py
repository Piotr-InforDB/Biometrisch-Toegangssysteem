""" Defines the BOARD class that contains the board pin mappings and RF module HF/LF info. """
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import spidev
import time


class BOARD:
    """ Board initialisation/teardown and pin configuration is kept here.
        This version is adapted for SX1278 on Raspberry Pi 4B.
    """

    # GPIO pin definitions (BCM mode)
    NSS     = 8    # Pin 24 - SPI Chip Select
    RESET   = 25   # Pin 22 - Reset
    DIO0    = 24   # Pin 18 - DIO0 interrupt
    LED     = 18   # Optional: Use onboard LED or remove
    SWITCH  = 4    # Optional: Repurpose or ignore

    DIO_PINS = [DIO0]

    spi = None
    low_band = True  # SX1278 uses low band (e.g., 433 MHz)

    @staticmethod
    def setup():
        """ Configure the Raspberry GPIOs """
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        # LED
        GPIO.setup(BOARD.LED, GPIO.OUT)
        GPIO.output(BOARD.LED, 0)

        # Optional: switch
        GPIO.setup(BOARD.SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # DIO pins
        for gpio_pin in BOARD.DIO_PINS:
            GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # RESET pin
        GPIO.setup(BOARD.RESET, GPIO.OUT)
        GPIO.output(BOARD.RESET, 1)

        BOARD.blink(0.1, 2)

    @staticmethod
    def reset():
        """ Pulse the RESET pin """
        GPIO.output(BOARD.RESET, 0)
        time.sleep(0.1)
        GPIO.output(BOARD.RESET, 1)
        time.sleep(0.1)

    @staticmethod
    def teardown():
        """ Cleanup GPIO and SpiDev """
        GPIO.cleanup()
        if BOARD.spi:
            BOARD.spi.close()

    @staticmethod
    def SpiDev(spi_bus=0, spi_cs=0):
        """ Init and return the SpiDev object """
        BOARD.spi = spidev.SpiDev()
        BOARD.spi.open(spi_bus, spi_cs)
        BOARD.spi.max_speed_hz = 5000000  # Up to 10MHz supported
        return BOARD.spi

    @staticmethod
    def add_event_detect(dio_number, callback):
        """ Add interrupt for given DIO pin """
        GPIO.add_event_detect(dio_number, GPIO.RISING, callback=callback)

    @staticmethod
    def add_events(cb_dio0=None, cb_dio1=None, cb_dio2=None, cb_dio3=None, cb_dio4=None, cb_dio5=None, switch_cb=None):
        """ Accepts all 6 DIO callbacks even if unused to prevent TypeError """
        if cb_dio0:
            BOARD.add_event_detect(BOARD.DIO0, callback=cb_dio0)
        # Other DIOs not connected, but arguments accepted for compatibility
        if switch_cb:
            GPIO.add_event_detect(BOARD.SWITCH, GPIO.RISING, callback=switch_cb, bouncetime=300)

    @staticmethod
    def led_on(value=1):
        GPIO.output(BOARD.LED, value)
        return value

    @staticmethod
    def led_off():
        GPIO.output(BOARD.LED, 0)
        return 0

    @staticmethod
    def blink(time_sec, n_blink):
        if n_blink == 0:
            return
        BOARD.led_on()
        for _ in range(n_blink):
            time.sleep(time_sec)
            BOARD.led_off()
            time.sleep(time_sec)
            BOARD.led_on()
        BOARD.led_off()
