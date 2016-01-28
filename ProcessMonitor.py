import datetime
import psutil

import ClientGlobals


def collectProcessesInformation(pOutputFile):

    # write current time to file
    pOutputFile.write('processes '+ datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '\n')

    # write each process name, id, cpu percent and memory percent to file
    for proc in psutil.process_iter():

        # store process attributes (name, record number, process id, cpu percentage and memory percentage) in list
        entry = [proc.name(), proc.pid, proc.cpu_percent(), proc.memory_percent()]

        # write process attributes to file
        pOutputFile.write(', '.join(str(item) for item in entry) + '\n')

        # flush output buffer
        pOutputFile.flush()

    # ensure output buffer flushed before returning
    pOutputFile.flush()
