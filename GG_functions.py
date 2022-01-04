# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 13:59:46 2021

@author: olehe
"""
import mido
import os
import glob
#import math
#from scipy.io import wavfile
import subprocess
import time
#import random
import numpy as np
import pandas as pd
import sys
'''
test = np.array([[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
,[0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0]
,[1,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0]])


test = np.array([[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
,[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]])

'''

#%% Make some folders

if not os.path.isdir('stimsMidi'):
	os.mkdir('stimsMidi')
if not os.path.isdir('stimsWAV'):
	os.mkdir('stimsWAV')
	

#%% Functions

def generate_midi(inputArray, tempo, loops, saveName):
	
	output = mido.MidiFile(type=1)
	# default is 480 ticks per beat.
	tickResolution = 480
	eventResolution = int(tickResolution / 4)
	tempoTicks = mido.bpm2tempo(tempo)
	
	
	# then write out from the input array
	# GM drums on channel 10 (9 0-indexed), keys 42 hihat 40 snare 36 kick
	# go for 40, 50 and 60 now
	instrKeys = [42, 40, 36]
	
	# so, its 480 ticks per beat (quarter note)
	
	# Just a track to set the tempo
	track = mido.MidiTrack()
	track.append(mido.MetaMessage('set_tempo', tempo=tempoTicks))
	track.append(mido.MetaMessage('end_of_track', time=(32 * eventResolution * loops)))
	
	output.tracks.append(track)
	
	# write one track per instrument
	
	
	count=0
	
	# hold-time for events
	# not implemented yet
	holdTime = int(tempoTicks/32)
	
	# generate tracks
	for key in instrKeys:
		track = mido.MidiTrack()
		
		thisInstr = inputArray[count,]
		count += 1
		previousEventTime = 0
		loopCount = 0
		for loop in range(0, loops):
			for n in range(0, 32):
				thisEventTime = n*eventResolution + (loopCount * eventResolution * 32)
				if thisInstr[n] == 1:
					# insert an event
					deltaTime = thisEventTime - previousEventTime
					track.append(mido.Message('note_on', note=key, velocity=100, channel=9, time=deltaTime))
					track.append(mido.Message('note_off', note=key, velocity=0, channel=9, time=0))
					
					
					previousEventTime = thisEventTime
				#else:
					#lastEventCount += tickResolution
			loopCount += 1
			#track.append(mido.MetaMessage('end_of_track', time=thisEventTime + tickResolution))
		output.tracks.append(track)		
			
	
	output.save(saveName)
	
	
	return

def thisPath():
	thisPath = os.getcwd()
	thisPath = thisPath + '\\bin\\fluidsynth.exe'
	thisPath = thisPath.replace('\\', '/')
	return thisPath

def write_wav(midiName, name):
	#REPLACE THIS WITH YOUR OWN FLUIDSYNTH
	# Attempting now to autofind path
	#thisPath = os.getcwd()
	#print(thisPath)
	#fluidsynth = 'C:/Users/olehe/Documents/GitHub/SanderGenerator/fluidsynth-2.2.2/bin/fluidsynth.exe'
	fluidsynth = thisPath()
	result = subprocess.run([fluidsynth, "-i", "-q", "default.sf2", midiName, "-T", "wav", "-F", name], shell=True)
	# This doesn't always play nice, but it's solved by simply letting it sleep a bit.
	# I've not tested without the sleep, so it could possible work without it.
	time.sleep(1)
	
	return

def normalize(name):
	# yeah no, I'll fix this later
	unnormal = np.fromfile(name, dtype='int16')
	normalized = np.array([unnormal / np.max(np.abs(unnormal)) * 32767], np.int16)
	# work in progress
	return

#%%

def processPattern(pattern, savename='default', tempo=120, loops=1):

	savename.replace(' ', '')
	
	
	#print(output_array)
	#print(self.tempoField.text())
	
	SI = calculate()
	hSI = SI[0]
	wSI = SI[1]
	hSIstring = str(round(hSI, 3))
	wSIstring = str(round(wSI, 3))
	#replace comma with something?
	hSIstring = hSIstring.replace('.', '_')
	hSIformatted = '-hSI-' +hSIstring
	
	wSIstring = wSIstring.replace('.', '_')
	wSIformatted = '-wSI-' +wSIstring

	midiName = 'stimsMidi/' + savename + hSIformatted + wSIformatted + '.mid'
	waveName = 'stimsWAV/' + savename + hSIformatted + wSIformatted + '.wav'
	

	generate_midi(pattern, tempo, loops, midiName)
	write_wav(midiName, waveName)
	
	return

#%% Pattern generation


def generateRandomPattern(minEvents=10, maxEvents=20):
	# just a simple random pattern with some contraints
	
	maxEvents = 20
	minEvents = 10
	# collapse over both instruments? Total between 12 and 18?
	
	# set the hi-hat first
	hihat = np.array([1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,
	        1, 0, 1, 0, 1, 0, 1, 0, 1, 0])

	# now generating them both together
	generate = True
	while generate:
		#snare = np.random.randint(0, 1+1, 32)
		snare = np.round(1-np.random.power(1,32)).astype(int)
		kick = np.round(1-np.random.power(1,32)).astype(int)
		both = np.array([snare, kick]).flatten()
		if sum(both) >= minEvents and sum(both) <= maxEvents:
			generate = False
	
	pattern = np.array([hihat, snare, kick])

	
	return pattern


def searchPattern(SImeasure='W', target=30, timeout=60, minEvents=10, maxEvents=30, verbose=True):
	# select either 'H' for Hoesl's or 'W' for Witek's as a measure.
	if SImeasure == 'H':
		select = 0
	elif SImeasure == 'W':
		select = 1
	else:
		print('Incorrect input for SI measure')
		return
	
	target = float(target)

	generate = True
	timeStart = time.time()
	
	
	count = 0
	if verbose:
		print('Searching for a maximum of ' + str(timeout) + ' seconds')
	while generate:
		count += 1
		thisPattern = generateRandomPattern(minEvents, maxEvents)
		SIs = calculate(thisPattern[1], thisPattern[2])
		thisSI = SIs[select]
		
		if thisSI >= target*0.9 and thisSI <= target*1.1:
			generate = False
			if verbose:
				print('Pattern found.')
		timeNow = time.time()
		if (timeNow-timeStart) > timeout:
			generate=False
			thisPattern = None
			if verbose:
				print('Failed, tested ' + str(count) + ' patterns.')
			
			
	return thisPattern
		
#%% helpful functions

def savePattern(pattern, saveName):
	
	patternA = pattern[1,] # snare
	patternB = pattern[2,] # kick
	
	output = syncopationIndexHoesl(patternA, patternB)
	hWeights = output[1]
	output = syncopationIndexWitek(patternA, patternB)
	wWeights = output[1]
	
	
	
	
	
	colNames = ['hihat', 'snare', 'kick', 'hWeights', 'wWeights']
	data = {'hihat':pattern[0,],
	  'snare':pattern[1,],
	  'kick':pattern[2,],
	  'hWeights':hWeights,
	  'wWeights':wWeights}
	pattern_df = pd.DataFrame(data).T

	#print(name)
	if saveName[0][-4:] != '.csv':
		saveName = name[0] + '.csv'
	
	pattern_df.to_csv(saveName)
	self.report_status('Saved pattern')

		
#%% Syncopation measures
def syncopationIndexHoesl(patternA, patternB, wrap = True, weights = None):
	# default to wrapping, meaning that the first event in the patterns
	
	if weights is not None:
		w = weights
		#should probably check that length is same
	else:
		w = (0, -3,-2, -3, -1, -3, -2, -3, -1, -3, -2, -3, -1,-3, -2, -3, 0, -3,-2, -3, -1, -3, -2, -3, -1, -3, -2, -3, -1,-3, -2, -3)
	 
	
	if wrap:
		patternA = np.append(patternA, patternA[0])
		patternB = np.append(patternB, patternB[0])
		w = np.append(w, w[0])
	
	if len(patternA) != len(w):
		print('Error: Length of pattern needs to be same length as the weights.')
		return
	
	def delta(m,n):
		if(m > n):
			return 1
		else:
			return 0
		
	def phi(a,w,i):
		j = i - 1
		if i >= 3 and a[i-1]== 0.0:
			j = i - 1 - delta(a[i-2],a[i-1])*delta(w[i-2],w[i-1])
		if i >= 5 and a[i-1]==0.0 and a[i-2]==0.0:
			j = i - 1 - 3*(delta(a[i-4],a[i-3])*delta(w[i-4],w[i-3])*delta(a[i-4],a[i-2])*delta(w[i-4],w[i-2])*delta(a[i-4],a[i-1])*delta(w[i-4],w[i-1]))
		return j
	
	def syncopation(s,b,w,B):
		# is B supposed to be length of pattern, with or without loop?
		w_out = np.zeros(len(w), dtype = float)
		c = 2.8 # optimized parameter that 'governs the relationship between metric weight'
		d = 1.6 # two-stream syncopation factor, equals d when both instruments are silent on i, otherwise 0
		h = 1.32 # scaling factor, chosen such that the slope of the linear link function (with perceived syncopation)
		n = len(w)
		S = 0
		for i in range(1,n): 
			j = phi(s,w,i)
			k = phi(b,w,i)
			w_out[i] = (delta(w[i],w[k])*delta(b[k],b[i])*(c**(w[i])-c**(w[k]))
             +delta(w[i],w[j])*delta(s[j],s[i])*(c**(w[i])-c**(w[j])))*d**(delta(1,s[i]+b[i]))
		
		S = sum(w_out)
		return S/B*h, w_out
	
	
	
	output = syncopation(patternA,patternB,w,32)
	

	return output


def syncopationIndexWitek(patternA, patternB, wrap = True, weights = None):

	
	if weights is not None:
		w = weights
		#should probably check that length is same
	else:
		w = (0, -3,-2, -3, -1, -3, -2, -3, -1, -3, -2, -3, -1,-3, -2, -3, 0, -3,-2, -3, -1, -3, -2, -3, -1, -3, -2, -3, -1,-3, -2, -3)
	 
	
	if wrap:
		patternA = np.append(patternA, patternA[0])
		patternB = np.append(patternB, patternB[0])
		w = np.append(w, w[0])
		
	if len(patternA) != len(w):
		print('Error: Length of pattern needs to be same length as the weights.')
		return
	
	def delta(m,n):
		if(m > n):
			return 1
		else:
			return 0
		
	def phi(a,w,i):
		j = i - 1
		if i >= 3 and a[i-1]== 0.0:
			j = i - 1 - delta(a[i-2],a[i-1])*delta(w[i-2],w[i-1])
		if i >= 5 and a[i-1]==0.0 and a[i-2]==0.0:
			j = i - 1 - 3*(delta(a[i-4],a[i-3])*delta(w[i-4],w[i-3])*delta(a[i-4],a[i-2])*delta(w[i-4],w[i-2])*delta(a[i-4],a[i-1])*delta(w[i-4],w[i-1]))
		return j
	
	def syncopation(patternA, patternB, w, B):
		w_out = np.zeros(len(w), dtype=int)
		n = len(w)
		S = 0
		for i in range(1,n):
			j = phi(patternA, w, i)
			k = phi(patternB, w, i)
			Swb = delta(w[i],w[k])*delta(patternB[k],patternB[i])
			Sws = delta(w[i],w[j])*delta(patternA[j],patternA[i])
			Swb1 = delta(1, Swb)
			Wb = w[i] - w[k] + 2 + 3*delta(1,patternA[i]+patternB[i])
			Ws = w[i] - w[j] + 1 + 4*delta(1,patternA[i]+patternB[i])
			
			w_out[i] = Swb*Wb + Sws*Ws*Swb1
		S = sum(w_out)
		return S, w_out
	
	output = syncopation(patternA, patternB, w, 32)
	
	
	return output

def calculate(patternA, patternB, wrap = True, weights = None, verbose=False):
	# Calculates and reports the SI, only the SI
	

	hSI = syncopationIndexHoesl(patternA, patternB, wrap, weights)[0]
	wSI = syncopationIndexWitek(patternA, patternB, wrap, weights)[0]
	if verbose:
		print('hSI is: ' + str(round(hSI,3)) + ' wSI is: ' + str(round(wSI,3)))

	
	return hSI, wSI











