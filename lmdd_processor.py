#!/usr/bin/python

__author__ = 'bigzhang'

import sys
import string
import re
import xlsxwriter
from optparse import OptionParser

class LmddProcessor(object):
    def __init__(self,excle_name,tims, size):
        """
        """
        workbook = xlsxwriter.Workbook(excle_name)
        worksheet = workbook.add_worksheet()
        self.workbook = workbook
        self.worksheet = worksheet

        bold = workbook.add_format({'bold': True})
        headings = ['Size', 'Times','time_w', 'speed_w', 'time_r', 'speed_r']
        worksheet.write_row('A1', headings, bold)
        avgheadings = ['Size', 'Wrtie', 'Read']
        worksheet.write_row('K1', avgheadings, bold)

        self.isread = 0
        self.size = 0

        self.count = 0
        self.totoltime = 0
        self.totolperf = 0

        self.col = 0
        self.avgindex = 0

        self.testtimes = tims
        self.listsize = size

    """
    find out read/write performance data,
    and write to excel table.
    """
    def write_excle(self,fields):
        """
        Write out to excel table.
        """
        row = long(fields['col'])

        if(fields['isread']):
            self.worksheet.write(row, 4, float(fields['time']))
            self.worksheet.write(row, 5, float(fields['perf']))
            if(fields['index'] == self.testtimes ):
                avgrow = fields['avgindex']
                #self.worksheet.write(avgrow, 14, float(fields['timeavg']))
                self.worksheet.write(avgrow, 12, float(fields['perfavg']))
        else:
            self.worksheet.write(row, 0, fields['size'])
            self.worksheet.write(row, 1, float(fields['index']))
            self.worksheet.write(row, 2, float(fields['time']))
            self.worksheet.write(row, 3, float(fields['perf']))

            if(fields['index'] == self.testtimes ):
                avgrow = fields['avgindex']
                self.worksheet.write(avgrow, 10, fields['size'])
                #self.worksheet.write(avgrow, 11, float(fields['timeavg']))
                self.worksheet.write(avgrow, 11, float(fields['perfavg']))

    def add_chart(self):
        # Create a new chart object.
        chart = self.workbook.add_chart({'type': 'line'})

        chart.set_x_axis({
            'name': 'Size',
            'name_font': {'size': 14, 'bold': True},
            'num_font':  {'italic': True },
        })

        # Add a series to the chart.
        avg_col =self.listsize + 1
        arr_str = '=Sheet1!$L$2:$L$' + str(avg_col)
        chart.add_series({
            'name': 'Write',
            'values': arr_str,
            'marker': {
                'type': 'square',
                'size': 4,
                'border': {'color': 'black'},
                'fill':   {'color': 'red'},
            },
        })

        # Add a series to the chart.
        arr_str = '=Sheet1!$M$2:$M$' + str(avg_col)
        chart.add_series({
            'name': 'Read',
            'values': arr_str,
            'marker': {
                'type': 'square',
                'size': 4,
                'border': {'color': 'blue'},
                'fill':   {'color': 'red'},
            },
        })

        self.worksheet.insert_chart('L20', chart)

    def finish(self):
        self.workbook.close()

    """
    Read input file and split it.
    """
    def reset_count(self):
        self.count = 0
        self.totoltime = 0
        self.totolperf = 0

    def check_isread(self, line):
        isread = re.search(r'\slmdd read\s', line)
        if isread:
            #print line
            self.isread = 1
            self.col = 0
            self.avgindex = 0

    def check_ishead(self, line):
        issize = re.search(r'\sSize ===', line)
        if issize:
            #print line
            dosize = re.findall(r'\d+[k|m]',line)
            self.size = dosize[0]
            self.reset_count()
            self.avgindex += 1

    def split(self, line):
            """
            """

            self.check_isread(line)
            self.check_ishead(line)

            isperf = re.search(r'\sMB/sec\s', line)

            if isperf:
                #print line
                data = re.findall(r'[\d|.]+',line)
                self.count += 1
                self.col += 1
                self.totoltime += string.atof(data[1])
                self.totolperf += string.atof(data[2])


                return {
                    'isread':self.isread,
                    'col':  self.col,
                    'size': self.size,
                    'index': self.count,
                    'time': data[1],
                    'perf': data[2],
                    'timeavg': self.totoltime/self.count,
                    'perfavg': self.totolperf/self.count,
                    'avgindex':self.avgindex,
                }

    def parse(self, handle):
            """
            Parses the log file.
            Returns a dictionary composed of log entry values
            for easy data summation
            """
            for line in handle:
                fields = self.split(line)
                "Reserve one line for head"
                if fields:
                    self.write_excle(fields)

            self.add_chart()
            self.finish()


if __name__ == '__main__':

    processor = LmddProcessor('lmddout.xlsx',10)
    input_file = open('lmdd_perf_.log', 'r')
    lines = input_file.readlines()
    processor.parse(lines)