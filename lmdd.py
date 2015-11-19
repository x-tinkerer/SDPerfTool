#!/usr/bin/python

__author__ = 'bigzhang'

from sys import stdin
from pyadb import ADB
from lmdd_processor import LmddProcessor
from lmdd_speed import LmddSpeed

if __name__ == '__main__':
    adb = ADB()
    adb.set_adb_path('/home/bigzhang/Android/Sdk/platform-tools/adb')
    # verity ADB path
    if adb.check_path() is False:
        print "ERROR"
        exit(-2)

    test_times = 10
    tester = LmddSpeed(test_times, None, adb)
    input_file = open('lmdd_perf_.log', 'wb+')

    tester.lmdd_header(input_file)
    tester.prepare_env()
    tester.lmdd_write(input_file)
    tester.lmdd_read(input_file)
    tester.finish()

    processor = LmddProcessor('lmdd_perf.xlsx',test_times)
    input_file = open('lmdd_perf_.log', 'r')
    lines = input_file.readlines()
    processor.parse(lines)
