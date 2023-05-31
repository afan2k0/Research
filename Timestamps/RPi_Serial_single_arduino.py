import serial
import time
from datetime import datetime, timedelta

ser = serial.Serial('/dev/ttyACM4', 115200, timeout=1)
ser.flush()

x = 1
timestamps = []
previous_operation = "read"
while x < 500:

    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        x = float(line)
        if(previous_operation == "write"):
            timestamps.append(datetime.now() - first_send_time)
            print("Received Value {}, {}".format(x, datetime.now()))
        previous_operation = "read"
        
    else:
        ser.write("{:f}\n".format(x).encode('utf-8'))
        if(previous_operation == "read"):
            first_send_time = datetime.now()
            print("Sent Value {}, {}".format(x, first_send_time))
        previous_operation = "write"

average_delta = sum(timestamps, timedelta(0)) / len(timestamps)
print("\nAverage time between sending and receiving in seconds (console logging): {:.8f}\n".format(average_delta.total_seconds()))


x = 1
timestamps = []
previous_operation = "read" 
with open('logfile_serial.log', 'w') as log_file:
    ser.flush()
    while x < 1000:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            x = float(line)
            if(previous_operation == "write"):
                timestamps.append(datetime.now() - first_send_time)
                log_file.write("Received Value {}, {}\n".format(x, datetime.now()))
            previous_operation = "read"
            
        else:
            ser.write("{:f}\n".format(x).encode('utf-8'))
            if(previous_operation == "read"):
                first_send_time = datetime.now()
                log_file.write("Sent Value {}, {}\n".format(x, first_send_time))
            previous_operation = "write"

    average_delta = sum(timestamps, timedelta(0)) / len(timestamps)
    log_file.write("\nAverage time between sending and receiving in seconds: {:.8f}\n".format(average_delta.total_seconds()))
ser.close()
print("\nAverage time between sending and receiving in seconds (file logging): {:.8f}\n".format(average_delta.total_seconds()))
