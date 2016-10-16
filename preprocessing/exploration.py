#!/usr/bin/env python

"""
------------------------------------------------------------------------------------------------------------------
TELECOM DATA PREPROCESSING AND EXPLORATION

File name: exploration.py 
Description: This script makes data exploration for telecom Open data 2013.
Author:Carolina Arias Munoz
Date Created: 30/07/2016
Date Last Modified: 30/07/2016
Python version: 2.7
------------------------------------------------------------------------------------------------------------------
"""
#import sys
import pandas
import numpy
import matplotlib
matplotlib.rcParams['agg.path.chunksize'] = 10000
import matplotlib.pyplot as plt
import glob
matplotlib.style.use('ggplot')

#path for the csv files
log_path = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/scripts/2exploration/'
data_path = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/csv/'
data_path_outliers = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/csv/stats/outliers/'
plots_path = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/csv/stats/fig/'
stats_path = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/csv/stats/'
#path for the normalized csv files
data_path_norm = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/csv/csvnorm/'
data_path_norm_week = '/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/data/sms-call-internet-mi/csv/csvnorm/byweek/'


#strings of paths
data_files = glob.glob(data_path + '*.txt')

##Creating log file
#sys.stdout = open (log_path + 'explorationlog.txt', 'w')

#------------------------------------------TELECOM DATA -----------------------------------------------------  
for data_file in data_files:
    #obtainning just the name of the variable
    varname = data_file[93:110]
    # eliminating '.txt'
    varname = varname.replace('.txt', '')
    #variables.append(varname)
    with open(data_file, 'rb') as data_file:
        #Importing data
        df = pandas.read_table(data_file, sep='\t', names=['date_time','cellid', varname]) 
        # Setting date_time as data frame index
        df = df.sort_values(by ='date_time', axis=0, ascending=True)
        df = df.reset_index(drop=True) 
        df = df.set_index(['date_time'], drop = False)
        #------------------------------#
        # STATISTICS AND PLOTS
        #------------------------------#
        #some info on the data
		print 'Some info on ' + varname + ' dataframe'
		print ''
		#df.info()
		print 'Creating time index... it will take a while...'
		#creating time index
		df = df.set_index(pandas.DatetimeIndex(df['date_time']))
		print 'Time index created for ' + varname
		print ''
        print 'Statitics on ' + varname + ':'
        #calculate statistics
        statistics = df[varname].describe()
        print statistics
		print ''
		#saving the statistics in a csv file
		statistics.to_csv(stats_path + varname + '.csv', sep=',')
		print 'Plots on ' + varname
		#simple plot
        mask = (df['date_time'] >= '2013-11-01T00:00:00+0100') & (df['date_time'] < '2013-12-01T00:00:00+0100')
        dfnov = df.loc[mask]
        line = dfnov['sms_outlog'].plot(kind='line', title = varname + ' 2013', figsize = (30,10))
        fig1 = line.get_figure()
        fig1.savefig(plots_path + 'sms_outlog_line.png',dpi=300)
        plt.close(fig1)
        #density plot
		density = df[varname].plot(kind='density', title = varname + ' 2013. Density Plot')
		fig2 = density.get_figure()
		fig2.savefig(plots_path + varname + '_density.png',dpi=300)
		plt.close(fig2)
		#histogram
		histplot = df[varname].plot(kind='hist',title = varname + ' 2013. Histogram') 
		fig3 = histplot.get_figure()
		fig3.savefig(plots_path + varname + '_hist.png',dpi=300)
		plt.close(fig3)
		#boxplot
		boxplot = df[varname].plot(kind='box', title = varname + ' 2013. Boxplot')
		fig4 = boxplot.get_figure()
		fig4.savefig(plots_path + varname + '_boxplot.png',dpi=300)
		plt.close(fig4)
        Checking data for an specific location
		cellid = 5999
		dfcell = df[(df.cellid == cellid)]        
		line = dfcell[varname].plot(kind='line', title = varname + ''+ ' cellid' +' 2013', figsize = (40,20))
		fig1 = line.get_figure()
		fig1.savefig(plots_path + varname + '_line.png',dpi=300)
		plt.close(fig1)
        #print boxplot
        #---------------------------------------------------#
        # Cheking OUTLIERS
        #---------------------------------------------------#
        #standard deviaton of data
        std = df[varname].std()
        #Interquartile range
        iqr = 1.35 * std
        #25% quartile
        q1 = statistics.ix['25%']
        #75% quartile
        q3 = statistics.ix['75%']
        #superior outer fence limit
        sup_out_lim = q3 + (25 * iqr)
        mask = df[varname] >= sup_out_lim 
        df_so = df.loc[mask]
        df_so.to_csv(path_or_buf = data_path_outliers + varname + 'so.csv', sep=',', index = False)

 

#sys.stdout.close()
print 'enjoy! bye'
