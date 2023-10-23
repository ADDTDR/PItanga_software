from smbus import SMBus
import time
from font5x7 import Font5x7_full as Font5x7
from datetime import datetime
from pikachu import pikachu as pikachu_bitmap
from bluetooth_bitmap import bluetooth_bitmap


HT16K33_ADDRESS_1 = 0x71
HT16K33_ADDRESS_0 = 0x70

HT16K33_CMD_BRIGHTNESS = 0xE0
HT16K33_ENABLE_DISPLAY = 0x81
HT16K33_TURN_ON_OSCILLATOR = 0x21
LED_DRIVER_BRIGHTNESS_LEVEL = 2

class HT16K33():

    def __init__(self, ht16k33_i2c_address):
        bus = SMBus(2)
        # Turn on oscillator 
        bus.write_byte(ht16k33_i2c_address, HT16K33_TURN_ON_OSCILLATOR)
        # Enable display (no blinking mode)
        bus.write_byte(ht16k33_i2c_address, HT16K33_ENABLE_DISPLAY)
        # Clear display 
        bus.write_i2c_block_data(ht16k33_i2c_address, 0x00, [0x00] * 16)
        # Set brightness 0-15
        bus.write_byte(ht16k33_i2c_address, HT16K33_CMD_BRIGHTNESS | LED_DRIVER_BRIGHTNESS_LEVEL)
        self.ht16k33_i2c_address = ht16k33_i2c_address
        self.bus = bus
        # Graphic buffer 
        self.buffer = [0x00 for x in range(0, 16)]
        # Decimal point hardware limited to 1 per 3 5x7 displays sine driver support only 16 rows 
        self.decimal_dot_bit = 0

    def set_brightness(self, led_driver_brightness_level):
        self.bus.write_byte(self.ht16k33_i2c_address, HT16K33_CMD_BRIGHTNESS | led_driver_brightness_level)

    def rotate_90(self, a):
        b = []
        for k in range(0, 7):       	
            q = [(x & (1 << k)) >> k for x in a ]
            qi = 0
            for bit in q:    
                qi = (qi << 1) | bit
            b.append(qi)
        return b

    def clear(self):
        self.buffer = [ 0x00 for x in range(0, 16)]
        

    def read_key_data(self):
        # read all keys
        key_data = self.bus.read_i2c_block_data(self.ht16k33_i2c_address, 0x45, 1)
        return key_data[0]


    def fill(self):
        self.buffer = [0xff for x in range(0, 16)]
    
    def decimal_dot(self):
        # First bit connected to decimal point on second display  ltp305
        # Row 15, pin 10,  on ht16k33 
        self.buffer[13] = 0xff & 0b10000000


    def update(self):
        self.bus.write_i2c_block_data(self.ht16k33_i2c_address, 0x00, self.buffer)
        

    def write_data_raw(self, a, b, c):  
        bx = []
        ax = a
        kx = b 
        cx = c
        
        # Push data to common raw buffer 
        for e in ax:
            bx.append(e)
        for e in kx:
            bx.append(e)
        for e in cx:
            bx.append(e)

        # Distribute data between lines 
        # Place 3 
        # Row1
        self.buffer[0] = bx[0] & 0x1f
        # Row2
        self.buffer[2] = bx[1] & 0x1f
        # Row3
        self.buffer[4] = bx[2] & 0x1f
        # Row4
        self.buffer[6] = bx[3] & 0x1f
        # Row5
        self.buffer[8] = bx[4] & 0x1f 
        # Row6
        self.buffer[10] = bx[5] & 0x1f  
        # Row7
        self.buffer[12] = bx[6] & 0x1f
        # Row8
        self.buffer[14] = 0xff & 0x00 
    
        # Place 2 
        # Row 1
        self.buffer[1] = (bx[0+7] >> 3) & 0x03
        self.buffer[0] = self.buffer[0] | (((bx[0+7] & 7) << 5)  & 0xff)
        # Row2
        self.buffer[3] = (bx[1+7] >> 3) & 0x03
        self.buffer[2] = self.buffer[2] | (((bx[1+7] & 7) << 5)  & 0xff)    
        # Row3
        self.buffer[5] = (bx[2+7] >> 3) & 0x03
        self.buffer[4] = self.buffer[4] | (((bx[2+7] & 7) << 5)  & 0xff)
        # Row4
        self.buffer[7] = (bx[3+7] >> 3) & 0x03
        self.buffer[6] = self.buffer[6] | (((bx[3+7] & 7) << 5)  & 0xff)
        # Row5
        self.buffer[9] = (bx[4+7] >> 3)& 0x03
        self.buffer[8] = self.buffer[8] | (((bx[4+7] & 7) << 5)  & 0xff)
        # Row6
        self.buffer[11] = (bx[5+7] >> 3) & 0x03
        self.buffer[10] = self.buffer[10] | (((bx[5+7] & 7) << 5)  & 0xff)
        # Row7
        self.buffer[13] = (bx[6+7] >> 3) & 0x03
        self.buffer[12] = self.buffer[12] | (((bx[6+7] & 7) << 5)  & 0xff)


        # Place 1
        self.buffer[1] = self.buffer[1] | (bx[0+14] & 0xff) << 2
        self.buffer[3] = self.buffer[3] | (bx[1+14] & 0xff) << 2
        self.buffer[5] = self.buffer[5] | (bx[2+14] & 0xff) << 2
        self.buffer[7] = self.buffer[7] | (bx[3+14] & 0xff) << 2
        self.buffer[9] = self.buffer[9] | (bx[4+14] & 0xff) << 2
        self.buffer[11] = self.buffer[11] | (bx[5+14] & 0xff) << 2
        self.buffer[13] = self.buffer[13] | (bx[6+14] & 0xff) << 2
        self.buffer[15] = self.buffer[15] | (bx[6+14] & 0xff) << 2

        # Write data 
        self.bus.write_i2c_block_data(self.ht16k33_i2c_address, 0x00, self.buffer)

    def write_data(self, a, b, c, show_decimals=False, decimal_dots=0x00):  
        bx = []
        ax = self.rotate_90(a)
        kx = self.rotate_90(b)
        cx = self.rotate_90(c)
        
        # Push data to common raw buffer 
        for e in ax:
            bx.append(e)
        for e in kx:
            bx.append(e)
        for e in cx:
            bx.append(e)

        # Distribute data between lines 
        # The same as function from above 
        # Rewrite in later revisions to 1 function  
        # Display module 3
        self.buffer[0] = bx[0] & 0x1f
        self.buffer[2] = bx[1] & 0x1f
        self.buffer[4] = bx[2] & 0x1f
        self.buffer[6] = bx[3] & 0x1f
        self.buffer[8] = bx[4] & 0x1f 
        self.buffer[10] = bx[5] & 0x1f  
        self.buffer[12] = bx[6] & 0x1f
        self.buffer[14] = 0x00
    
        #Display module 2 
        self.buffer[1] = (bx[0+7] >> 3) & 0x03
        self.buffer[0] = self.buffer[0] | (((bx[0+7] & 7) << 5)  & 0xff)

        self.buffer[3] = (bx[1+7] >> 3) & 0x03
        self.buffer[2] = self.buffer[2] | (((bx[1+7] & 7) << 5)  & 0xff)    

        self.buffer[5] = (bx[2+7] >> 3) & 0x03
        self.buffer[4] = self.buffer[4] | (((bx[2+7] & 7) << 5)  & 0xff)

        self.buffer[7] = (bx[3+7] >> 3) & 0x03
        self.buffer[6] = self.buffer[6] | (((bx[3+7] & 7) << 5)  & 0xff)

        self.buffer[9] = (bx[4+7] >> 3)& 0x03
        self.buffer[8] = self.buffer[8] | (((bx[4+7] & 7) << 5)  & 0xff)

        self.buffer[11] = (bx[5+7] >> 3) & 0x03
        self.buffer[10] = self.buffer[10] | (((bx[5+7] & 7) << 5)  & 0xff)

        self.buffer[13] = (bx[6+7] >> 3) & 0x03
        self.buffer[12] = self.buffer[12] | (((bx[6+7] & 7) << 5)  & 0xff)


        # Display module 1
        self.buffer[1] = self.buffer[1] | (bx[0+14] & 0xff) << 2
        self.buffer[3] = self.buffer[3] | (bx[1+14] & 0xff) << 2
        self.buffer[5] = self.buffer[5] | (bx[2+14] & 0xff) << 2
        self.buffer[7] = self.buffer[7] | (bx[3+14] & 0xff) << 2
        self.buffer[9] = self.buffer[9] | (bx[4+14] & 0xff) << 2
        self.buffer[11] = self.buffer[11] | (bx[5+14] & 0xff) << 2
        self.buffer[13] = self.buffer[13] | (bx[6+14] & 0xff) << 2
        # Copy the same data in row8 as in row7 used to commute anode 15 between 2 display modules
        # The same colum  is distributed between Display module 1 and display module 2 on different catode signal  
        self.buffer[15] = self.buffer[15] | (bx[6+14] & 0xff) << 2

        #place decimal dot 
        if show_decimals:

            # Put dot on first display module for led driver 2
            self.buffer[15] = self.buffer[15] | (decimal_dots & 0b00000100) << 5
            # Put dot on second display module for led driver 2
            self.buffer[13] = self.buffer[13] | (decimal_dots & 0b00000010) << 6

            # Put dot on third display module for led driver 1
            self.buffer[13] = self.buffer[13] | (decimal_dots & 0b00001000) << 4



        #write data 
        self.bus.write_i2c_block_data(self.ht16k33_i2c_address, 0x00, self.buffer)


class Pitanga():

    def __init__(self):
        # Initialise drivers 
        self.led_driver_1 = HT16K33(ht16k33_i2c_address=HT16K33_ADDRESS_1)
        self.led_driver_1.clear()
        self.led_driver_0 = HT16K33(ht16k33_i2c_address=HT16K33_ADDRESS_0)
        self.led_driver_0.clear()


    # Display string 6 char
    def display_print(self, font, str_data, show_decimals=False, decimal_dots=0x00):
        #Clear buffer 
        self.led_driver_1.clear()
        self.led_driver_0.clear()

        font_first_char = 0x20

        #Write data  led driver 1
        self.led_driver_1.write_data(
            font[ord(str_data[5])- font_first_char],
            font[ord(str_data[4])- font_first_char],
            font[ord(str_data[3])- font_first_char],
            show_decimals=show_decimals,
            decimal_dots = decimal_dots & 0b00000110
        )
        
        # Write data  led driver 0 
        ch = [x for x in font[ord(str_data[1])- font_first_char]] #Create separate array 
        # Work around for mistake in schematic connection on ds2
        j = ch[3]
        ch[3] = ch[4]
        ch[4] = j
        self.led_driver_0.write_data(
            font[ord(str_data[2])- font_first_char],
            ch,
            font[ord(str_data[0])- font_first_char],
            show_decimals=show_decimals,
            decimal_dots = decimal_dots  & 0b00011000
            )


    def display_bitmap(self, bitmap):
        # Slice 7 lines hight 
        bitmap_slice = bitmap[:7]
        
        # Display data from 6 to 1
        led_display_data = []
        for x in range(0, 30, 5):
            # Start from first line to the end 
            char = []
            for line in bitmap_slice:               
                char_line = line[:-x] if x > 0 else line
                char_line = char_line[25-x:]
                char.append(int("".join(str(x) for x in char_line), 2))
            led_display_data.append(char)

        
        self.led_driver_1.clear()
        self.led_driver_0.clear()
        self.led_driver_1.write_data_raw(
            led_display_data[0],
            led_display_data[1],
            led_display_data[2]
        )
        self.led_driver_0.write_data_raw(
            led_display_data[3],
            led_display_data[4],
            led_display_data[5]
        )

display_string = "Motanas si Pisicuta ) "
pikachu_d = pikachu_bitmap
display_menu = 3

# Keys variable replace array with a integer value
keys = 0b0000
pitanga  = Pitanga()
decimal_dots = 0b00001010
# Dots  will alternate between values
decimal_dots_time_patterns = [0b00001010, 0b00000000]

def circular_left_rotate(num, shift, num_bits=8):
    shift %= num_bits
    return ((num << shift) | (num >> (num_bits - shift))) & ((1 << num_bits) - 1)

while True:
    
    current_time = datetime.now().strftime("%H%M%S")
    # Display_string = display_string 
 
    value = 1 if pitanga.led_driver_1.read_key_data() == 16 else 0
    # Prepare key data code uses bitwise operations for reasons of use the minimal memory possible 
    # and keep it easy portable to mcu 
    # Shift bits to the left of an integer instead of using separate element of an array to store button value 

    keys = keys << 1
    # Bit insert position 0 indicates to insert value in the lsb place 
    bit_insert_position = 0 
    mask = 1 << bit_insert_position
    keys = (keys & ~mask) | ((value << bit_insert_position) & mask)
    #apply 4 bit mask but 2 bit are sufficient do detect rising edge 
    keys = keys & 0x0f 

    # Toggle state only if previously button state was 0
    # Meaning button was released 
    # check bit position 0 and 1 of integer value, detecting rising edge condition 
    if keys & 0b00000001 == 1 and keys & 0b00000010 == 0:
         display_menu = display_menu + 1
         # Simple menu state machine flag 
         if display_menu == 5:
             display_menu = 0 

    
    
    if display_menu == 0:
        # Show time 
        # Circular rotate decimals pattern 
        decimal_dots_time_patterns =  decimal_dots_time_patterns[1:] + decimal_dots_time_patterns[:1]
        pitanga.display_print(Font5x7, current_time[:6], show_decimals=True, decimal_dots=decimal_dots_time_patterns[0])
        time.sleep(0.12)
 
    if display_menu == 1:
        # Show bitmap 
        # display_print(Font5x7, display_string[:6])
        pikachu_d = pikachu_d[1:] + pikachu_d[:1]
        pitanga.display_bitmap(pikachu_d)
        time.sleep(0.12)

    if display_menu == 2:
        # Show text 
        display_string = display_string[1:] + display_string[:1]
        pitanga.display_print(Font5x7, display_string[:6], show_decimals=False)
        time.sleep(0.12)
 
    if display_menu == 3:
        # Show running dots 
        decimal_dots = circular_left_rotate(decimal_dots, 1, 8)
        pitanga.display_print(Font5x7, '      ', show_decimals=True, decimal_dots=decimal_dots)
        time.sleep(0.045)
    
    if display_menu == 4:
        bluetooth_bitmap = bluetooth_bitmap[1:] + bluetooth_bitmap[:1]
        pitanga.display_bitmap(bluetooth_bitmap)
        time.sleep(0.1)
