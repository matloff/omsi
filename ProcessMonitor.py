import psutil
import time
import datetime

import ClientGlobals


def collectProcessInformation(output_file):

    # write current time to file
    output_file.write('processes '+ datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '\n')

    # write each process name, id, cpu percent and memory percent to file
    for proc in psutil.process_iter():

        # store process attributes (name, record number, process id, cpu percentage and memory percentage) in list
        entry = [proc.name(), proc.pid, proc.cpu_percent(), proc.memory_percent()]

        # write process attributes to file
        output_file.write(', '.join(str(item) for item in entry) + '\n')

        # flush output buffer
        output_file.flush()

    # ensure output buffer flushed before returning
    output_file.flush()
