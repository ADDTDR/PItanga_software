from smbus2 import SMBus
import time 

bus = SMBus(0)

DEV_ADDRESS = 0x4b

#	  HAL_I2C_Mem_Read(&hi2c1, DS1631Z_I2C_ADDR, 0xAC, 1,  ds_config, 1, 100 );
#
#	  HAL_I2C_Mem_Write(&hi2c1, DS1631Z_I2C_ADDR, 0x51, 1, ds_config, 0, 100);
#	  HAL_I2C_Mem_Write(&hi2c1, DS1631Z_I2C_ADDR, 0x22, 1, ds_config, 0, 100);
#
#	  uint8_t ds_temp[2];
#	  HAL_I2C_Mem_Read(&hi2c1, DS1631Z_I2C_ADDR, 0xAA, 1,  ds_temp, 2, 100 );
#
#//	  ds_temp[0] & 0xff
#//      float ds_temp_c = (ds_temp[0] & 0xff) + (ds_temp[1] >> 4) * 0.0625;
#	  uint8_t t_msb = ds_temp[0] & 0xff;
#	  if (t_msb >= 0x80)
#		  t_msb = t_msb - 255;
#
#	  ssd1306_SetCursor(0, 18);
#	  sprintf(str, "dsT:%d.%d", (t_msb), (ds_temp[1] >> 4) * 625  );

while True:
	config = bus.read_byte_data(DEV_ADDRESS, 0xAC)
	bus.write_byte_data(DEV_ADDRESS, 0x51, config )
	bus.write_byte_data(DEV_ADDRESS, 0x22, config )
	raw_temp = bus.read_i2c_block_data(DEV_ADDRESS, 0xAA, 2)
	print('raw temperature data {}'.format(raw_temp))
	tmsb=raw_temp[0] - 0xff if raw_temp[0] >= 0x80 else raw_temp[0]
	temp=raw_temp[0] + (raw_temp[1] >> 4) * 0.0625
	print('temperature {}'.format(temp))
	time.sleep(1)
