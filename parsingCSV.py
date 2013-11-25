#!/usr/lib/python

##PENDING:
###########Plot an histogram to see the common interarrival values

import csv
from decimal import Decimal
import sys, getopt #to manage arguments passed from CLI
import math

def main(argv):
	inputfile = ''
	outputfile = ''
	rows = 0 #augmenting the rows
	DoA = 0 #Difference of Arrival
	
	#Input file-related columns	
	epochColumn = 1
	sourceAddress = 2
	retryColumn = 3

	#Managing multi source stats
	registered = 0	#Just for having an output file where nodes are numbered for GNUPlot
	substraction = 0
	hostsNumbered = {}
	retransmissions = {}
	sxTransmissions = {}
	interArrivalTimesPerHost = {}
	lastArrivalPerHost = {}
	source = ''

#------Managing the input file------#

	opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="]) #h and i are two of the options accepted (help and input)
								#semicolon next to i means that it accepts an argument (as well as with o)
	for opt,arg in opts:
		if opt == '-h':
			print 'parse.py -i <inputFile>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg

	print 'Processing: ', inputfile
	print 'Outputting into: ', outputfile

#------Processing------#

	with open(inputfile, 'r') as file: #opens the file
		capture = list(csv.reader(file)) #stores the content of the csv as a list
		with open(outputfile, 'w') as statistics:
			for lines in capture:
				#Deprecated, future updates will remove this#
				if capture[rows][sourceAddress] != "":
					source = capture[rows][sourceAddress]
					if rows == 0:	
						DoA = 0
						hostsNumbered[source] = registered
					else:
						DoA = Decimal(capture[rows][epochColumn]) - Decimal(capture[rows-1][epochColumn])
						if source not in hostsNumbered:
							registered += 1
							hostsNumbered[source] = registered
					
					
					###################################################
					#Capturing the time between transmissions per host#
					###################################################
					if source in interArrivalTimesPerHost:
						#Build a dictionary for the arrivals according to each key
						interArrivalTimesPerHost[source].append(float(capture[rows][epochColumn]) - lastArrivalPerHost[source])
					else:
						interArrivalTimesPerHost[source] = []
					
					lastArrivalPerHost[source] = float(capture[rows][epochColumn])
						
						
					#######################################################
					#Capturing successful transmission and retransmissions#
					#######################################################
					if capture[rows][retryColumn] != "Frame is not being retransmitted":
						countRetransmissions(source, retransmissions)
					else:
						countSxTransmissions(source, sxTransmissions)
					
					
					#########################################
					###Writing to output file (deprecated)###
					#########################################
					
					#Writing 1. row 2. host 3. arrivalTime 4. time between arrivals
					statistics.write(str(rows) + ' ' + source + ' ' + str(hostsNumbered[source]) + ' ' + capture[rows][epochColumn] + ' ' + str(DoA) + '\n')
				
				rows += 1

		statistics.close()
	file.close()

	##########################################
	#Printing to a plotable friendly format#
	##########################################	
	outputToFile(interArrivalTimesPerHost)

	###############
	#Screen output#
	###############
	
	print "\n"
	print "###Retransmissions###"
	for key in retransmissions:
		print "---Node ", key, " retransmissions: ", retransmissions[key]
	print "\n"	
	
	print "###Successful Transmissions###"			
	for key in sxTransmissions:
		print "+++Node:", key, " succcessful transmissions: ", sxTransmissions[key]
		print "	  ---Average time between transmissions: ", average(interArrivalTimesPerHost[key]), "s."
		print "		---Standard deviation: ", std(interArrivalTimesPerHost[key]), "s."



#################
####Functions####
#################

def outputToFile(dict):
	listOfValues = []
	for key in dict:
		lines = 0
		nameOfFile = "Node-" + key
		listOfValues = dict[key]
		with open(nameOfFile, 'w') as output:
			for value in listOfValues:
				output.write(str(lines) + ' ' + str(value) + '\n')
				lines += 1
		output.close()
		

def average(listOfValues):	
	if len(listOfValues) > 0:
		numerator = 0
		counter = 0
		for item in listOfValues:
			numerator = numerator + item
			counter = counter + 1
		return numerator/counter
	else:
		return 0

def std(listOfValues):
	if len(listOfValues) > 1:
		numerator = 0
		counter = 0
		mean = average(listOfValues)
		for item in listOfValues:
			numerator = numerator + (math.fabs(item - mean)**(2))
			counter = counter + 1
		return (numerator/(counter - 1))**(0.5)
	else:
		return 0

def countRetransmissions(source, dictionary):
	if source not in dictionary:
		dictionary[source] =  1
	else:
		dictionary[source] +=  1
		
def countSxTransmissions(source, dictionary):
	if source not in dictionary:
		dictionary[source] = 1
	else:
		dictionary[source] += 1

if __name__ == "__main__":
	main(sys.argv[1:])
