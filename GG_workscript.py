# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 11:23:59 2021

@author: olehe
"""



import GG_grooveIndex
from GrooveGenerator_WIP import GrooveGenerator
import seaborn as sns
import numpy as np


generator = GrooveGenerator()

testPattern = np.array([[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,
        1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
       [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 1, 1, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1,
        0, 1, 1, 1, 0, 1, 1, 1, 1, 0]])


numSearch = 500
hSI = []
wSI = []
GI = []

for n in range(0, numSearch):
	generator.generateRandomPattern()
	thisPattern = generator.getPattern()
	thisInfo = generator.calculate()
	hSI.append(thisInfo[0])
	wSI.append(thisInfo[1])
	GI.append(thisInfo[2])



sns.scatterplot(x=GI, y=wSI)



