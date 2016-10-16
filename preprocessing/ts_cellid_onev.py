#!/usr/bin/env python

"""
------------------------------------------------------------------------------------------------------------------
TELECOM DATA PARSER

File name: ts_cellid_one.py
Description: This script parse the Telecom data files and convert them in one csv file with
data each hour and without country code.
Author:Carolina Arias Munoz
Date Created: 30/07/2016
Date Last Modified: 30/07/2016
Python version: 2.7
------------------------------------------------------------------------------------------------------------------
"""

import csv
import numpy
import time
#from datetime import datetime, timedelta
import glob

def tsv_from_dict(dictionary):
  table = ""

  for date_time in dictionary.keys():
    for sid in dictionary[date_time].keys():
      table += date_time + '\t' + str(sid) + '\t' + str(dictionary[date_time][sid]) + '\n'
    
  
  return table
# ---------------------------------------------------------------
ncols = 2
nrows = 24

grid_nodata = -9999

records = nrows

# tsv_file = 'sms-call-internet-mi-2013-11-01.txt'

out = {}

#-----------------------------------------------------------------------------------------------------     
data_path = 'your path'
data_files = glob.glob(data_path + '*.txt')

for data_file in data_files:

  with open(data_file, 'rb') as telecom_data:

    telecom_data = csv.reader(telecom_data, delimiter='\t')
    count = 0

    print "Start parsing data in " + data_file + '...'

    for row in telecom_data:

      # 0: lat
      # 1: long
      # 2: name
      # 3: timestamp
      # 4: temperature
      # 5: humidity
      # 6: precipitation
      # 7: heatindex

      sid = row[0]
      ts = row[1]
      ts = numpy.longdouble(ts)
      variable = row[6]

      # Check empty values and convert values to double
      if variable == '':
        variable = numpy.longdouble(0.0)
      elif type(variable) is str:
        variable = numpy.longdouble(variable)
      
      
      #timestamp 
      # %w - day of the week as a decimal, Sunday=0 
      # %W - week number of the current year, starting with the first Monday as the first day of the first week
      # ts = time.strftime("%Y-%m-%d %H:%M:%S-%W-%w", time.gmtime(ts))
      #date = time.strftime("%Y-%m-%d", time.gmtime(ts))
      date_time = time.strftime("%Y-%m-%dT%H:00:00+0100", time.gmtime(ts))
      #hour = time.strftime("%H", time.gmtime(ts))
    
       # Add the timestamp to the dictionary
      if date_time not in out:
        out[date_time] = {}
     
      # Add the cell id to the dictionary
      if sid not in out[date_time]:
       out[date_time][sid] = numpy.longdouble(0.0)

      # Add values with same timestamp and same cell id
      out[date_time][sid] += variable
      
      count += 1

      # Give feedback
      if count < 10000 and count % 1000 == 0:
        print 'Parsed', count, 'records'    
      elif count % 100000 == 0:
        print 'Parsed', count, 'records'
print ""
# Give feedback again
#print 'Finished parsing data. There are', len(out.keys()), 'timestamps.'
#print 'Writing', len(out.keys()), ' files...'
print 'Finished parsing data.'
print 'Writing files...'

#-----------------------------------------------------------------------------------------------------     





# Write the files

for date_time in sorted(out):

  fcount = 0

print "Done"





