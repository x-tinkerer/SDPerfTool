#!/usr/bin/python

__author__ = 'bigzhang'

import datetime
from pyadb import ADB
from lmdd_processor import LmddProcessor
from lmdd_speed import LmddSpeed
from optparse import OptionParser

if __name__ == '__main__':
    usage = "usage: %prog -t times"
    parser = OptionParser()
    parser.add_option('-t', '--times', dest = "times",
                      help = "Test Times",
                      default = 10, type = "int")

    (options, args) = parser.parse_args()

    adb = ADB()
    adb.set_adb_path('/home/bigzhang/Android/Sdk/platform-tools/adb')
    # verity ADB path
    if adb.check_path() is False:
        print "ERROR"
        exit(-2)

    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    speed_file = 'lmdd_perf_' + current_time + '.log'
    xlsx_file = 'lmdd_perf_' + current_time + '.xlsx'

    test_times = options.times
    tester = LmddSpeed(test_times, None, adb)
    list_size = tester.get_list_size()
    input_file = open(speed_file, 'wb+')

    tester.lmdd_header(input_file)
    tester.prepare_env()
    tester.lmdd_write(input_file)
    tester.lmdd_read(input_file)
    tester.finish()

    processor = LmddProcessor(xlsx_file, test_times, list_size)
    input_file = open(speed_file, 'r')
    lines = input_file.readlines()
    processor.parse(lines)
