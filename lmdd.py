#!/usr/bin/python

__author__ = 'bigzhang'

import datetime
from pyadb import ADB
from lmdd_processor import LmddProcessor
from lmdd_speed import LmddSpeed
from optparse import OptionParser

target_list=['data', 'sdcard', 'sdcard1']

if __name__ == '__main__':
    usage = "usage: %prog [-d target]{-t times}"
    parser = OptionParser()
    parser.add_option('-t', '--times', dest = "times",
                      help = "Test Times",
                      default = 10, type = "int")

    parser.add_option('-d', '--dest', dest = "target",
                      help = "The target test path, data or sdcard or sdcard1",
                      type = "string")

    (options, args) = parser.parse_args()

    # get adb path for config file.
    adb_conf = open('adb.conf', 'r')
    adbpath = adb_conf.readlines()
    adb_conf.close()
    if adbpath == []:
        print "Please config ADB PATH!"
        exit(0)
    adb = ADB()
    adb.set_adb_path(adbpath[0])
    # verity ADB path
    if adb.check_path() is False:
        print "ERROR: ADB PATH NOT Correct."
        exit(-2)

    # get detected devices
    dev = 0
    while dev is 0:
        print "Detecting devices..." ,
        error,devices = adb.get_devices()

        if len(devices) == 0:
            print "[+] No devices detected!"
            print "Waiting for devices..."
            adb.wait_for_device()
            continue
        elif error is 2:
            print "You haven't enought permissions!"
            exit(-3)

        print "OK"
        dev = 1

    # adb need run as root
    adb.set_adb_root()
    adb.wait_for_device()

    # built log and xlsx file name with datetime
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    speed_file = 'lmdd_perf_' + current_time + '.log'
    xlsx_file = 'lmdd_perf_' + current_time + '.xlsx'

    # built SPEED Tester.
    test_times = options.times
    test_target = options.target

    if test_target not in target_list:
        print 'PLEASE INPUT TARGET PATH!'
        print '--- Target: data or sdcard or sdcard1 ---'
        print '--- Target: data or sdcard or sdcard1 ---'
        print '--- Target: data or sdcard or sdcard1 ---'
        exit(0)
    else:
        print 'Test Target:%s' %test_target

    tester = LmddSpeed(test_times, None, adb, test_target)
    list_size = tester.get_list_size()
    input_file = open(speed_file, 'wb+')

    tester.lmdd_header(input_file)
    tester.prepare_env()
    tester.lmdd_write(input_file)
    tester.lmdd_read(input_file)
    tester.finish()

    # Analyse speed log and built xlsx report
    processor = LmddProcessor(xlsx_file, test_times, list_size)
    input_file = open(speed_file, 'r')
    lines = input_file.readlines()
    processor.parse(lines)
