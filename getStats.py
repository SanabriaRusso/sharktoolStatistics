#!/usr/lib/python

import pyshark
from collections import defaultdict
import sys
import math

def main(arvg):

	capture = pyshark.read('BECA.pcap', ['frame.number', 'frame.time', 'ip.addr', 'frame.time_delta', 'wlan.bssid', 'wlan.fc.retry'], 'ip.version eq 4')
	capture = list(capture)
	print "The length of the file is of ",len(capture)," lines."

	###Variables
	statistics = defaultdict(list)
	counter = 0
	meanInterArrivalTime = defaultdict(list)

	###Filling the statistics dictionary of lists
    ###First index in capute list, should be an int. That's why "counter" exists. Fix needed.
	for lines in capture:
		statistics[capture[counter]['ip.addr'][0]].append(capture[counter]['frame.time'])		
		counter = counter + 1

	for k in statistics:
		#print statistics[k]
		perHostStatistics = statistics[k]	#Reading statistics from one key (ergo host) at a time.
		previous = 0
		DoA = 0		##Difference of Arrival
		lsDoA = []	##Difference of Arrival list of values (used for computing metrics)
		
		###Computing###
		if len(perHostStatistics) > 2:
			print "\n+++Entering for node: ", k
			for item in perHostStatistics:
				substraction = item - previous	
				if substraction == item:	#this causes an error
					substraction = 0	#maybe should fix it
				lsDoA.append(substraction)
				previous = item
			print "+++Node: ", k ," the average DoA is: ", "%.9f" % average(lsDoA)
			print "+++Node: ", k ," with a standard deviation of", "%.9f" % std(lsDoA)
		else:
			print "\n---Node " ,k , " does not have enough readings to be counted."
			continue
		

def average(listOfValues):	
	numerator = 0
	counter = 0
	for item in listOfValues:
		numerator = numerator + item
		counter = counter + 1
	return numerator/counter


def std(listOfValues):
	numerator = 0
	counter = 0
	mean = average(listOfValues)
	for item in listOfValues:
		numerator = numerator + (math.fabs(item - mean)**(2))
		counter = counter + 1
	return (numerator/(counter - 1))**(0.5)


if __name__ == "__main__":
	main(sys.argv[1:])
