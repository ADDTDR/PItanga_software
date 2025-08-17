from smbus import SMBus
from datetime import datetime
import time

HT16K33_ADDRESS_0 = 0x70
HT16K33_CMD_BRIGHTNESS = 0xE0
HT16K33_ENABLE_DISPLAY = 0x81
HT16K33_TURN_ON_OSCILLATOR = 0x21
LED_DRIVER_BRIGHTNESS_LEVEL = 15
SMBUS = 1


class TinynumberHat():

    def __init__(self) -> None:
        self.bus = SMBus(SMBUS)
        self.ht16k33_i2c_address = HT16K33_ADDRESS_0
        self.dp = True
        # Turn on oscillator
        self.bus.write_byte(self.ht16k33_i2c_address, HT16K33_TURN_ON_OSCILLATOR)
        # Enable display (no blinking mode)
        self.bus.write_byte(self.ht16k33_i2c_address, HT16K33_ENABLE_DISPLAY)
        # Clear display
        self.bus.write_i2c_block_data(self.ht16k33_i2c_address, 0x00, [0x00] * 16)
        # Set brightness 0-15
        self.bus.write_byte(self.ht16k33_i2c_address, HT16K33_CMD_BRIGHTNESS | LED_DRIVER_BRIGHTNESS_LEVEL)
        # Fill with 1, turn on all segments
        self.bus.write_i2c_block_data(self.ht16k33_i2c_address, 0x00, [0xff] * 16)
        # Clear display
        self.bus.write_i2c_block_data(self.ht16k33_i2c_address, 0x00, [0x00] * 16)

        self.numbers = {
            '0': 0b00111111, '1': 0b00000110, '2': 0b01011011, '3': 0b01001111,
            '4': 0b01100110, '5': 0b01101101, '6': 0b01111101, '7': 0b00000111,
            '8': 0b01111111, '9': 0b01101111, '.': 0b10000000, '-': 0b01000000,
            ' ': 0b00000000, 'A': 0b01110111, 'B': 0b01111100, 'C': 0b00111001,
            'D': 0b01011110, 'E': 0b01111001, 'F': 0b01110001, 'G': 0b00111101,
            'H': 0b01110110, 'I': 0b00110000, 'J': 0b00011110, 'K': 0b01011001,
            'L': 0b00111000, 'M': 0b00010101, 'N': 0b01010100, 'O': 0b00111111,
            'P': 0b01110011, 'Q': 0b01100111, 'R': 0b01010000, 'S': 0b01101101,
            'T': 0b01111000, 'U': 0b00111110, 'V': 0b00111110, 'W': 0b00011101,
            'X': 0b01110110, 'Y': 0b01101110, 'Z': 0b01011011
        }

        self.numbers_2 = {
            1: 0b00000101,
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

    def show_time(self):
        buffer = [0x00 for x in range(0, 16)]
        self.dp = ~self.dp
        time_now = datetime.now().strftime('%H-%M-%S%f')
        buffer[0] = self.numbers.get(time_now[0], 0b01000000)
        buffer[1] = self.numbers.get(time_now[1], 0b01000000)
        buffer[2] = self.numbers.get(time_now[2], 0b01000000)
        buffer[3] = self.numbers.get(time_now[3], 0b01000000)
        buffer[4] = self.numbers.get(time_now[4], 0b01000000)
        buffer[5] = self.numbers.get(time_now[5], 0b01000000)
        buffer[6] = self.numbers.get(time_now[6], 0b01000000)
        buffer[7] = self.numbers.get(time_now[7], 0b01000000) | 0b10000000 if self.dp == True else self.numbers.get(
            time_now[7], 0b01000000)
        buffer[8] = self.numbers.get(time_now[8], 0b01000000)

        self.bus.write_i2c_block_data(self.ht16k33_i2c_address, 0x00, buffer)

    def show_string(self, string):
        buffer = [0x00] * 16
        buffer[0] = self.numbers.get(string[0], 0x00)
        buffer[1] = self.numbers.get(string[1], 0x00)
        buffer[2] = self.numbers.get(string[2], 0x00)
        buffer[3] = self.numbers.get(string[3], 0x00)
        buffer[4] = self.numbers.get(string[4], 0x00)
        buffer[5] = self.numbers.get(string[5], 0x00)
        buffer[6] = self.numbers.get(string[6], 0x00)
        buffer[7] = self.numbers.get(string[7], 0x00)
        buffer[8] = self.numbers.get(string[8], 0x00)
        self.bus.write_i2c_block_data(self.ht16k33_i2c_address, 0x00, buffer)

    def show_date(self):
        buffer = [0x00] * 16
        d = datetime.now().strftime('%d%m-%Y')
        for i in range(len(d)):
            buffer[i] = self.numbers.get(d[i], 0b01000000)
        buffer[1] = buffer[1] | 0b10000000  # put dot
        self.bus.write_i2c_block_data(self.ht16k33_i2c_address, 0x00, buffer)

    def show_timestamp(self):
        buffer = [0x00] * 16
        ts = str(int(time.time()))
        for i in range(min(len(ts), 9)):
            buffer[i] = self.numbers.get(ts[i], 0b01000000)
        self.bus.write_i2c_block_data(self.ht16k33_i2c_address, 0x00, buffer)



    def read_key_data(self):
        keys_data = self.bus.read_i2c_block_data(self.ht16k33_i2c_address, 0x40, 5)
        keys = keys_data[4]
        return keys


if __name__ == "__main__":
    tinynumberhat = TinynumberHat()
    text = ' HELLO HACKADAY 1HZ CHALLENGE '
    mode = 16
    while True:
        key_data = tinynumberhat.read_key_data()
        if key_data != 0:
            mode = key_data
        if mode == 128:
            text = text[1:] + text[:1]
            tinynumberhat.show_string(text)
        elif mode == 16:
            tinynumberhat.show_time()
        elif mode == 32:
            tinynumberhat.show_date()
        elif mode == 64:
            tinynumberhat.show_timestamp()

        time.sleep(0.1)
