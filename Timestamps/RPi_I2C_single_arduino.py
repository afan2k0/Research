import time
import smbus
from datetime import datetime, timedelta

bus = smbus.SMBus(1)
SLAVE_ADDRESS = 0x08

def writeNumber(value):
    bus.write_byte(SLAVE_ADDRESS, value)
    return -1

def readNumber():
    number = bus.read_byte(SLAVE_ADDRESS)
    return number

x = 1
timestamps = []
previous_operation = "read"
while x < 200:
    writeNumber(x)
    if(previous_operation == "read"): #now we are writing
        first_send_time = datetime.now()
        print("Sent Value {}, {}".format(x, first_send_time))
    previous_operation = "write"
    
    x = readNumber()
    if(previous_operation == "write"):
        timestamps.append(datetime.now() - first_send_time)
        print("Received Value {}, {}".format(x, datetime.now()))
    previous_operation = "read"

if len(timestamps) > 0:
    average_delta = sum(timestamps, timedelta(0)) / len(timestamps)
    print("\nAverage time between sending and receiving in seconds (console logging): {:.8f}\n".format(average_delta.total_seconds()))
else:
    print("No data received, cannot calculate average time.")


x = 1
timestamps = []
previous_operation = "read"
with open('logfile_i2c.log', 'w') as log_file:
    while x < 200:
        writeNumber(x)
        if(previous_operation == "read"):
            first_send_time = datetime.now()
            log_file.write("Sent Value {}, {}\n".format(x, first_send_time))
        previous_operation = "write"
        
        x = readNumber()
        if(previous_operation == "write"):
            timestamps.append(datetime.now() - first_send_time)
            log_file.write("Received Value {}, {}\n".format(x, datetime.now()))
        previous_operation = "read"

    if len(timestamps) > 0:
        average_delta = sum(timestamps, timedelta(0)) / len(timestamps)
        log_file.write("\nAverage time between sending and receiving in seconds: {:.8f}\n".format(average_delta.total_seconds()))
    else:
        log_file.write("No data received, cannot calculate average time.")

if len(timestamps) > 0:
    print("\nAverage time between sending and receiving in seconds (file logging): {:.8f}\n".format(average_delta.total_seconds()))
else:
    print("No data received, cannot calculate average time.")
