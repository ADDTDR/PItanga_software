from smbus import  SMBus
from datetime import datetime
import time

HT16K33_ADDRESS_0 = 0x70
HT16K33_CMD_BRIGHTNESS = 0xE0
HT16K33_ENABLE_DISPLAY = 0x81
HT16K33_TURN_ON_OSCILLATOR = 0x21
LED_DRIVER_BRIGHTNESS_LEVEL = 15

	bus = SMBus(0)
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

	numbers_2 = {
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

	buffer = [0x00 for x in range(0, 16)]

	i = True
	while True:
	    i = ~i 
	    time_now =  datetime.now().strftime('%H-%M-%S%f')
	    # print(datetime.now().strftime('%H.%M.%S.%f'))
	    buffer[0] = numbers.get(time_now[0], 0b01000000)
	    buffer[1] = numbers.get(time_now[1], 0b01000000) 

	    buffer[2] = numbers.get(time_now[2], 0b01000000)
	    buffer[3] = numbers.get(time_now[3], 0b01000000) 

	    buffer[4] = numbers.get(time_now[4], 0b01000000)
	    buffer[5] = numbers.get(time_now[5], 0b01000000) 

	    buffer[6] = numbers.get(time_now[6], 0b01000000)
	    buffer[7] = numbers.get(time_now[7], 0b01000000) | 0b10000000 if i == True  else numbers.get(time_now[7], 0b01000000)
	    buffer[8] = 0xff
	    # buffer[0] = 0b00000011
	    #Write buffer 
	    bus.write_i2c_block_data(ht16k33_i2c_address, 0x00, buffer)
	    # keys = bus.read_i2c_block_data(ht16k33_i2c_address, 0x40, 5)
	    # print(keys)
	    time.sleep(0.1)
	    
