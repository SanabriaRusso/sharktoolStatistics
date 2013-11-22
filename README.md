sharktoolStatistics
===================

Some nice scripts for retrieving statistics from pcap files using Sharktools.

The current script assumes that you have already installed Sharktools. Follow http://luissanabria.me/?p=132 for a very short hint of how the installtion process should go.

Current configuration uses a test.pcap file captured from an Ethernet interface with Wireshark 1.2.7 and Ubuntu 10.04.1.


Parsing .csv files
===================

I've also added an example file, called "parsingCSV.py", which will import a .csv file exported from Wireshark and compute different things. At the moment, it should admit the exaple test.csv file and output a file with the following structure:

columns - descriptions:

1-row, 2-host, 3-arrivalTime, 4-time between two consecutive arrivals of any source (as if seen from the channel's perspective)

It also will print on the display the number of retransmitted frames.


Pending Work
============

As with the pyshark example, I'm still to write the time between transmitted packets of the same host. 
