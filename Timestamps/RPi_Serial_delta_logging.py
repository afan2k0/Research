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
values = [-999.99, -999.99, -999.99]

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
last_receive_time = time.time()
first_send_time = time.time()
current_state = ['s', 's', 's']  # current state is the state that it needs to do
sending_completed = False
with open('logfile_serial_multi.log', 'w') as log_file:
    while values[0] < 999.99 or values[1] < 999.99 or values[2] < 999.99:
        # Get the current time at the start of the sequence
        current_time = time.time()

        # If less than 0.01 seconds have passed since the last 'sending' sequence, wait until 0.01 seconds have passed
        if current_time - last_receive_time < 0.01 and sending_completed:
            time.sleep(0.01 - (last_receive_time - first_send_time))  # Sleep for the remaining time to complete 0.01 seconds
            

       
        # Conduct the sending sequence
        for i in range(len(current_state)):
            if current_state[i] == 's':  # keep writing if state is sending
                ports[i].write("{:f}\n".format(values[i]).encode('utf-8'))
                send_timestamps[i].append(datetime.now())
                if i == 0:
                    log_file.write(f"Serial {i} Sent Value {values[i]} @ {datetime.now()}\n")
                current_state[i] = 'r'
                if(i == 0):
                    first_send_time = time.time()
                    s0_send_times.append(datetime.now())

        # Conduct the receiving sequence immediately after all sending finished
        for i in range(len(current_state)):
            while current_state[i] == 'r':  # wait until data is available
                if ports[i].in_waiting > 0:  
                    line = ports[i].readline().decode('utf-8').rstrip()
                    values[i] = float(line)
                    receive_timestamps[i].append(datetime.now())
                    current_state[i] = 's'
                    #log_file.write(f"Serial {i} Received Value {values[i]}  @ {datetime.now()}\n")
        sending_completed = True
        last_receive_time = time.time()
