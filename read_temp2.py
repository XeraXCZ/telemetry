import os
import time
import spidev
from datetime import datetime
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

# Initialize hardware SPI (SPI0) for the first MAX6675
spi0 = spidev.SpiDev()
spi0.open(0, 0)  # bus 0, device 0 (CS0)
spi0.max_speed_hz = 5000

# Initialize software SPI for the second MAX6675
gpio = GPIO.get_platform_gpio()
spi1 = SPI.BitBang(gpio, 24, 10, 23, 25)  # 10 is used as dummy MOSI pin

def read_temp_hardware(spi_device):
    # Read 2 bytes of data from the MAX6675
    raw = spi_device.xfer2([0x00, 0x00])
    value = (raw[0] << 8) | raw[1]
    # Remove the lower 3 bits (status bits)
    value >>= 3
    # Convert to Celsius (each bit represents 0.25 degrees Celsius)
    temp_c = value * 0.25
    return temp_c

def read_temp_software(spi_device):
    # Read 2 bytes of data from the MAX6675 using software SPI
    raw = spi_device.transfer([0x00, 0x00])
    value = (raw[0] << 8) | raw[1]
    # Remove the lower 3 bits (status bits)
    value >>= 3
    # Convert to Celsius (each bit represents 0.25 degrees Celsius)
    temp_c = value * 0.25
    return temp_c

try:
    while True:
        motor = read_temp_hardware(spi0)
        oil = read_temp_software(spi1)
        dt = datetime.now()
        print(f"{dt},{oil},{motor}")
        #print("Oil: {:.2f} °C".format(oil))
        #print("Motor: {:.2f} °C".format(motor))
        time.sleep(1)
except KeyboardInterrupt:
    spi0.close()

