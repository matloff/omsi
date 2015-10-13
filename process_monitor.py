__author__ = 'rylan'

import sys

try:
    import psutil
except ImportError:
    print 'Cannot import psutil library. Exiting...'
    sys.exit()

try:
    import time
except ImportError:
    print 'Cannot import time library. Exiting...'
    sys.exit()

try:
    import datetime
except ImportError:
    print 'Cannot import datetime library. Exiting...'
    sys.exit()


def collect_process_information(record_num, output_file):

    # write current time to file
    output_file.write(datetime.datetime.now().strftime('%Y%m%d%M%S') + '\n')

    # write each process name, id, cpu percent and memory percent to file
    for proc in psutil.process_iter():

        # store process attributes (name, record number, process id, cpu percentage and memory percentage) in list
        entry = [proc.name(), record_num, proc.pid, proc.cpu_percent(), proc.memory_percent()]

        # write process attributes to file
        output_file.write(', '.join(str(item) for item in entry) + '\n')

        # flush output buffer
        output_file.flush()

    # easy debugging
    output_file.write('\n\n\n\n\n\n\n\n')

    # ensure output buffer flushed before returning
    output_file.flush()
    return


def convert_to_int(input_str):
    while True:
        try:
            output_int = int(input_str)
            return output_int
        except ValueError:
            output_int = raw_input('Please enter an integer: ')


def main():
    # allow professor to set how frequently process information will be recorded
    frequency = convert_to_int(raw_input('Please enter time spacing in seconds: '))

    # allow user to decide how long the test will be
    test_duration = convert_to_int(raw_input('Please enter test time in minutes: '))

    # calculate end time
    end_time = datetime.datetime.now() + datetime.timedelta(minutes=test_duration)

    # open file to store process information
    output_file = open('output.txt', 'w')

    # create and initialize integer to track the number of completed process information collection
    record_number = 0

    # collect process information from student's machine as long as student hasn't exceeded end of test
    while datetime.datetime.now() < end_time:

        collect_process_information(str(record_number), output_file)

        record_number += 1

        time.sleep(frequency)

    # stop collecting process information once test has finished
    print 'Test is over\n'
    sys.exit()

if __name__ == '__main__':
    main()
