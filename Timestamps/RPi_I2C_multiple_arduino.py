import time
from smbus2 import SMBus, i2c_msg
from datetime import datetime, timedelta
import struct

bus = SMBus(1)
time.sleep(1)
addresses = [0x01, 0x02, 0x03]
values = [-99.99, -99.99, -99.99]
def float_to_bytes(f):
    packed = struct.pack('!f', f)
    return bytearray(packed)

def bytes_to_float(byte_list):
    byte_array = bytes(byte_list)
    unpacked = struct.unpack('<f', byte_array)
    return unpacked[0]  

def writeNumber(address, value):
    msg = i2c_msg.write(address, float_to_bytes(value))
    bus.i2c_rdwr(msg)

def readNumber(address):
    msg = i2c_msg.read(address, 4)
    bus.i2c_rdwr(msg)
    return(bytes_to_float(msg))


for i in range(len(addresses)):
    writeNumber(addresses[i], 1500)
    print(f"Wrote to {addresses[i]}: 1500 @ {datetime.now()}")
temp = readNumber(addresses[0])
print(f"Read from {addresses[0]}: {temp} @ {datetime.now()}")
temp = readNumber(addresses[1])
print(f"Read from {addresses[1]}: {temp} @ {datetime.now()}")
temp = readNumber(addresses[2])
print(f"Read from {addresses[2]}: {temp} @ {datetime.now()}")
    



send_timestamps = [[] for _ in addresses]
receive_timestamps = [[] for _ in addresses]
s0_send_times = []

previous_operation = "read"
while all(x < 0 for x in values):
    for i in range(len(addresses)):
        if i == 0:
            s0_send_times.append(datetime.now())
        writeNumber(addresses[i], values[i])
        send_timestamps[i].append(datetime.now())
        print(f"Wrote to {addresses[i]}: {values[i]} @ {datetime.now()}")
        values[i] = round(readNumber(addresses[i]), 2)
        receive_timestamps[i].append(datetime.now())
        print(f"Read from {addresses[i]}: {values[i]} @ {datetime.now()}")
    time.sleep(0.01)
average_delays = []

for send_times, recv_times in zip(send_timestamps, receive_timestamps):
    delays = [(r - s).total_seconds() for s, r in zip(send_times, recv_times)]
    average_delay = sum(delays) / len(delays)
    average_delays.append(average_delay)

print("Average delays (in seconds) per port: ", average_delays)


s0_deltas = [(s0_send_times[i+1] - s0_send_times[i]).total_seconds() for i in range(len(s0_send_times)-1)]
com_cycle = sum(s0_deltas) / len(s0_deltas)
print(f"Communication Cycle (in seconds): {com_cycle}")

values = [-99.99, -99.99, -99.99]
for i in range(20):
    for i in range(len(addresses)):
        writeNumber(addresses[i], 1500)
        print(f"Wrote to {addresses[i]}: 1000 @ {datetime.now()}")
temp = readNumber(addresses[0])
print(f"Read from {addresses[0]}: {temp} @ {datetime.now()}")
temp = readNumber(addresses[1])
print(f"Read from {addresses[1]}: {temp} @ {datetime.now()}")
temp = readNumber(addresses[2])
print(f"Read from {addresses[2]}: {temp} @ {datetime.now()}")

send_timestamps = [[] for _ in addresses]
receive_timestamps = [[] for _ in addresses]
s0_send_times = []

with open('logfile_i2c_multi.log', 'w') as log_file:
    while all(x < 0 for x in values):
        for i in range(len(addresses)):
            if i == 0:
                s0_send_times.append(datetime.now())
            writeNumber(addresses[i], values[i])
            send_timestamps[i].append(datetime.now())
            log_file.write(f"Wrote to {addresses[i]}: {values[i]} @ {datetime.now()}\n")
            values[i] = round(readNumber(addresses[i]), 2)
            receive_timestamps[i].append(datetime.now())
            log_file.write(f"Read from {addresses[i]}: {values[i]} @ {datetime.now()}\n")
        time.sleep(0.01)
    average_delays = []
    for send_times, recv_times in zip(send_timestamps, receive_timestamps):
        delays = [(r - s).total_seconds() for s, r in zip(send_times, recv_times)]
        average_delay = sum(delays) / len(delays)
        average_delays.append(average_delay)

    log_file.write(f"Average delays (in seconds) per port: {average_delays} @ {datetime.now()}\n")


    s0_deltas = [(s0_send_times[i+1] - s0_send_times[i]).total_seconds() for i in range(len(s0_send_times)-1)]
    com_cycle = sum(s0_deltas) / len(s0_deltas)
    log_file.write(f"Communication Cycle (in seconds): {com_cycle}\n")
print("finished writing to log file") 
