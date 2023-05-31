import time
from datetime import datetime

x = 1
timestamps = []

for i in range(500):
    current_timestamp = datetime.now()
    print(x, current_timestamp)
    
    timestamps.append(current_timestamp)
    
    x += 1

deltas = [(timestamps[i+1] - timestamps[i]).total_seconds() for i in range(len(timestamps)-1)]
average_delta = sum(deltas) / len(deltas)

print("\nAverage delta between each print in milliseconds (console logging): {:.8f}\n".format(average_delta * 1000))
average_delta_1 = average_delta * 1000


x = 1
timestamps = []
with open("logfile.log", "w") as log_file:
    for i in range(500):
        current_timestamp = datetime.now()
        log_file.write("Value of x: {}\n".format(x))
        log_file.write("Timestamp in milliseconds: {}\n".format(current_timestamp.microsecond / 1000))
        
        timestamps.append(current_timestamp)

        x += 1
        
    deltas = [(timestamps[i+1] - timestamps[i]).total_seconds() for i in range(len(timestamps)-1)]
    average_delta = sum(deltas) / len(deltas)

    log_file.write("\nAverage delta between each print in milliseconds (file logging): {:.8f}\n".format(average_delta * 1000))
print("\nAverage delta between each print in milliseconds (file logging): {:.8f}\n".format(average_delta * 1000))

print("File logging is {:.2f} x faster".format(average_delta_1 / (average_delta * 1000)))
