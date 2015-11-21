## SDPerfTool

This is a SD/eMMC Performance auto test tool.

### Prepare:
1. Install Python
Download link:https://www.python.org/downloads/release/python-2710/

2. Install xlsxwriter
xlsxwriter Home Page:http://xlsxwriter.readthedocs.org/getting_started.html
use command line: pip install XlsxWriter

3. Config adb path.
Modify adb.conf, replace whit your computer's adb path.

### How To Use:
Run as command line: python lmdd.py [-d target ]{-t times}

target: is data or sdcard or sdcard1.
times: default is 10, if you do not write anything.
