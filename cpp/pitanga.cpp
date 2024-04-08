#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include "pickachu.h"
#include <linux/i2c-dev.h>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <bitset>
#include <iterator> 

#define HT16K33_ADDRESS_0 0x72
#define HT16K33_ADDRESS_1 0x73
#define HT16K33_TURN_ON_OSCILLATOR 0x21
#define HT16K33_ENABLE_DISPLAY 0x81
#define HT16K33_CMD_BRIGHTNESS 0xE0
#define LED_DRIVER_BRIGHTNESS_LEVEL 0x05
void circularRotateVertical(uint8_t arr[][30], int numRows, int numCols);

void circularRotateVertical(uint8_t (*arr)[30], int numRows, int numCols) {
    uint8_t temp[numCols];
    // Store the last row to temporary array
    for (int i = 0; i < numCols; ++i) {
        temp[i] = arr[numRows - 1][i];
    }
    // Shift all rows up by one position
    for (int i = numRows - 1; i > 0; --i) {
        for (int j = 0; j < numCols; ++j) {
            arr[i][j] = arr[i - 1][j];
        }
    }
    // Place the temporary array in the first row
    for (int i = 0; i < numCols; ++i) {
        arr[0][i] = temp[i];
    }
}

const int ROWS = 30;
const int COLS = 30;

void generateRandomMatrix(uint8_t matrix[][COLS]) {
    for (int i = 0; i < ROWS; ++i) {
        for (int j = 0; j < COLS; ++j) {
            matrix[i][j] = rand() % 2; // Generates 0 or 1 randomly
        }
    }
}

int main() {
    const char *device = "/dev/i2c-1"; // I2C bus device path
    int fd = open(device, O_RDWR);
    int fd2 = open(device, O_RDWR);
    if (fd < 0) {
        std::cerr << "Error: Unable to open I2C device." << std::endl;
        return 1;
    }

    // Set up the first HT16K33 LED driver
    if (ioctl(fd, I2C_SLAVE, HT16K33_ADDRESS_0) < 0) {
        std::cerr << "Error: Unable to set I2C slave address for device 0." << std::endl;
        close(fd);
        return 1;
    }

    // Turn on oscillator
    unsigned char cmd[2] = {HT16K33_TURN_ON_OSCILLATOR, 0x00};
    if (write(fd, cmd, sizeof(cmd)) != sizeof(cmd)) {
        std::cerr << "Error: Unable to turn on oscillator for device 0." << std::endl;
        close(fd);
        return 1;
    }

    // Enable display
    cmd[0] = HT16K33_ENABLE_DISPLAY;
    if (write(fd, cmd, sizeof(cmd)) != sizeof(cmd)) {
        std::cerr << "Error: Unable to enable display for device 0." << std::endl;
        close(fd);
        return 1;
    }

    // Set brightness
    cmd[0] = HT16K33_CMD_BRIGHTNESS | LED_DRIVER_BRIGHTNESS_LEVEL;
    if (write(fd, cmd, sizeof(cmd)) != sizeof(cmd)) {
        std::cerr << "Error: Unable to set brightness for device 0." << std::endl;
        close(fd);
        return 1;
    }

    // Set up the second HT16K33 LED driver
    if (ioctl(fd2, I2C_SLAVE, HT16K33_ADDRESS_1) < 0) {
        std::cerr << "Error: Unable to set I2C slave address for device 1." << std::endl;
        close(fd);
        return 1;
    }

    // Turn on oscillator for device 1
    cmd[0] = HT16K33_TURN_ON_OSCILLATOR;
    if (write(fd2, cmd, sizeof(cmd)) != sizeof(cmd)) {
        std::cerr << "Error: Unable to turn on oscillator for device 1." << std::endl;
        close(fd);
        return 1;
    }

    // Enable display for device 1
    cmd[0] = HT16K33_ENABLE_DISPLAY;
    if (write(fd2, cmd, sizeof(cmd)) != sizeof(cmd)) {
        std::cerr << "Error: Unable to enable display for device 1." << std::endl;
        close(fd);
        return 1;
    }

    // Set brightness for device 1
    cmd[0] = HT16K33_CMD_BRIGHTNESS | LED_DRIVER_BRIGHTNESS_LEVEL;
    if (write(fd2, cmd, sizeof(cmd)) != sizeof(cmd)) {
        std::cerr << "Error: Unable to set brightness for device 1." << std::endl;
        close(fd);
        return 1;
    }

    std::cout << "Hello, World!" << std::endl;
	/*for (auto & i : pikachu) {
        for (int j = 0; j < 30; ++j) {
            std::cout << i[j];
        }
    std::cout <<  std::endl;
    }*/

    std::cout << '\n' << '\n' << '\n';
    uint8_t  buffer[16] = {0};
    uint8_t  buffer2[16] = {0};

    uint8_t pikachu[ROWS][COLS];
    generateRandomMatrix(pikachu);
    // Generate random data and write to both LED drivers
    srand(time(NULL));
    int start_line = 0;
    while (true) {
   
    circularRotateVertical(pikachu, 30, 30);

    int buffer_index = 0;
    for (int line  = start_line; line  < start_line + 7; line ++ ) {
	// 0x01 << 7 for dot #6    
	buffer2[buffer_index + 1] = pikachu[line][0] << 6 | pikachu[line][1] << 5 | pikachu[line][2] << 4 | pikachu[line][3] << 3 | pikachu[line][4] << 2 | pikachu[line][5] << 1 | pikachu[line][6];
	buffer2[buffer_index] = pikachu[line][7] << 7 |  pikachu[line][8] << 6 | pikachu[line][9] << 5 | pikachu[line][10] << 4 | pikachu[line][11] << 3 | pikachu[line][12] << 2 | pikachu[line][13] << 1 | pikachu[line][14];

	buffer[buffer_index] = pikachu[line][29] | pikachu[line][28] << 1 | pikachu[line][27] << 2 | pikachu[line][26] << 3 | pikachu[line][25] << 4 | pikachu[line][24] << 5 | pikachu[line][23] << 6 | pikachu[line][22] << 7;
	
	buffer[buffer_index + 1] = pikachu[line][21] | pikachu[line][20] << 1 | pikachu[line][19] << 2 | pikachu[line][18] << 3 | pikachu[line][17] << 4 | pikachu[line][16] << 5 | pikachu[line][15] << 6;

        buffer_index = buffer_index + 2;
    }
    

        std::vector<unsigned char> data(16);
        for (int j = 0; j < 16; ++j) {
            data[j] = buffer2[j];
        }

        // Write data to the first LED driver
        for (int j = 0; j < 16; ++j) {
            unsigned char reg_addr = j;
            cmd[0] = reg_addr;
            cmd[1] = data[j];
            if (write(fd, cmd, sizeof(cmd)) != sizeof(cmd)) {
                std::cerr << "Error: Unable to write data to device 0." << std::endl;
                close(fd);
                return 1;
            }
        }

        // Generate new random data for the second LED driver
        for (int j = 0; j < 16; ++j) {
            data[j] = buffer[j];
        }

        // Write data to the second LED driver
        for (int j = 0; j < 16; ++j) {
            unsigned char reg_addr = j;
            cmd[0] = reg_addr;
            cmd[1] = data[j];
            if (write(fd2, cmd, sizeof(cmd)) != sizeof(cmd)) {
                std::cerr << "Error: Unable to write data to device 1." << std::endl;
                close(fd2);
                return 1;
            }
        }
        usleep(102000);
    }

    close(fd);
    close(fd2);

    return 0;
}

