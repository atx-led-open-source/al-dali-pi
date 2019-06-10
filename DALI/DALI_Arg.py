# send any DALI command as 2 bytes
# enter the 2 bytes as HEX values
# run the Monitor program to observe the response 

import time
import serial
import sys

base = sys.path[0]

ser = serial.Serial(
	port ='/dev/ttyS0',
	baudrate = 19200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1,
)

text = sys.argv[1]

uppermsg = text.upper()

ser.write('h%s\n'%(uppermsg))  # write hXXYY where XX is the first DALI byte and YY the 2nd
time.sleep(.2)
log = open("%s/../DALI_log.txt" % base, "r")
last_line = log.readlines()[-1]
log.close()

print ('%s' % last_line)

	
