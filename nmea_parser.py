

class NmeaParser():
    def __init__(self) -> None:
        pass    

    def parse_gnrmc(self, sentence):
        if sentence.startswith('$GNRMC'):
            fields = sentence.split(',')
            time_utc = fields[1]   # UTC time (HHMMSS)
            status = fields[2]     # Status (A=active, V=void)
            latitude = fields[3]   # Latitude (DDMM.MMMM)
            longitude = fields[5]  # Longitude (DDDMM.MMMM)
            speed_over_ground = fields[7]  # Speed over ground in knots
            date_utc = fields[9]    # UTC date (DDMMYY)

            # Convert latitude and longitude to decimal degrees
            latitude_deg = float(latitude[:2]) + float(latitude[2:]) / 60.0
            longitude_deg = float(longitude[:3]) + float(longitude[3:]) / 60
            
            return {
                'time_utc': time_utc,
                'status' : status,
                'latitude' : latitude_deg,
                'longitude' : longitude_deg,
                'speed_over_ground' : speed_over_ground, 
                'date_utc' : date_utc
            }
        return None

if __name__ == '__main__':
    nmea_parser = NmeaParser()
    with open('nema_log.txt') as f:
        for line in f:
            if line.startswith('$GNRMC'):
                time_string = nmea_parser.parse_gnrmc(line).get('time_utc', '000000.000')
                
                hh = time_string[0] + time_string[1] 
                mm = time_string[2] + time_string[3]
                ss = time_string[4] + time_string[5]
                print(hh, mm, ss)
