#!/usr/bin/python

__author__ = 'bigzhang'

from pyadb import ADB

class LmddSpeed(object):
    __adb =None
    __times = 0
    __size_list =[]
    __target ='/data'

    def __init__(self, times=None, size_list=None, adb=None, target=None):
        if times == None:
            self.__times = 10
        else:
            self.__times = times
        #size_list = ['8k', '32k', '128k', '512k', '2m', '8m', '32m', '128m', '512m']
        if size_list == None:
            self.__size_list = ['8k', '16k', '32k', '64k', '128k', '256k', '512k', '1m', '2m', '4m', '8m', '16m', '32m', '64m', '128m', '256m', '512m', '1024m']
        else:
            self.__size_list = size_list
        self.__adb = adb
        self.__target = target

        if target == 'data':
            self.__target_path = '/data/dumb'
        elif target == 'sdcard':
            self.__target_path = '/storage/sdcard/dumb'
        else:
            self.__target_path = '/storage/sdcard1/dumb'

    def lmdd_header(self, fd):
        fd.writelines('== HW Info ==')
        cpuinfo = self.__adb.shell_command('cat /proc/cpuinfo')
        fd.writelines(cpuinfo)

    def get_list_size(self):
        return len(self.__size_list)

    def prepare_env(self):
        self.__adb.shell_command('stop')
        self.__adb.shell_command('sleep 5')
        self.__adb.push_local_file('./bin/lmdd', '/data/lmdd')
        self.__adb.shell_command('chmod 777 /data/lmdd')

    def finish(self):
        self.__adb.shell_command('rm /data/lmdd')
        self.__adb.shell_command('rm %s' % self.__target_path)
        self.__adb.shell_command('start')

    def lmdd_write(self, fd):
        fd.writelines('=============== lmdd write test ===============\n')
        for size in self.__size_list:
            loop = 0
            print('=== %s === \n' %size)
            fd.writelines('=== %s Size ===\n' %size)
            while loop < self.__times:
                perf_out = self.__adb.shell_command('/data/lmdd if=internal of=%s move=%s fsync=1' % (self.__target_path, size))
                print(perf_out)
                fd.writelines(perf_out)
                loop = loop + 1

    def lmdd_read(self, fd):
        fd.writelines('=============== lmdd read test ===============\n')
        for size in self.__size_list:
            loop = 0
            print('=== %s ===\n' %size)
            fd.writelines('=== %s Size ===\n' %size)
            while loop < self.__times:
                self.__adb.shell_command('echo 3 > /proc/sys/vm/drop_caches')
                perf_out = self.__adb.shell_command('/data/lmdd if=%s of=internal move=%s fsync=1' %(self.__target_path, size))
                print(perf_out)
                fd.writelines(perf_out)
                loop = loop + 1

if __name__ == '__main__':
    adb = ADB()
    adb.set_adb_path('/home/bigzhang/Android/Sdk/platform-tools/adb')
    # verity ADB path
    if adb.check_path() is False:
        print "ERROR"
        exit(-2)

    tester = LmddSpeed(None,None,adb)
    input_file = open('lmdd_perf_.log', 'wb+')

    tester.lmdd_header(input_file)
    tester.prepare_env()
    tester.lmdd_write(input_file)
    tester.lmdd_read(input_file)
    tester.finish()
