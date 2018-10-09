#!/usr/bin/python


from struct import *
import sys

f = open(sys.argv[1],'rb')
a=f.read()
print len(a)
f.close()

i = 0;
if a[i:i+2] != "\xaa\x01":
	sys.exit(-1)

i = i + 2;
beacon_id = unpack('i', a[i:i+4])[0]
print str(beacon_id); #beacon_id
i = i + 4;

i = i + 2;
epoch_time = unpack('i', a[i:i+4])[0]
print str(epoch_time); #epoch time
i = i + 4

i = i + 2;
total_seconds = unpack('h', a[i:i+2])[0]
print str(total_seconds); #total number of seconds available in the packet
i = i + 2;

for x in range(total_seconds):
	records = unpack('B', a[i:i+1])[0];
	i = i + 1;
	#print "SECOND ------------------------------->" + str(x)
	
	eachSecondPacket = "";
	#print str(records) + "-";
	for y in range(records):
		mac = "";
		mac = mac + str(hex(ord(a[i+2])).split('x')[1]) + ":"	
		mac = mac + str(hex(ord(a[i+1])).split('x')[1]) + ":"	
		mac = mac + str(hex(ord(a[i+0])).split('x')[1]) + " "
		rssi = unpack('b', a[i+3:i+4])[0];			
		i = i + 5
		eachSecondPacket = eachSecondPacket + mac + "," + str(rssi) + "&";		

	print eachSecondPacket;
