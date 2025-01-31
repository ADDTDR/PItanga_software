import smbus
import time 

VEML7700_ADDRESS = 0x10
INTEGRATION_TIME_MS = 100

bus = smbus.SMBus(1)

# https://github.com/palouf34/veml7700/blob/master/veml7700.py
def configure_sensor():
    # Set integration time (bits 11:6) and enable the sensor (bit 0)
    # config_data = (INTEGRATION_TIME_MS << 6) | 0x01
    bus.write_i2c_block_data(VEML7700_ADDRESS, 0x00, [0x00, 0x1b])

def read_light_sensor():
    # Start measurement 
    # bus.write_byte_data(VEML7700_ADDRESS, 0x00, 0x03)

    # time.sleep(INTEGRATION_TIME_MS / 1000.0)

    data = bus.read_i2c_block_data(VEML7700_ADDRESS, 0x04, 2)
    print(data)

    raw_data = (data[1] << 8 | data[0])
    return raw_data

def main():
    configure_sensor()
    while True:
        light_data = read_light_sensor()

        print(f"Raw Light Data : {light_data}")

        time.sleep(1)


if __name__ == "__main__":
    main()
