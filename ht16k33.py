from smbus import SMBus
import time
import random 
import os
from font5x7 import Font5x7_90 as Font5x7
from datetime import datetime
from pikachu import pikachu as pikachu_bitmap
from ds1631 import Ds1631
import random 
#from tinynumberhat import TinynumberHat
from serial_reader import GpsSerialReader
import threading 

GMT = 1
HT16K33_ADDRESS_0 = 0x70
HT16K33_ADDRESS_1 = 0x71


HT16K33_CMD_BRIGHTNESS = 0xE0
HT16K33_ENABLE_DISPLAY = 0x81
HT16K33_TURN_ON_OSCILLATOR = 0x21
LED_DRIVER_BRIGHTNESS_LEVEL = 5
JOKES_FILE = 'jokes.txt'
# tinynumberhat = TinynumberHat()
# t = threading.Thread(name='tinynumberhat', target=tinynumberhat.shoe_time)
# t.start()
try:
    gps_serial_reader = GpsSerialReader()
    gps_time_thread = threading.Thread(name='gps_serial_reader', target=gps_serial_reader.read_serial_gps_device)
    gps_time_thread.start()
except:
    print('No gps clock')

class HT16K33():

    def __init__(self, ht16k33_i2c_address):
        bus = SMBus(1)
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

        self.key_a = 0b0000
        self.key_b = 0b0000
        self.key_c = 0b0000
        self.key_d = 0b0000

    def set_brightness(self, brightness):
        self.bus.write_byte(self.ht16k33_i2c_address, HT16K33_CMD_BRIGHTNESS | brightness)


    def clear(self):
        self.buffer = [ 0x00 for x in range(0, 16)]
        

    def read_key_data(self):

        # read all keys 
        key_data = self.bus.read_i2c_block_data(self.ht16k33_i2c_address, 0x40, 5)
        keys = key_data[4]

  
        key_a_press, key_b_press, key_c_press, key_d_press = False, False, False, False

        value = 1 if  keys & 0x10 == 16 else 0
        # Prepare key data code uses bitwise operations for reasons of use the minimal memory possible 
        # and keep it easy portable to mcu 
        # Shift bits to the left of an integer instead of using separate element of an array to store button value 
        self.key_a = self.key_a << 1
        # Bit insert position 0 indicates to insert value in the lsb place 
        bit_insert_position = 0 
        mask = 1 << bit_insert_position
        self.key_a = (self.key_a & ~mask) | ((value << bit_insert_position) & mask)
        #apply 4 bit mask but 2 bit are sufficient do detect rising edge 
        self.key_a = self.key_a & 0x0f 

        # Toggle state only if previously button state was 0
        # Meaning button was released 
        # check bit position 0 and 1 of integer value, detecting rising edge condition 
        if self.key_a & 0b00000001 == 1 and self.key_a & 0b00000010 == 0:
            key_a_press = True


        value = 1 if  keys & 0x20 == 0x20 else 0
        self.key_b = self.key_b << 1
        bit_insert_position = 0 
        mask = 1 << bit_insert_position
        self.key_b = (self.key_b & ~mask) | ((value << bit_insert_position) & mask)
        self.key_b = self.key_b & 0x0f 
        if self.key_b & 0b00000001 == 1 and self.key_b & 0b00000010 == 0:
            key_b_press = True
        
        value = 1 if  keys & 0x40 == 0x40 else 0
        self.key_c = self.key_c << 1
        bit_insert_position = 0 
        mask = 1 << bit_insert_position
        self.key_c = (self.key_c & ~mask) | ((value << bit_insert_position) & mask)
        self.key_c = self.key_c & 0x0f 
        if self.key_c & 0b00000001 == 1 and self.key_c & 0b00000010 == 0:
            key_c_press = True
        
        value = 1 if  keys & 0x80 == 0x80 else 0
        self.key_d = self.key_d << 1
        bit_insert_position = 0 
        mask = 1 << bit_insert_position
        self.key_d = (self.key_d & ~mask) | ((value << bit_insert_position) & mask)
        self.key_d = self.key_d & 0x0f 
        if self.key_d & 0b00000001 == 1 and self.key_d & 0b00000010 == 0:
            key_d_press = True


        return (key_a_press, key_b_press, key_c_press, key_d_press)


    def fill(self):
        self.buffer = [0xff for x in range(0, 16)]


    def update(self):
        self.bus.write_i2c_block_data(self.ht16k33_i2c_address, 0x00, self.buffer)
        

    def write_data_raw(self, a, b, c, show_decimals=False, decimal_dots=0x00):  
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
        self.buffer[14] = bx[6] & 0x1f
    
        # Place 2 
        # Row 1
        self.buffer[1] = (bx[0+7] >> 3) & 0x03
        self.buffer[0] = self.buffer[0] | (((bx[0+7] & 7) << 5)  & 0xff)
        # Row 2
        self.buffer[3] = (bx[1+7] >> 3) & 0x03
        self.buffer[2] = self.buffer[2] | (((bx[1+7] & 7) << 5)  & 0xff)    
        # Row 3
        self.buffer[5] = (bx[2+7] >> 3) & 0x03
        self.buffer[4] = self.buffer[4] | (((bx[2+7] & 7) << 5)  & 0xff)
        # Row 4
        self.buffer[7] = (bx[3+7] >> 3) & 0x03
        self.buffer[6] = self.buffer[6] | (((bx[3+7] & 7) << 5)  & 0xff)
        # Row 5
        self.buffer[9] = (bx[4+7] >> 3)& 0x03
        self.buffer[8] = self.buffer[8] | (((bx[4+7] & 7) << 5)  & 0xff)
        # Row 6
        self.buffer[11] = (bx[5+7] >> 3) & 0x03
        self.buffer[10] = self.buffer[10] | (((bx[5+7] & 7) << 5)  & 0xff)
        # Row 7
        self.buffer[13] = (bx[6+7] >> 3) & 0x03
        self.buffer[12] = self.buffer[12] | (((bx[6+7] & 7) << 5)  & 0xff)
        # Row 8
        self.buffer[15] = (bx[6+7] >> 3) & 0x03
        self.buffer[14] = self.buffer[14] | (((bx[6+7] & 7) << 5)  & 0xff)


        # Place 1
        # Row 1
        self.buffer[1] = self.buffer[1] | (bx[0+14] & 0xff) << 2
        # Row 2
        self.buffer[3] = self.buffer[3] | (bx[1+14] & 0xff) << 2
        # Row 3
        self.buffer[5] = self.buffer[5] | (bx[2+14] & 0xff) << 2
        # Row 4
        self.buffer[7] = self.buffer[7] | (bx[3+14] & 0xff) << 2
        # Row 5
        self.buffer[9] = self.buffer[9] | (bx[4+14] & 0xff) << 2
        # Row 6 
        self.buffer[11] = self.buffer[11] | (bx[5+14] & 0xff) << 2
        # Row 7
        self.buffer[13] = self.buffer[13] | (bx[6+14] & 0xff) << 2
        # Row 8
        # self.buffer[15] = self.buffer[15] | (1 & 0xff) << 2
        # self.buffer[15] = se

        # place decimal dot 
        if show_decimals:
            # Dot on display third display an14 & ca7
            # print('{0:08b}'.format(decimal_dots))
            # dot on ds 3
            self.buffer[15] = self.buffer[15] | (decimal_dots & 0b00000001) << 6
            # dot on ds 1
            self.buffer[13] = self.buffer[13] | (decimal_dots & 0b00000100) << 5
            # dot on ds 1
            self.buffer[15] = self.buffer[15] | (decimal_dots & 0b00000010) << 6
            


            # # Put dot on third display module for led driver 1
            # self.buffer[13] = self.buffer[13] | (decimal_dots & 0b00001000) << 4

        # Write data 
        self.bus.write_i2c_block_data(self.ht16k33_i2c_address, 0x00, self.buffer)



class Pitanga():

    def __init__(self):
        # Initialise drivers 
        self.led_driver_1 = HT16K33(ht16k33_i2c_address=HT16K33_ADDRESS_1)
        self.led_driver_1.clear()
        self.led_driver_0 = HT16K33(ht16k33_i2c_address=HT16K33_ADDRESS_0)
        self.led_driver_0.clear()
        self.brightness = LED_DRIVER_BRIGHTNESS_LEVEL

    def rotate_90(self, a):
        b = []
        for k in range(0, 7):           
            q = [(x & ( 1 << k ) ) >> k for x  in a]
            qi = 0
            for bit in q:    
                qi =  (qi << 1)  | bit
            b.append(qi)
        return b

    def reverse_bits(self, num):
        num_bits = 5
        reversed_num = 0
        for i in range(num_bits):
            reversed_num = reversed_num << 1
            reversed_num = reversed_num | (num & 1)
            num = num >> 1
        return reversed_num

    # Display string 6 char
    def display_print(self, font, str_data, show_decimals=False, decimal_dots=0x00, update_leds=True):

        font_first_char = 0x20
        bx = [0,0,0,0,0,0]
   
        bx[0] =  [ self.reverse_bits(y) for y in font[ord(str_data[5])- font_first_char][::-1] ]
        bx[1] =  [ self.reverse_bits(y) for y in font[ord(str_data[4])- font_first_char][::-1] ]
        bx[2] =  [ self.reverse_bits(y) for y in font[ord(str_data[3])- font_first_char][::-1] ]
        bx[3] =  [ self.reverse_bits(y) for y in font[ord(str_data[2])- font_first_char][::-1] ]
        bx[4] =  [ self.reverse_bits(y) for y in font[ord(str_data[1])- font_first_char][::-1] ]
        bx[5] =  [ self.reverse_bits(y) for y in font[ord(str_data[0])- font_first_char][::-1] ]
        
        


        if update_leds:
            #Clear buffer 
            self.led_driver_1.clear()
            self.led_driver_0.clear()
            #Write data  led driver 1
            self.led_driver_1.write_data_raw(bx[0], bx[1], bx[2], show_decimals, decimal_dots & 0b00000111)
            # Write data  led driver 0
            self.led_driver_0.write_data_raw(bx[3], bx[4], bx[5], show_decimals, (decimal_dots  & 0b00111000) >> 3)

        return []


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

    def set_brightness(self, brightness=5):
        self.led_driver_0.set_brightness(brightness=self.brightness)
        self.led_driver_1.set_brightness(brightness=self.brightness)

def main():

    #ds1631 = Ds1631()
    with open(JOKES_FILE, 'r') as file:
        # Read all the lines into a list
        lines = file.readlines()

    display_string = random.choice(lines)
    display_string = display_string.replace('\n', '')

    pikachu_d = pikachu_bitmap
    display_menu = 3
    counter = 0

    pitanga  = Pitanga()
    decimal_dots = 0b00000101
    # Dots  will alternate between values
    decimal_dots_time_patterns = [0b00001010, 0b00000000]

    running = 0

    def circular_left_rotate(num, shift, num_bits=8):
        shift %= num_bits
        return ((num << shift) | (num >> (num_bits - shift))) & ((1 << num_bits) - 1)

    while True:
        pitanga_keys = pitanga.led_driver_1.read_key_data()  


        if pitanga_keys[0]:
            display_menu = display_menu + 1
            # Simple menu state machine flag 
            if display_menu == 4:
                display_menu = 0 

        if pitanga_keys[1]:
            if pitanga.brightness < 15:
                pitanga.brightness = pitanga.brightness + 1
                pitanga.set_brightness()                
            pitanga.display_print(Font5x7, 'B={}   '.format(pitanga.brightness + 1), show_decimals=False, decimal_dots=0xf00)
            running = 10

        if pitanga_keys[2]:
            if pitanga.brightness > 0:
                pitanga.brightness = pitanga.brightness - 1
                pitanga.set_brightness()                
            pitanga.display_print(Font5x7, 'B={}   '.format(pitanga.brightness + 1), show_decimals=False, decimal_dots=0xf00)
            running = 10

        if pitanga_keys[3]:
            if display_menu >= 0:
                display_menu = display_menu - 1
                if display_menu == -1:
                    display_menu = 3 
                
    
        if running == 0:
            if display_menu == 0:
                gmt = GMT
                # current_time = datetime.now().strftime("%H%M%SS")
                gps_time = os.environ.get('GPS_CLOCK', '00:00:00')
                gps_time_parts  = gps_time.split(':')                
                
                current_time = '{0:02d}'.format( (int(gps_time_parts[0]) + gmt) % 24 ) + gps_time_parts[1] + gps_time_parts[2]
                # print('curent time', current_time)  
                # Circular rotate decimals pattern 
                decimal_dots_time_patterns =  decimal_dots_time_patterns[1:] + decimal_dots_time_patterns[:1]
                # Show time 
                pitanga.display_print(Font5x7, current_time[:6], show_decimals=True, decimal_dots=decimal_dots_time_patterns[0])
                time.sleep(0.12)
        
            if display_menu == 1:
                #if counter > 10:
                    #temperature = ds1631.read_sensor()
                #    temperature = str(random.randint(0, 100))
                #    temperature = 't=' + temperature + '  '
                #    pitanga.display_print(Font5x7, temperature[:6], show_decimals=False, decimal_dots=0xf00)
                #    counter = 0
                # # Show bitmap 
                # pikachu_d = pikachu_d[1:] + pikachu_d[:1]
                # pitanga.display_bitmap(pikachu_d)
                #counter = counter + 1
                decimal_dots = circular_left_rotate(decimal_dots, 1, 8)
                pitanga.display_print(Font5x7, '       ', show_decimals=True, decimal_dots=decimal_dots & 0b00111111)
                time.sleep(0.12)
      

            if display_menu == 2:
                # Show jockes text 
                display_string = display_string[1:] + display_string[:1]
                pitanga.display_print(Font5x7, display_string[:6], show_decimals=False)
                time.sleep(0.1)
                if counter > 180 and counter < 250:
                    display_string = '      '[:1] + display_string[1:] 
                elif counter == 260:
                    counter = 0
                    display_string = random.choice(lines)
                    display_string = display_string.replace('\n', '')
                counter = counter + 1

            if display_menu == 3:
                current_time = datetime.now().strftime(" %H%M ")
                current_time = current_time[::-1]               
                # Show time 
                # Show running dots 
                decimal_dots = circular_left_rotate(decimal_dots, 1, 8)
                # decimal_dots = 0b00000011
                pitanga.display_print(Font5x7, current_time, show_decimals=True, decimal_dots=decimal_dots & 0b0000100)
                time.sleep(0.12)
        else:
            if running > 0:
                running = running -1
                time.sleep(0.08)

if __name__ == '__main__':
    main()
