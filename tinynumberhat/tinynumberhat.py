from smbus import  SMBus
from datetime import datetime
import time

HT16K33_ADDRESS_0 = 0x70
HT16K33_CMD_BRIGHTNESS = 0xE0
HT16K33_ENABLE_DISPLAY = 0x81
HT16K33_TURN_ON_OSCILLATOR = 0x21
LED_DRIVER_BRIGHTNESS_LEVEL = 6

class TinynumberHat():

	def __init__(self) -> None:
		
		self.bus = SMBus(2)
		self.ht16k33_i2c_address = HT16K33_ADDRESS_0

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
		time.sleep(5.1)
		# Clear display 
		self.bus.write_i2c_block_data(self.ht16k33_i2c_address, 0x00, [0x00] * 16)


		self.numbers = {
			'0': 0b00111111, 
			'1': 0b00000110,
			'2': 0b01011011,
			'3': 0b01001111,
			'4': 0b01100110,
			'5': 0b01101101,
			'6': 0b01111101,
			'7': 0b00000111,
			'8': 0b01111111, 
			'9': 0b01101111,
			'.': 0b10000000,

			
			'P': 0b01110011,
			'L': 0b00111000,
			'A': 0b01110111,
			'Y': 0b01101110,
			'S': 0b01101101,
			'T': 0b01111000,
			'O': 0b01011100,
			'U': 0b00111110,  
			'E': 0b01111001,
			' ': 0b00000000,
			'H': 0b01110110, 
			'-': 0b01000000,
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

	def shoe_time(self):
		buffer = [0x00 for x in range(0, 16)]

		i = True
		while True:
			i = ~i 
			time_now =  datetime.now().strftime('%H-%M-%S%f')
			# print(datetime.now().strftime('%H.%M.%S.%f'))
			buffer[0] = self.numbers.get(time_now[0], 0b01000000)
			buffer[1] = self.numbers.get(time_now[1], 0b01000000) 

			buffer[2] = self.numbers.get(time_now[2], 0b01000000)
			buffer[3] = self.numbers.get(time_now[3], 0b01000000) 

			buffer[4] = self.numbers.get(time_now[4], 0b01000000)
			buffer[5] = self.numbers.get(time_now[5], 0b01000000) 

			buffer[6] = self.numbers.get(time_now[6], 0b01000000)
			buffer[7] = self.numbers.get(time_now[7], 0b01000000) | 0b10000000 if i == True  else self.numbers.get(time_now[7], 0b01000000)
			buffer[8] = self.numbers.get(time_now[8], 0b01000000) 
			# buffer[0] = 0b00000011
			#Write buffer 
			self.bus.write_i2c_block_data(self.ht16k33_i2c_address, 0x00, buffer)
			# keys = bus.read_i2c_block_data(ht16k33_i2c_address, 0x40, 5)
			# print(keys)
			time.sleep(0.1)
			



if __name__ == "__main__":
	tinynumberhat = TinynumberHat()
	tinynumberhat.shoe_time()

