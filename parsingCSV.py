#!/usr/lib/python
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
	epochColumn = 6
	sourceAddress = 1
	retryColumn = 7

	#Managing multi source stats
	registered = 0	
	hostsNumbered = {}
	retransmissions = {}
	sxTransmissions = {}
	source = ''
	transmitter = ''

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
					
					#Capturing successful transmission and retransmissions
					if capture[rows][retryColumn] != "Frame is not being retransmitted":
						if source not in retransmissions:
							retransmissions[source] =  1
						else:
							retransmissions[source] +=  1
					else:
						if source not in sxTransmissions:
							sxTransmissions[source] = 1
						else:
							sxTransmissions[source] += 1
						
					#Writing 1. row 2. host 3. arrivalTime 4. time between arrivals
					statistics.write(str(rows) + ' ' + source + ' ' + str(hostsNumbered[source]) + ' ' + capture[rows][epochColumn] + ' ' + str(DoA) + '\n')
				
				else:	#Unrecognised source address
					continue
				
				rows += 1

		statistics.close()
	file.close()
	print "\n"
	print "###Retransmissions###"
	for key in retransmissions:
		print "---Node ", key, " retransmissions: ", retransmissions[key]
	print "\n"	
	print "###Successful Transmissions###"
			
	for key in sxTransmissions:
		print "+++Node ", key, " succcessful transmissions: ", sxTransmissions[key]

if __name__ == "__main__":
	main(sys.argv[1:])
