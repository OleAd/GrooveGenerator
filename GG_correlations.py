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




#%% The goal of this section is to just create a lot of patterns and correlate
# between Hoesl's and Witek's measure of syncopation.


# Should patterns be stored too?
# There are a totalt of 65536 permutations of each instrument row given 16 events
# only kick and snare count, and only if there's at least one event,
# meaning there are 65535 + 65535 = 131070 combinations 
# could just generate them all
# BUT, for 32 then it is: 4294967296 * 2 - 2, which is just too much... OR IS IT?
# Could give it a try...
# estimates 0.0024 s per rhythm
# so, that means around 119 days of 24 hour computing. 
# Down to 2 weeks with parallelization, don't want to commit to that


# initiate empty dictionary
allData = {}
random.seed(42)


maxNum = 2**32

hihats = np.tile(np.array([1,0]),16)



# random sampling without replacement from all possibilities

patterns = 10000
numbers = range(1, maxNum)

snareValues = random.sample(numbers, patterns)
kickValues = random.sample(numbers, patterns)

count = 0

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
	


allData_df = pd.DataFrame.from_dict(allData, 'index')	

#%% Plots and statistics

sns.scatterplot(data=allData_df, x='wSI', y='hSI')	
pg.corr(allData_df['wSI'], allData_df['hSI'])


sns.scatterplot(data=allData_df, x='wSI', y='events')
sns.scatterplot(data=allData_df, x='hSI', y='events')	
		
	




