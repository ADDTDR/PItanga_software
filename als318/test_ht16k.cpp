#include <iostream>
#include <wiringPiI2C.h>
#include <unistd.h>
#include <vector>
#include <cstdlib>
#include <ctime>

#define HT16K33_ADDRESS_0 0x70
#define HT16K33_ADDRESS_1 0x71
#define HT16K33_TURN_ON_OSCILLATOR 0x21
#define HT16K33_ENABLE_DISPLAY 0x81
#define HT16K33_CMD_BRIGHTNESS 0xE0
#define LED_DRIVER_BRIGHTNESS_LEVEL 0x0A
#define SMBUS 1

int main() {
   int fd = wiringPiI2CSetup(HT16K33_ADDRESS_0);
   int fd2 = wiringPiI2CSetup(HT16K33_ADDRESS_1);

   if ((fd == -1) ||(fd2 == -1)){
        std::cerr << "Error: Unable to open I2C device." << std::endl;
        return 1;
    }
   wiringPiI2CWriteReg8(fd,   HT16K33_TURN_ON_OSCILLATOR, 0x00);
   wiringPiI2CWriteReg8(fd, HT16K33_ENABLE_DISPLAY, 0x00);
   wiringPiI2CWriteReg8(fd2,   HT16K33_TURN_ON_OSCILLATOR, 0x00);
   wiringPiI2CWriteReg8(fd2, HT16K33_ENABLE_DISPLAY, 0x00);
    for (int i = 0; i < 16; ++i) {
        wiringPiI2CWriteReg8(fd, 0x00 + i, 0xff);
    }
    wiringPiI2CWriteReg8(fd,   HT16K33_CMD_BRIGHTNESS | LED_DRIVER_BRIGHTNESS_LEVEL, 0x00);
    wiringPiI2CWriteReg8(fd2,   HT16K33_CMD_BRIGHTNESS | LED_DRIVER_BRIGHTNESS_LEVEL, 0x00);

    srand(time(NULL));
    while (true)  {
        std::vector<int> data(16);
        for (int j = 0; j < 16; ++j) {
            data[j] = rand() % 256;
        }
       
        for (int j = 0; j < 16; ++j) {
	wiringPiI2CWriteReg8(fd, 0x00 + j, data[j]);

 	for (int j = 0; j < 16; ++j) {
            data[j] = rand() % 256;
        }

	wiringPiI2CWriteReg8(fd2, 0x00 + j, data[j]);
        }
        usleep(102000);
    } 
    return 0;
}
