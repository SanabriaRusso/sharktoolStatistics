sharktoolStatistics
===================

Some nice scripts for retrieving statistics from pcap files using Sharktools.

The current script assumes that you have already installed Sharktools. Follow http://luissanabria.me/?p=132 for a very short hint of how the installtion process should go.

Current configuration uses a test.pcap file captured from an Ethernet interface with Wireshark 1.2.7 and Ubuntu 10.04.1.


Parsing .csv files
===================

I've also added an example file, called "parsingCSV.py", which will import a .csv file exported from Wireshark and compute different things. At the moment, it should admit the exaple test.csv file and output a file with the following structure:

0. HostNumber 1. HostIP 2. avgDifferenceOfArrival 3. stdDoA 4. FirstTX 5. LastTX 6. Retransmissions 7. SuccessfullTX

Pending Work
============

The previous version had a script to output the time between packets of the same host. This feature is removed in this version, giving way to more processed statistics in the outout file.





