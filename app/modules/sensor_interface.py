from smbus import SMBus

class Fetcher():

    def fetch_sensor_data():
        addr = 0x8 # bus address
        bus = SMBus(1) # indicates /dev/ic2-1

        return temp, humid