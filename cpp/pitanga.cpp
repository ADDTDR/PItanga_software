#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <string>
#include <linux/i2c-dev.h>
#include <vector>
#include <ctime>
#include <iomanip>
#include <sstream>
#include "fonts.h" 

#define HT16K33_ADDRESS_0 0x70
#define HT16K33_ADDRESS_1 0x71
#define HT16K33_TURN_ON_OSCILLATOR 0x21
#define HT16K33_ENABLE_DISPLAY 0x81
#define HT16K33_CMD_BRIGHTNESS 0xE0
#define LED_DRIVER_BRIGHTNESS_LEVEL 0x0a

const int ROWS = 30;
const int COLS = 30;

const char *device = "/dev/i2c-1"; // I2C bus device path
int fd = open(device, O_RDWR);
int fd2 = open(device, O_RDWR);

void circularRotateVertical(uint8_t (*arr)[30], int numRows, int numCols, int stopCols) {
    uint8_t temp[numCols];
    // Store the last row to temporary array
    for (int i = stopCols; i < numCols; ++i) {
        temp[i] = arr[numRows - 1][i];
    }
    // Shift all rows up by one position
    for (int i = numRows - 1; i > 0; --i) {
        for (int j = stopCols; j < numCols; ++j) {
            arr[i][j] = arr[i - 1][j];
        }
    }
    // Place the temporary array in the first row
    for (int i = stopCols; i < numCols; ++i) {
        arr[0][i] = temp[i];
    }
}



//void generateRandomMatrix(uint8_t matrix[][COLS]) {
//    for (int i = 0; i < ROWS; ++i) {
//        for (int j = 0; j < COLS; ++j) {
//            matrix[i][j] = rand() % 2; // Generates 0 or 1 randomly
//        }
//    }
//}

//void displayMatrix(uint8_t frameBuffer[][COLS]) {
//    for (int i = 0; i < ROWS; ++i) {
//        for (int j = 0; j < COLS; ++j) {
//            std::cout << frameBuffer[i][j] << " ";
//        }
//        std::cout << std::endl;
//    }
//}

void numToBits(uint8_t num, bool bits[8]){
    for (int i = 0; i < 8; ++i) {
        bits[i] = (num >> i) & 1;
    }
}

std::string  getTime(){
    std::stringstream ss;
    std::time_t currentTime = std::time(nullptr);
    std::tm *localTime = std::localtime(&currentTime);
    ss << std::setw(2) << std::setfill('0') << localTime->tm_hour
    << std::setw(2) << std::setfill('0') << localTime->tm_min
    << std::setw(2) << std::setfill('0') << localTime->tm_sec;
    return ss.str();
}

int  init_pitanga(){

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
    return 0;
}

int main() {
    init_pitanga();
    std::cout << "Running Demo" << std::endl;

    unsigned char cmd[2];
    std::cout << '\n' << '\n' << '\n';
    uint8_t  buffer[16] = {0};
    uint8_t  buffer2[16] = {0};

    uint8_t frameBuffer[ROWS][COLS] = {0x00};
    // generateRandomMatrix(frameBuffer);
    // Generate random data and write to both LED drivers
//    srand(time(nullptr));

    int x_offset = 0;
    int y_offset = 0;

    uint8_t dots = 0b00000001;	
    uint8_t mode_counter = 0; 


    while (true) {
     int start_line = 0;

     
    
    if (mode_counter == 8 ){	

        for (int j = 0; j < COLS; j++) {
        }
    }*/   
   std::string str = getTime();
        for(char e : str){
                // Render char
                int x  = 0;
                bool bits [8][8] = {0};
                for(auto  & a: Font5x7_full[e-0x20]){
                    numToBits(a, bits[x]);
                    x++;
                }
                    // Copy
                    // Wrap to function

                    for (int i = 0; i < 5; ++i) {
                        for (int j = 0; j < 7; ++j) {				
                     		frameBuffer[j + y_offset][i + x_offset] = bits[i][j];	
                        }
                    }
                    x_offset = x_offset + 5;
        }
        x_offset = 0;

  }else{
  mode_counter +=1;
  // circularRotateVertical(frameBuffer, 8, 30, 25);

  }

        //Copy 
        int buffer_index = 0;
        for (int line  = start_line; line  < start_line + 7; line ++ ) {
            // 0x01 << 7 for dot #6
            buffer2[buffer_index + 1] = frameBuffer[line][0] << 6 | frameBuffer[line][1] << 5 | frameBuffer[line][2] << 4 | frameBuffer[line][3] << 3 |  frameBuffer[line][4] << 2  | frameBuffer[line][5] << 1  | frameBuffer[line][6];
            buffer2[buffer_index] =     frameBuffer[line][7] << 7 | frameBuffer[line][8] << 6 | frameBuffer[line][9] << 5 | frameBuffer[line][10] << 4 | frameBuffer[line][11] << 3 | frameBuffer[line][12] << 2 | frameBuffer[line][13] << 1 | frameBuffer[line][14];
            buffer[buffer_index] = frameBuffer[line][29] | frameBuffer[line][28] << 1 | frameBuffer[line][27] << 2 | frameBuffer[line][26] << 3 | frameBuffer[line][25] << 4 | frameBuffer[line][24] << 5 | frameBuffer[line][23] << 6 | frameBuffer[line][22] << 7;
            buffer[buffer_index + 1] = frameBuffer[line][21] | frameBuffer[line][20] << 1 | frameBuffer[line][19] << 2 | frameBuffer[line][18] << 3 | frameBuffer[line][17] << 4 | frameBuffer[line][16] << 5 | frameBuffer[line][15] << 6;
            buffer_index = buffer_index + 2;
        }
        buffer[14] = buffer[12];
        buffer[15] = buffer[13] & 0b00011111;

	buffer2[14] = buffer2[12];
	buffer2[15] = buffer2[13] & 0b00011111;
            
	if(dots == 0b00000010)
		dots = 0b00000000;
	else 
		dots = 0b00000010;

    // Dots 
	buffer[15] = buffer[15] | (dots & 0b00000001) << 6;
        buffer[13] = buffer[13] | (dots & 0b00000100) << 5;
        buffer[15] = buffer[15] | (dots & 0b00000010) << 6;
    // Shift by 1 position for first led driver  
    buffer2[15] = buffer2[15] | (dots >> 1  & 0b00000001) << 6;
        buffer2[13] = buffer2[13] | (dots >> 1 & 0b00000100) << 5;
        buffer2[15] = buffer2[15] | (dots >> 1 & 0b00000010) << 6;
	// displayMatrix(frameBuffer);

        // TODO remove unnecessary copy 
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

        // TODO remove unnecessary copy 
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
        usleep(100000);
    }

}

