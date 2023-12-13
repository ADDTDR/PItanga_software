import serial
import os
from nmea_parser import NmeaParser
from functools import reduce
import threading
import time 

class GpsSerialReader():
    def __init__(self) -> None:
        self.serial_device = serial.Serial('/dev/ttyUSB0', 9600)
        self.nmea_parser = NmeaParser()
        
    def read_serial_gps_device(self):
        while True:
            data = self.serial_device.readline()
            if data:
                try:
                    gnrmc_dict = self.nmea_parser.parse_gnrmc(data.decode())
                except:
                    gnrmc_dict = {}

                if gnrmc_dict is not None:                    
                    time_string = gnrmc_dict.get('time_utc', '000000.000')                        
                    hh = time_string[0] + time_string[1] 
                    mm = time_string[2] + time_string[3]
                    ss = time_string[4] + time_string[5]
                    os.environ['GPS_CLOCK'] = hh + ':' + mm + ':' + ss
          

if __name__ == '__main__':
        gps_serial_reader = GpsSerialReader()
        t = threading.Thread(name='gps_serial_reader', target=gps_serial_reader.read_serial_gps_device)
        t.start()
        while True:
            print(os.environ.get('GPS_CLOCK'))
            time.sleep(1)
            print( reduce( lambda a, ax: ax + a, ['-' for _ in range(1, 40)]) )
