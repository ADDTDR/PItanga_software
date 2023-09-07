from smbus2 import SMBus
import time
from font5x7 import Font5x7
from datetime import datetime

HT16K33_ADDRESS_1 = 0x71
HT16K33_ADDRESS_0 = 0x70
HT16K33_CMD_BRIGHTNESS = 0xE0


class HT16K33():

    def __init__(self, ht16k33_i2c_address):

        bus = SMBus(0)
        #turn on oscilator 
        bus.write_byte(ht16k33_i2c_address, 0x21)
        #enable display (no blinking mode)
        bus.write_byte(ht16k33_i2c_address, 0x81)
        #clear dispay 
        bus.write_i2c_block_data(ht16k33_i2c_address, 0x00, [0x00] * 16)
        #set brightness 0-15
        bus.write_byte(ht16k33_i2c_address, HT16K33_CMD_BRIGHTNESS | 5)
        self.ht16k33_i2c_address = ht16k33_i2c_address
        self.bus = bus
        self.buffer = [0x00 for x in range(0, 16)]

    def rotate_90(self, a):
        b = []
        for k in range(0, 7):
            q = [(a[0] & (1 << k)) >> k , (a[1] & (1 << k)) >> k , (a[2] & (1 << k)) >> k,  (a[3] & (1 << k)) >> k,  (a[4] & (1 << k)) >> k]
            qi = 0
            for bit in q:    
                qi = (qi << 1) | bit
            b.append(qi)
        return b

    def clear(self):
        self.buffer = [ 0x00 for x in range(0, 16)]
        self.bus.write_i2c_block_data(self.ht16k33_i2c_address, 0x00, self.buffer)

    def write_number(self, a, b, c):  
        bx = []
        ax = self.rotate_90(a)
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




ht_1 = HT16K33(ht16k33_i2c_address=HT16K33_ADDRESS_1)
ht_1.clear()

ht_0 = HT16K33(ht16k33_i2c_address=HT16K33_ADDRESS_0)
ht_0.clear()


while True:
    for i in range(0 , 10 -3):
        current_time = datetime.now().strftime("%H%M%S")
        #bus.write_byte(HT16K33_ADDRESS, HT16K33_CMD_BRIGHTNESS | i)
        ht_1.write_number(Font5x7[int(current_time[5])], Font5x7[int(current_time[4])], Font5x7[int(current_time[3])])

        #Workaraund for mistake in shematic connection on ds2 
        ch = [x for x in Font5x7[int(current_time[1])]] #Create separate array 
        j = ch[3]
        ch[3] = ch[4]
        ch[4] = j
        ht_0.write_number(Font5x7[int(current_time[2])], ch, Font5x7[int(current_time[0])])

        time.sleep(1)
        ht_1.clear()
        ht_0.clear()

