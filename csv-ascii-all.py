#!/usr/bin/env python
"""
------------------------------------------------------------------------------------------------------------------
CSV/TSV files to ESRI ascii 
File name: csv-ascii-all.py
Description: This script creates csv/tsv files from https://dandelion.eu/datagems/SpazioDati/telecom-sms-call-internet-mi/description/
to ascii ESRI files.
Author:Carolina Arias Munoz
Date Created: 12/01/2016
Python version: 2.7
------------------------------------------------------------------------------------------------------------------
"""
import csv, numpy, time
import glob

def ascii_grid_from_dict(dictionary, num_rows, num_cols):
  grid = ""
  count = 0
  total = num_rows * num_cols
  for row in range(1, num_rows+1):
    for col in range(1, num_cols+1):
      grid += str(dictionary[ str(total - row*num_cols + col) ])
      count += 1
      if count % num_cols == 0 and not count == total:
        grid += '\n'
      elif not count == total:
        grid += '\t'
  return grid

grid_ncols = 100
grid_nrows = 100
grid_xllcorner = 501017.5
grid_yllcorner = 5022692.5
#grid_north = 5022570
#grid_west = 524371
#grid_south = 5046074
#grid_east = 500900
grid_cellsize = 235
grid_nodata = -9999

grid_num_cells = grid_ncols * grid_nrows

#Grid headers for ESRI
grid_header = 'ncols %d\n' % grid_ncols
grid_header += 'nrows %d\n' % grid_nrows
grid_header += 'xllcorner %s\n' % grid_xllcorner
grid_header += 'yllcorner %s\n' % grid_yllcorner
grid_header += 'cellsize %s\n' % grid_cellsize
grid_header += 'nodata_value %d\n' % grid_nodata

# Grid headers for GRASS gis
#grid_header = 'north: %s\n' % grid_north
#grid_header += 'south: %s\n' % grid_south
#grid_header += 'east: %s\n' % grid_east
#grid_header += 'west: %s\n' % grid_west
#grid_header += 'rows: %d\n' % grid_nrows
#grid_header += 'cols: %d\n' % grid_ncols
#grid_header += 'null: %d\n' % grid_nodata
#grid_header += ''

out = {}

#-----------------------------------------------------------------------------------------------------     
data_path = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/12alldata_dic/'
data_files = glob.glob(data_path + '*.txt')

for data_file in data_files:

    with open(data_file, 'rb') as telecom_data:
    
      telecom_data = csv.reader(telecom_data, delimiter='\t')
      count = 0
    
      print "Start parsing data..."
    
      for row in telecom_data:
    
        # 0: sid
        # 1: timestamp
        # 2: country_code
        # 3: sms_in
        # 4: sms_out
        # 5: calls_in
        # 6: calls_out
        # 7: internet_traffic
    
        sid = row[0]
        ts = row[1][0:10]
        variable = row[6]
        ts = numpy.longdouble(ts)
        date_time = time.strftime("%Y-%m-%dT%H:00:00+0100", time.gmtime(ts))
    
        # Check empty values and convert values to double
        if variable == '':
          variable = numpy.longdouble(0.0)
        elif type(variable) is str:
          variable = numpy.longdouble(variable)
    
        # Add the timestamp to the dictionary
        if date_time not in out:
          out[date_time] = {}
          # Initialize all the cell ids, ordered from 1 to 10000
          for sid in [str(i) for i in range(1, grid_num_cells+1)]:
            out[date_time][sid] = numpy.longdouble(0.0)
    
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
    print 'Finished parsing data. There are', len(out.keys()), 'timestamps.'
    

    # Write the raster files
    for date_time in sorted(out):
      print 'Writing' , date_time, 'raster file...'
      fcount = 0
    
      assert len(out[date_time]) == grid_num_cells
    
    #  print out[ts]
    
      grid_values = ascii_grid_from_dict( out[date_time], grid_ncols, grid_nrows )
           
      filename = ''.join(['/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/8callsout_ascii_dic/', date_time[0:13],'calls_out','.asc'])
      f = open(filename, 'w')
      f.write(grid_header)
      f.write(grid_values)
      f.close()
      fcount += 1
      print 'just writted', fcount, '1 ascii files...'

# Bye!
print "Done. Enjoy your rasters."