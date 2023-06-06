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

send_timestamps = [[] for _ in serial_ports]
receive_timestamps = [[] for _ in serial_ports]

y = [0.0, 0.0, 0.0]
u_prev = [0.0, 0.0, 0.0]
u = [0.0, 0.0, 0.0]
y11_prev, y12_prev, y13_prev, y21_prev, y22_prev, y23_prev, y31_prev, y32_prev, y33_prev = 0, 0, 0, 0, 0, 0, 0, 0, 0
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
with open('logfile_serial_mini_model.log', 'w') as log_file:
    while True:
        # Get the current time at the start of the sequence
        current_time = time.time()

        '''
        # If less than 0.01 seconds have passed since the last 'sending' sequence, wait until 0.01 seconds have passed
        if current_time - last_receive_time < 0.01 and sending_completed:
            time.sleep(0.01 - (last_receive_time - first_send_time))  # Sleep for the remaining time to complete 0.01 seconds
        '''
        
        #print(u)
        y11 = (0.9900 * y11_prev) + (0.0050 * u[0]) + (0.0050 * u_prev[0])
        y12 = (0.9802 * y12_prev) + (0.0050 * u[1]) + (0.0050 * u_prev[1])
        y13 = (0.9704 * y13_prev) + (0.0049 * u[2]) + (0.0049 * u_prev[2])
        y[0] = y11 + y12 + y13
        '''
        print(f"y11_prev: {y11_prev}")
        print(f"y12_prev: {y12_prev}")
        print(f"y13_prev: {y13_prev}")
        print(f"u1 prev: {u_prev[0]}")
        print(f"u2 prev: {u_prev[1]}")
        print(f"u3 prev: {u_prev[2]}")
        print(f"y11: {y11}")
        print(f"y12: {y12}")
        print(f"y13: {y13}")
        '''
        #print(f"calculcated y1 to send: {y[0]}")
        y21 = 0.9608 * y21_prev + 0.0049 * u[0] + 0.0049 * u_prev[0]
        y22 = 0.9512 * y22_prev + 0.0049 * u[1] + 0.0049 * u_prev[1]
        y23 = 0.9417 * y23_prev + 0.0049 * u[2] + 0.0049 * u_prev[2]
        y[1] = y21 + y22 + y23
        #print(f"calculcated y2 to send: {y[1]}")
        y31 = 0.9324 * y31_prev + 0.0048 * u[0] + 0.0048 * u_prev[0]
        y32 = 0.9231 * y32_prev + 0.0048 * u[1] + 0.0048 * u_prev[1]
        y33 = 0.9139 * y33_prev + 0.0048 * u[2] + 0.0048 * u_prev[2]
        y[2] = y31 + y32 + y33
        #print(f"calculcated y3 to send: {y[2]}")
        
        #print(y)
        #print("\n")
        u_prev = u.copy()
        # Conduct the sending sequence
        for i in range(len(current_state)):
            if current_state[i] == 's':  # keep writing if state is sending
                ports[i].write("{:f}\n".format(y[i]).encode('utf-8'))
                send_timestamps[i].append(datetime.now())
                log_file.write(f"Serial {i} Sent Value {y[i]} @ {datetime.now()}\n")
                current_state[i] = 'r'
                if(i == 0):
                    first_send_time = time.time()
                    s0_send_times.append(datetime.now())

        #u_prev = u
        # Conduct the receiving sequence immediately after all sending finished
        for i in range(len(current_state)):
            while current_state[i] == 'r':  # wait until data is available
                if ports[i].in_waiting > 0:  
                    line = ports[i].readline().decode('utf-8').rstrip() #receive data
                    u[i] = float(line) #receive new u values u(k)
                    receive_timestamps[i].append(datetime.now())
                    current_state[i] = 's'
                    log_file.write(f"Serial {i} Received Value {u[i]}  @ {datetime.now()}\n")
        sending_completed = True
        last_receive_time = time.time()
        
        y11_prev = y11
        y12_prev = y12
        y13_prev = y13
        y21_prev = y21
        y22_prev = y22
        y23_prev = y23
        y31_prev = y31
        y32_prev = y32
        y33_prev = y33
        
