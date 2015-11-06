# Pradyumna Kikkeri, CSCI 3202 Fall 2015
# Assignment 7, Prof. Hoenigmann, due Friday, November 6, 2015

import random
import re


class Node(object):
	def __init__(self, name):
		self.name = name
		self.prior = None
		self.probDist = None

#From net in assignment writeup
cloudy = Node('Cloudy')
cloudy.prior = 0.5

rainy = Node('Rainy')
rainy.probDist = {True: 0.8, False: 0.2}

sprinkler = Node('Sprinkler')
sprinkler.probDist = {True: 0.1, False: 0.5}

wetGrass = Node('WetGrass')
wetGrass.probDist = {(True, True): 0.99, (True, False): 0.9, (False, True): 0.9, (False, False): 0.0}

def Problem1Prior(samples):
	samplesize = len(samples)
	cloudy_days = 0

	for sample in samples:
		if sample['clouds'] == True:
			cloudy_days += 1

	print '\n1a) P(c = true) = ', cloudy_days/float(samplesize), '\n'

	rainy_days = 0
	cloudy_and_rainy_days = 0

	for sample in samples:
		if sample['rain'] == True:
			rainy_days += 1
			if sample['clouds'] == True:
				cloudy_and_rainy_days += 1

	print '1b) P(c = true | rain = true) = ', cloudy_and_rainy_days/float(rainy_days), '\n'
	

	
	wet_sprinkler_days = 0
	wet_grass_days = 0

	for sample in samples:
		if sample['wet'] == True:
			wet_grass_days += 1
			if sample['sprinkle'] == True:
				wet_sprinkler_days += 1

	print '1c) P(s = true | w = true) = ', wet_sprinkler_days/float(wet_grass_days), '\n'

	sprinkler_days = 0
	cloudy_wet_days = 0

	for sample in samples:
		if sample['clouds'] == True:
			if sample['wet'] == True:
				cloudy_wet_days += 1
				if sample['sprinkle'] == True:
					sprinkler_days += 1

	print '1d) P(s = true | c = true, w = true) = ', sprinkler_days/float(cloudy_wet_days), '\n'

def Problem3Rejection(rejection_samples):
	cloudy_days = 0

	for rs in rejection_samples:
		if rs <= cloudy.prior:
			cloudy_days += 1
	
	print '3a) P(c = true) = ', cloudy_days/float(100), '\n'


	i = 0
	buf = []

	while True:
		if i >= 99:
			break

		ins = {}
		current = rejection_samples[i]
		if current <= cloudy.prior:
			ins['clouds'] = True
		else:
			ins['clouds'] = False
		i += 1
		current = rejection_samples[i]
		if current <= rainy.probDist[ins['clouds']]:
			ins['rain'] = True
			buf.append(ins)
		else:
			ins['rain'] = False
		i+= 1

	cloudy_days = 0

	for b in buf:
		if b['clouds'] == True:
			cloudy_days += 1

	print '3b) P(c = true | rain = true) = ', cloudy_days/float(len(buf)), '\n'

	i = 0
	buf = []

	while True:
		if i >= 96:
			break
		ins = {}
		current = rejection_samples[i]
		if current <= cloudy.prior:
			ins['clouds'] = True
		else:
			ins['clouds'] = False
		cloudyval = ins['clouds']
		i += 1
		current = rejection_samples[i]
		if current <= sprinkler.probDist[cloudyval]:
			ins['sprinkle'] = True
		else:
			ins['sprinkle'] = False
		sprinkleval = ins['sprinkle']
		i += 1
		current = rejection_samples[i]
		if current <= rainy.probDist[cloudyval]:
			ins['rain'] = True
		else:
			ins['rain'] = False
		rainval = ins['rain']
		i += 1
		if not sprinkleval and not rainval:
			continue
		current = rejection_samples[i]
		if current <= wetGrass.probDist[sprinkleval, rainval]:
			ins['wet'] = True
			buf.append(ins)
		i += 1

	sprinkler_days = 0

	for b in buf:
		if b['sprinkle'] == True:
			sprinkler_days += 1

	print '3c) P(s = true | w = true) = ', sprinkler_days/float(len(buf)), '\n'

	

	i = 0
	buf = []

	while True:
		if i >= 96:
			break
		ins = {}
		current = rejection_samples[i]
		if current <= cloudy.prior:
			ins['clouds'] = True
		else:
			i += 1
			continue
		i += 1
		current = rejection_samples[i]
		if current <= sprinkler.probDist[True]:
			ins['sprinkle'] = True
		else:
			ins['sprinkle'] = False
		sprinkleval = ins['sprinkle']
		i += 1
		current = rejection_samples[i]
		if current <= rainy.probDist[True]:
			ins['rain'] = True
		else:
			ins['rain'] = False
		rainval = ins['rain']
		i += 1
		if not sprinkleval and not rainval:
			continue
		current = rejection_samples[i]
		if current <= wetGrass.probDist[sprinkleval, rainval]:
			ins['wet'] = True
			buf.append(ins)
		i += 1

	sprinkler_days = 0
	for b in buf:
		if b['sprinkle'] is True:
			sprinkler_days += 1


	print '3d) P(s = true| c = true, w = true) = ', sprinkler_days/float(len(buf)), '\n'


def main():

	sample_collection = [0.82,	0.56,	0.08,	0.81,	0.34,	0.22,	0.37,	0.99,	0.55,	0.61,	0.31,	0.66,	0.28,	1.0,	0.95,	
	0.71,	0.14,	0.1,	1.0,	0.71,	0.1,	0.6,	0.64,	0.73,	0.39,	0.03,	0.99,	1.0,	0.97,	0.54,	
	0.8,	0.97,	0.07,	0.69,	0.43,	0.29,	0.61,	0.03,	0.13,	0.14,	0.13,	0.4,	0.94,	0.19, 	0.6,	
	0.68,	0.36,	0.67,	0.12,	0.38,	0.42,	0.81,	0.0,	0.2,	0.85,	0.01,	0.55,	0.3,	0.3,	0.11,	
	0.83,	0.96,	0.41,	0.65,	0.29,	0.4,	0.54,	0.23,	0.74,	0.65,	0.38,	0.41,	0.82,	0.08,	0.39,	
	0.97,	0.95,	0.01,	0.62,	0.32,	0.56,	0.68,	0.32,	0.27,	0.77,	0.74,	0.79,	0.11,	0.29,	0.69,	
	0.99,	0.79,	0.21,	0.2,	0.43,	0.81,	0.9,	0.0,	0.91,	0.01]

	buf = []
	i = 0

	while i < len(sample_collection):
		ins = {}

		if sample_collection[i] <= cloudy.prior:
			ins['clouds'] = True
		else:
			ins['clouds'] = False

		i += 1
		cloudyval = ins['clouds']

		if sample_collection[i] <= sprinkler.probDist[cloudyval]:
			ins['sprinkle'] = True
		else:
			ins['sprinkle'] = False
		i += 1

		if sample_collection[i] <= rainy.probDist[cloudyval]:
			ins['rain'] = True
		else:
			ins['rain'] = False
		i+= 1
		sprinkleval = ins['sprinkle']
		rainval = ins['rain']

		if sample_collection[i] <= wetGrass.probDist[sprinkleval, rainval]:
			ins['wet'] = True
		else:
			ins['wet'] = False

		i += 1

		buf.append(ins)

	print "\nProblem 1 is prior sampling, Problem 3 is rejection sampling. Problems 2 and 4\n are answered in the writeup.\n"
	Problem1Prior(buf)
	Problem3Rejection(sample_collection)

if __name__ == '__main__':
	main()