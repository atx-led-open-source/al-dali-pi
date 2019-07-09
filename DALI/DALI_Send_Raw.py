# send any DALI command as 2 bytes
# enter the 2 bytes as HEX values
# run the Monitor program to observe the response 

import time
import serial
import sys

ser = serial.Serial(
	port ='/dev/ttyS0',
	baudrate = 19200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1,
)

while 1 :
	message = raw_input("input 2 byte DALI command ( like FE00 ): ")  # enter 4 HEX characters

	uppermsg = message.upper()

	ser.write('h%s\n'%(uppermsg))  # write hXXYY where XX is the first DALI byte and YY the 2nd

	x=ser.read(1)

	if x == 'N' :
		print('no response')  
	if x == 'J' :
		y=ser.read(2)
		y=int(y,16)
		print('                      Answer %02x'%(y))
	if x == 'X' :
		print('Framing Error')

	x=ser.read(10)

	
