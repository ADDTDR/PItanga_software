from smbus import SMBus

# Define the I2C bus number (0 or 1, depending on your Raspberry Pi)
i2c_bus = 2

# Define the I2C address of the LM75A sensor (default is 0x48)
lm75a_address = 0x48

# Create an SMBus object
bus = SMBus(i2c_bus)

# Read temperature data from the LM75A sensor
raw_temperature = bus.read_word_data(lm75a_address, 0)

# The LM75A returns temperature in a 16-bit signed value (two's complement)
# Convert the raw temperature data to Celsius
temperature = ((raw_temperature >> 8) + ((raw_temperature & 0xFF) << 8)) / 256.0

# Print the temperature
print(f"Temperature: {temperature} °C")

# Close the I2C bus
bus.close()
