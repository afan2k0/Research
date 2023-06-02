import serial
import time
from datetime import datetime, timedelta
# Initialize the serial connections
serial_ports = ['/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyACM2']
serial_baud_rate = 115200
serial_timeout = 1
num_ports = len(serial_ports)

# Initialize the serial ports
ports = [serial.Serial(port, serial_baud_rate, timeout=serial_timeout) for port in serial_ports]

# Initialize the data to be sent
values = [-999.99, -799.99, -599.99]

send_timestamps = [[] for _ in serial_ports]
receive_timestamps = [[] for _ in serial_ports]

s0_send_times = []
# Flush the ports
for port in ports:
    port.flush()

# Wait for initialization message from each port
for i, port in enumerate(ports):
    print(f"establishing handshake with {port}...")
    while True:
        if port.in_waiting > 0:
            line = port.readline().decode('utf-8').rstrip()
            if line == "READY":
                print(f"Port {serial_ports[i]} is ready.")
                break
        else:
            time.sleep(0.1)  # avoid busy-waiting

current_state = ['s', 's', 's']  # current state is the state that it needs to do
prev_state = 'r'
while values[0] < 999.99 or values[1] < 999.99 or values[2] < 999.99:
    # need to keep sending until current state != all s
    for i in range(len(current_state)):
        if current_state[i] == 's':  # keep writing if state is sending
            ports[i].write("{:f}\n".format(values[i]).encode('utf-8'))
            send_timestamps[i].append(datetime.now())
            print(f"Serial {i} Sent Value {values[i]} @ {datetime.now()}")
            current_state[i] = 'r'
            if(i == 0 and prev_state == 'r'):
                s0_send_times.append(datetime.now())
                prev_state = 's'
        elif ports[i].in_waiting > 0 and current_state[i] == 'r':  # start reading
            line = ports[i].readline().decode('utf-8').rstrip()
            values[i] = float(line)
            receive_timestamps[i].append(datetime.now())
            current_state[i] = 's'
            prev_state = 'r'
            print(f"Serial {i} Received Value {values[i]}  @ {datetime.now()}")
# Calculate average delays
average_delays = []
for send_times, recv_times in zip(send_timestamps, receive_timestamps):
    delays = [(r - s).total_seconds() for s, r in zip(send_times, recv_times)]
    average_delay = sum(delays) / len(delays)
    average_delays.append(average_delay)

print("Average delays (in seconds) per port: ", average_delays)


s0_deltas = [(s0_send_times[i+1] - s0_send_times[i]).total_seconds() for i in range(len(s0_send_times)-1)]
com_cycle = sum(s0_deltas) / len(s0_deltas)
print(f"Communication Cycle (in seconds): {com_cycle}")


# Initialize the data to be sent
values = [-999.99, -799.99, -599.99]

send_timestamps = [[] for _ in serial_ports]
receive_timestamps = [[] for _ in serial_ports]

s0_send_times = []
current_state = ['s', 's', 's']  # current state is the state that it needs to do
prev_state = 'r'
with open('logfile_serial_3multi.log', 'w') as log_file:
    while values[0] < 999.99 or values[1] < 999.99 or values[2] < 999.99:
        # need to keep sending until current state != all s
        for i in range(len(current_state)):
            if current_state[i] == 's':  # keep writing if state is sending
                ports[i].write("{:f}\n".format(values[i]).encode('utf-8'))
                send_timestamps[i].append(datetime.now())
                log_file.write(f"Serial {i} Sent Value {values[i]} @ {datetime.now()}\n")
                current_state[i] = 'r'
                if(i == 0 and prev_state == 'r'):
                    s0_send_times.append(datetime.now())
                    prev_state = 's'
            elif ports[i].in_waiting > 0 and current_state[i] == 'r':  # start reading
                line = ports[i].readline().decode('utf-8').rstrip()
                values[i] = float(line)
                receive_timestamps[i].append(datetime.now())
                current_state[i] = 's'
                prev_state = 'r'
                log_file.write(f"Serial {i} Received Value {values[i]} @ {datetime.now()}\n")
    # Calculate average delays
    average_delays = []
    for send_times, recv_times in zip(send_timestamps, receive_timestamps):
        delays = [(r - s).total_seconds() for s, r in zip(send_times, recv_times)]
        average_delay = sum(delays) / len(delays)
        average_delays.append(average_delay)

    log_file.write(f"Average delays (in seconds) per port: {average_delays}\n")


    s0_deltas = [(s0_send_times[i+1] - s0_send_times[i]).total_seconds() for i in range(len(s0_send_times)-1)]
    com_cycle = sum(s0_deltas) / len(s0_deltas)
    log_file.write(f"Communication Cycle (in seconds): {com_cycle}")
