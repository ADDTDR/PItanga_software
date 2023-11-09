from smbus import SMBus
import time 

DEV_ADDRESS = 0x4b

class Ds1631():
	def __init__(self) -> None:
		self.bus =  SMBus(2)
		self.data = []

	
	def read_sensor(self):
		config = self.bus.read_byte_data(DEV_ADDRESS, 0xAC)
		self.bus.write_byte_data(DEV_ADDRESS, 0x51, config )
		self.bus.write_byte_data(DEV_ADDRESS, 0x22, config )
	
		raw_temp = self.bus.read_i2c_block_data(DEV_ADDRESS, 0xAA, 2)
		# print('raw temperature data {}'.format(raw_temp))
		# tmsb=raw_temp[0] - 0xff if raw_temp[0] >= 0x80 else raw_temp[0]
		temp=raw_temp[0] + (raw_temp[1] >> 4) * 0.0625
		self.data.append(round( temp, 1 ))
		self.data = self.data[-10:]
		return '{:.1f}'.format( round( sum(self.data) / len(self.data) , 1) )


if __name__ == '__main__':
	ds1631 = Ds1631()
	while True:
		print(ds1631.read_sensor())
		time.sleep(1.0)
