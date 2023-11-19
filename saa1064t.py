from smbus import SMBus
import time 

SAA1064_ADDRESS = 0x38 

bus = SMBus(2)

'''C0 = 0 static mode, i.e. continuous display of digits 1 and 2
C0 = 1 dynamic mode, i.e. alternating display of digit 1 + 3 and 2 + 4
C1 = 0/1 digits 1 + 3 are blanked/not blanked
C2 = 0/1 digits 2 + 4 are blanked/not blanked
C3 = 1 all segment outputs are switched-on for segment test(1)
C4 = 1 adds 3 mA to segment output current
C5 = 1 adds 6 mA to segment output current
C6 = 1 adds 12 mA to segment output current
Byte order:
    X,C6,C5,C4,C3,C2,C1,C0
'''



#Config Driver 
CONTROL_REG = 0b00100000
bus.write_i2c_block_data(SAA1064_ADDRESS, 0x00, [CONTROL_REG])


digit_font = {
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
    
}


def circular_left_rotate(num, shift, num_bits=8):
    shift %= num_bits
    return ((num << shift) | (num >> (num_bits - shift))) & ((1 << num_bits) - 1)

while True:
    for key in 'PLAY ':
        digit_1 = digit_font.get(key, 0x00)
        bus.write_i2c_block_data(SAA1064_ADDRESS, 0x01, [digit_1, 0x00, 0x00, 0x00])
        time.sleep(0.5)
    time.sleep(1)

    for key in 'PAUSE ':
        digit_1 = digit_font.get(key, 0x00)
        bus.write_i2c_block_data(SAA1064_ADDRESS, 0x01, [digit_1, 0x00, 0x00, 0x00])
        time.sleep(0.5)
    time.sleep(2)

    for key in '1234567890. ':
        digit_1 = digit_font.get(key, 0x00)
        bus.write_i2c_block_data(SAA1064_ADDRESS, 0x01, [digit_1, 0x00, 0x00, 0x00])
        time.sleep(0.5)
    time.sleep(1)
    
    for key in 'STOP ':
        digit_1 = digit_font.get(key, 0x00)
        bus.write_i2c_block_data(SAA1064_ADDRESS, 0x01, [digit_1, 0x00, 0x00, 0x00])
        time.sleep(0.5)
    time.sleep(1)
