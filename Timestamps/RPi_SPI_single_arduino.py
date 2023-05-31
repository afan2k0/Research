import spidev
import time
import struct

spi = spidev.SpiDev()
spi.open(0,0) # Open SPI bus 0 device 0
spi.max_speed_hz = 500000

try:
    x = 1
    while True:
        spi.xfer2([0xFF])  # Send sync byte
        time.sleep(0.001)
        resp = spi.readbytes(4)  # read 4 bytes
        x = struct.unpack('>I', bytes(resp))[0]  # unpack bytes into integer, big-endian
        print("Received: ", x)
        x += 1
except KeyboardInterrupt:
    spi.close()
