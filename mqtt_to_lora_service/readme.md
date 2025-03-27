## Wiring
SX1278 to Raspberry Pi 4B Wiring
================================

| SX1278 Pin | Raspberry Pi Pin | GPIO    | Description              |
|------------|------------------|---------|--------------------------|
| VCC        | Pin 1            | –       | 3.3V Power   |
| GND        | Pin 6            | –       | Ground                   |
| SCK        | Pin 23           | GPIO11  | SPI Clock                |
| MISO       | Pin 21           | GPIO9   | SPI MISO                 |
| MOSI       | Pin 19           | GPIO10  | SPI MOSI                 |
| NSS        | Pin 24           | GPIO8   | SPI Chip Select (CS/SS)  |
| RESET      | Pin 22           | GPIO25  | Reset                    |
| DIO0       | Pin 18           | GPIO24  | Interrupt (RX Done)      |
