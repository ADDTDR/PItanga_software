from smbus2 import SMBus
import time


Font5x7 =[
       [0x3E, 0x51, 0x49, 0x45, 0x3E], #0
       [0x00, 0x42, 0x7F, 0x40, 0x00], #1
       [0x42, 0x61, 0x51, 0x49, 0x46], #2
       [0x21, 0x41, 0x45, 0x4B, 0x31], #3
       [0x18, 0x14, 0x12, 0x7F, 0x10], #4
       [0x27, 0x45, 0x45, 0x45, 0x39], #5
       [0x3C, 0x4A, 0x49, 0x49, 0x30], #6
       [0x01, 0x71, 0x09, 0x05, 0x03], #7
       [0x36, 0x49, 0x49, 0x49, 0x36], #8
       [0x06, 0x49, 0x49, 0x29, 0x1E]] #9

bus = SMBus(0)
HT16K33_ADDRESS = 0x71

HT16K33_CMD_BRIGHTNESS = 0xE0

#turn on oscilator 
bus.write_byte(HT16K33_ADDRESS, 0x21)
#enable display (no blinking mode)
bus.write_byte(HT16K33_ADDRESS, 0x81)
#clear dispay 
bus.write_i2c_block_data(HT16K33_ADDRESS, 0x00, [0x00] * 16)
#set brightness 0-15
bus.write_byte(HT16K33_ADDRESS, HT16K33_CMD_BRIGHTNESS | 10)


buffer = [0x00 for x in range(0, 16)]


def clear():
    buffer = [ 0x00 for x in range(0, 16)]
    bus.write_i2c_block_data(HT16K33_ADDRESS, 0x00, buffer)


def rotate_90(a):
    b = []
    for k in range(0, 7):
        q = [(a[0] & (1 << k)) >> k , (a[1] & (1 << k)) >> k , (a[2] & (1 << k)) >> k,  (a[3] & (1 << k)) >> k,  (a[4] & (1 << k)) >> k]
        qi = 0
        for bit in q:    
            qi = (qi << 1) | bit
        b.append(qi)
    return b

def write_number(a, b, c):  
    bx = []
    ax = rotate_90(a)
    kx = rotate_90(b)
    cx = rotate_90(c)
    
    #push data to common raw buffer 
    for e in ax:
        bx.append(e)
    for e in kx:
        bx.append(e)
    for e in cx:
        bx.append(e)

    #Distribute data between lines 
    #place 3 
    buffer[0] = bx[0] & 0x1f
    buffer[2] = bx[1] & 0x1f
    buffer[4] = bx[2] & 0x1f
    buffer[6] = bx[3] & 0x1f
    buffer[8] = bx[4] & 0x1f 
    buffer[10] = bx[5] & 0x1f  
    buffer[12] = bx[6] & 0x1f
    buffer[14] = 0xff & 0x00 
   
    #place 2 
    buffer[1] = (bx[0+7] >> 3) & 0x03
    buffer[0] = buffer[0] | (((bx[0+7] & 7) << 5)  & 0xff)

    buffer[3] = (bx[1+7] >> 3) & 0x03
    buffer[2] = buffer[2] | (((bx[1+7] & 7) << 5)  & 0xff)    

    buffer[5] = (bx[2+7] >> 3) & 0x03
    buffer[4] = buffer[4] | (((bx[2+7] & 7) << 5)  & 0xff)

    buffer[7] = (bx[3+7] >> 3) & 0x03
    buffer[6] = buffer[6] | (((bx[3+7] & 7) << 5)  & 0xff)

    buffer[9] = (bx[4+7] >> 3)& 0x03
    buffer[8] = buffer[8] | (((bx[4+7] & 7) << 5)  & 0xff)

    buffer[11] = (bx[5+7] >> 3) & 0x03
    buffer[10] = buffer[10] | (((bx[5+7] & 7) << 5)  & 0xff)

    buffer[13] = (bx[6+7] >> 3) & 0x03
    buffer[12] = buffer[12] | (((bx[6+7] & 7) << 5)  & 0xff)


    #place 1
    buffer[1] = buffer[1] | (bx[0+14] & 0xff) << 2
    buffer[3] = buffer[3] | (bx[1+14] & 0xff) << 2
    buffer[5] = buffer[5] | (bx[2+14] & 0xff) << 2
    buffer[7] = buffer[7] | (bx[3+14] & 0xff) << 2
    buffer[9] = buffer[9] | (bx[4+14] & 0xff) << 2
    buffer[11] = buffer[11] | (bx[5+14] & 0xff) << 2
    buffer[13] = buffer[13] | (bx[6+14] & 0xff) << 2
    buffer[15] = 0x00

    #write data 
    bus.write_i2c_block_data(HT16K33_ADDRESS, 0x00, buffer)

clear()

while True:
    for i in range(0 , 10 -3):
        #bus.write_byte(HT16K33_ADDRESS, HT16K33_CMD_BRIGHTNESS | i)
        write_number(Font5x7[i], Font5x7[i+1], Font5x7[i+2])
        time.sleep(0.1)
        clear()


