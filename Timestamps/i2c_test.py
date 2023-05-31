import smbus
import time

bus = smbus.SMBus(1)

SLAVE_ADDRESS = 0x08

def writeNumber(value):
    bus.write_byte(SLAVE_ADDRESS, value)
    return -1

def readNumber():
    number = bus.read_byte(SLAVE_ADDRESS)
    return number

number = 1
while True:

    writeNumber(number)
    print("RPI: Hi Arduino, I sent you ", number)


    number = readNumber()
    print("RPI: Arduino, I received a digit ", number)
