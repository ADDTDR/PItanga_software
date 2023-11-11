from smbus import  SMBus
import time

HT16K33_ADDRESS_0 = 0x72
HT16K33_CMD_BRIGHTNESS = 0xE0
HT16K33_ENABLE_DISPLAY = 0x81
HT16K33_TURN_ON_OSCILLATOR = 0x21
LED_DRIVER_BRIGHTNESS_LEVEL = 15

bus = SMBus(2)
ht16k33_i2c_address = HT16K33_ADDRESS_0

# Turn on oscillator 
bus.write_byte(ht16k33_i2c_address, HT16K33_TURN_ON_OSCILLATOR)
# Enable display (no blinking mode)
bus.write_byte(ht16k33_i2c_address, HT16K33_ENABLE_DISPLAY)
# Clear display 
bus.write_i2c_block_data(ht16k33_i2c_address, 0x00, [0x00] * 16)
# Set brightness 0-15
bus.write_byte(ht16k33_i2c_address, HT16K33_CMD_BRIGHTNESS | LED_DRIVER_BRIGHTNESS_LEVEL)

# Fill with 1, turn on all segments 
bus.write_i2c_block_data(ht16k33_i2c_address, 0x00, [0xff] * 16)
time.sleep(0.05)
# Clear display 
bus.write_i2c_block_data(ht16k33_i2c_address, 0x00, [0x00] * 16)


numbers = {
    1: 0b00000011,
    2: 0b01110110,
    3: 0b00110111,
    4: 0b00011011,
    5: 0b00111101,
    6: 0b01111101,
    7: 0b00000111,
    8: 0b01111111,
    9: 0b00111111, 
    0: 0b01101111 
}

buffer = [0x00 for x in range(0, 16)]

i = 0
while True:
    i = i + 1 if i < 9 else 0

    buffer[0] = numbers.get(i, 0x00)
    #Write buffer 
    bus.write_i2c_block_data(ht16k33_i2c_address, 0x00, buffer)
    time.sleep(0.2)
    