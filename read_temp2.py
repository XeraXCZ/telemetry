import spidev
import time
from datetime import datetime
import re

# Start date for file naming
startdate = datetime.now()
filename = re.sub('[-: ]', '', str(startdate)[:-7])

# Setup hardware SPI
spi1 = spidev.SpiDev(0, 0)  # Bus 0, Device 0 (CS0)
spi2 = spidev.SpiDev(0, 1)  # Bus 0, Device 1 (CS1)
spi1.max_speed_hz = 50000
spi2.max_speed_hz = 50000

file = f"/home/rajda/data/{filename}"

def read_temp_software(spi_device):
    raw = spi_device.xfer2([0x00, 0x00])
    value = (raw[0] << 8) | raw[1]
    value >>= 3
    temp_c = value * 0.25
    return temp_c

try:
    while True:
        temperature1 = read_temp_software(spi1)
        temperature2 = read_temp_software(spi2)
        dt = str(datetime.now())[:-7]
        with open(f"{file}", "a") as f:
            f.write(f"{dt},{temperature1},{temperature2}\n")
        with open("/home/rajda/data/telemetry.prom", "w") as telemetry_file:
            telemetry_file.write(f"temperature_one {temperature1}\n")
            #telemetry_file.write(f"{dt},{temperature1},{temperature2}")
        #print(f"{dt},{temperature1},{temperature2}")
        time.sleep(1)
except KeyboardInterrupt:
    spi1.close()
    spi2.close()
    print("Program interrupted")
