# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 12:52:01 2022

@author: olehe
"""
import timeit

import sys
import os
import time
import numpy as np
import pandas as pd
import seaborn as sns
import pingouin as pg


import GG_functions

import random
import time




#%% The goal of this section is to just create a lot of patterns and correlate
# between Hoesl's and Witek's measure of syncopation.

'''
# Store the patterns as integers, then just convert to binary for the pattern

There's 2^64 possible permuations.
32 dropped due to single event at same time
64 dropped to single events, per instrument
Assuming it takes 4 seconds to play the pattern at 120 BPM
Then : ((2**64 - 96) * 4 / 3600) / 24 / 365  (to get it in years)
Still a huge number. Let's assume that the entire population of Denmark does it
Population is around 5.8 million

((2**64 - 96) * 4 / 3600) / 24 / 365 / 5800000

In compute time
((2**64 - 96) * 0.00176) / 3600 / 24 / 365 / 1000000 / 16


'''
	


# initiate empty dictionary
allData = {}
random.seed(42)


maxNum = 2**32

hihats = np.tile(np.array([1,0]),16)



# random sampling without replacement from all possibilities

patterns = 1000000
# 500k patterns should take around 15 minutes, single-threaded.
# estimated 17.6 ms per iteration
numbers = range(1, maxNum)

snareValues = random.sample(numbers, patterns)
kickValues = random.sample(numbers, patterns)

count = 0
tic = time.time()
for n in range(0, len(snareValues)):
	snare = format(snareValues[n],'b').zfill(32)
	kick = format(kickValues[n],'b').zfill(32)
	

	snare = np.array(list(snare), 'int16')
	kick = np.array(list(kick), 'int16')
	
	
	hSI, wSI = GG_functions.calculate(snare, kick)
	eventCount = sum(snare)+sum(kick)
	
	allData[count] = {'hSI':hSI,
				'wSI':wSI,
				'events':eventCount,
				'snareN':snareValues[n],
				'kickN':kickValues[n]}
	count += 1

toc = time.time()
# roughly 1.8 ms per loop.

allData_df = pd.DataFrame.from_dict(allData, 'index')

allData_df.to_csv('1m_patterns.csv')
	

#%% Plots and statistics

sns.scatterplot(data=allData_df, x='wSI', y='hSI')	
pg.corr(allData_df['wSI'], allData_df['hSI'])


sns.scatterplot(data=allData_df, x='wSI', y='events')
sns.scatterplot(data=allData_df, x='hSI', y='events')	
		
	




