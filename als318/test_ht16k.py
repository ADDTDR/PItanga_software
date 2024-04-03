from smbus import SMBus
from random import randint 
import time 

HT16K33_ADDRESS_0 = 0x70
HT16K33_TURN_ON_OSCILLATOR = 0x21 
HT16K33_ENABLE_DISPLAY = 0x81
HT16K33_CMD_BRIGHTNESS = 0xE0
LED_DRIVER_BRIGHTNESS_LEVEL = 0x0A
SMBUS = 1

bus = SMBus(SMBUS)
bus.write_byte(HT16K33_ADDRESS_0, HT16K33_TURN_ON_OSCILLATOR)
bus.write_byte(HT16K33_ADDRESS_0, HT16K33_ENABLE_DISPLAY)
bus.write_i2c_block_data(HT16K33_ADDRESS_0, 0x00, [0x00] * 16)
bus.write_byte(HT16K33_ADDRESS_0, HT16K33_CMD_BRIGHTNESS | LED_DRIVER_BRIGHTNESS_LEVEL)

for i in range(0, 1000):
    bus.write_i2c_block_data(HT16K33_ADDRESS_0, 0x00, [randint(0, 255) for x in range(0, 16)])
    time.sleep(0.1)



