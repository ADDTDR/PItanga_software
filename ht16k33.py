from smbus import SMBus
import time
from font5x7 import Font5x7_full as Font5x7
from datetime import datetime

HT16K33_ADDRESS_1 = 0x71
HT16K33_ADDRESS_0 = 0x70
HT16K33_CMD_BRIGHTNESS = 0xE0


class HT16K33():

    def __init__(self, ht16k33_i2c_address):
        bus = SMBus(2)
        #turn on oscilator 
        bus.write_byte(ht16k33_i2c_address, 0x21)
        #enable display (no blinking mode)
        bus.write_byte(ht16k33_i2c_address, 0x81)
        #clear dispay 
        bus.write_i2c_block_data(ht16k33_i2c_address, 0x00, [0x00] * 16)
        #set brightness 0-15
        bus.write_byte(ht16k33_i2c_address, HT16K33_CMD_BRIGHTNESS | 15)
        self.ht16k33_i2c_address = ht16k33_i2c_address
        self.bus = bus
        self.buffer = [0x00 for x in range(0, 16)]

    def rotate_90(self, a):
        b = []
        for k in range(0, 7):
            #q = [(a[0] & (1 << k)) >> k , (a[1] & (1 << k)) >> k , (a[2] & (1 << k)) >> k,  (a[3] & (1 << k)) >> k,  (a[4] & (1 << k)) >> k]	
            q = [(x & (1 << k)) >> k for x in a ]
            qi = 0
            for bit in q:    
                qi = (qi << 1) | bit
            b.append(qi)
        return b

    def clear(self):
        self.buffer = [ 0x00 for x in range(0, 16)]
        #self.bus.write_i2c_block_data(self.ht16k33_i2c_address, 0x00, self.buffer)

    def write_data(self, a, b, c):  
        bx = []
        ax = self.rotate_90(a)
        #ax = self.rotate_90(ax)
        #ax = self.rotate_90(ax)
        #ax = self.rotate_90(ax)
       	#ax = self.rotate_90(ax)

        kx = self.rotate_90(b)
        cx = self.rotate_90(c)
        
        #push data to common raw buffer 
        for e in ax:
            bx.append(e)
        for e in kx:
            bx.append(e)
        for e in cx:
            bx.append(e)

        #Distribute data between lines 
        #place 3 
        self.buffer[0] = bx[0] & 0x1f
        self.buffer[2] = bx[1] & 0x1f
        self.buffer[4] = bx[2] & 0x1f
        self.buffer[6] = bx[3] & 0x1f
        self.buffer[8] = bx[4] & 0x1f 
        self.buffer[10] = bx[5] & 0x1f  
        self.buffer[12] = bx[6] & 0x1f
        self.buffer[14] = 0xff & 0x00 
    
        #place 2 
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


        #place 1
        self.buffer[1] = self.buffer[1] | (bx[0+14] & 0xff) << 2
        self.buffer[3] = self.buffer[3] | (bx[1+14] & 0xff) << 2
        self.buffer[5] = self.buffer[5] | (bx[2+14] & 0xff) << 2
        self.buffer[7] = self.buffer[7] | (bx[3+14] & 0xff) << 2
        self.buffer[9] = self.buffer[9] | (bx[4+14] & 0xff) << 2
        self.buffer[11] = self.buffer[11] | (bx[5+14] & 0xff) << 2
        self.buffer[13] = self.buffer[13] | (bx[6+14] & 0xff) << 2
        self.buffer[15] = 0x00

        #write data 
        self.bus.write_i2c_block_data(self.ht16k33_i2c_address, 0x00, self.buffer)



#Initialise drivers 
ht_1 = HT16K33(ht16k33_i2c_address=HT16K33_ADDRESS_1)
ht_1.clear()

ht_0 = HT16K33(ht16k33_i2c_address=HT16K33_ADDRESS_0)
ht_0.clear()


#display string
def display_print(font, str_data):
    #Clear buffer 
    ht_1.clear()
    ht_0.clear()
    font_first_char = 0x20

    #Write data  led driver 
    ht_1.write_data(
        font[ord(str_data[5])- font_first_char],
        font[ord(str_data[4])- font_first_char],
        font[ord(str_data[3])- font_first_char]
    )
    #Write data  led driver
    #Workaraund for mistake in shematic connection on ds2 
    ch = [x for x in font[ord(str_data[1])- font_first_char]] #Create separate array 
    j = ch[3]
    ch[3] = ch[4]
    ch[4] = j
    ht_0.write_data(
        font[ord(str_data[2])- font_first_char],
        ch,
        font[ord(str_data[0])- font_first_char]
        )

    
display_string = "Andruselu "
while True:
    current_time = datetime.now().strftime("%H:%M:%S")
    display_string = display_string 

    display_string = display_string[1:] + display_string[:1]
    # current_time = "Andrus"
    display_print(Font5x7, display_string[:6])
    #display update rate
    time.sleep(0.2)


