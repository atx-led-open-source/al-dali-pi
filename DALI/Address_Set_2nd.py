#
#
# program to set the 2nd address in a ATX LED wall switch
# the 2nd address is used by the N-Way switch with this mode
#


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


print('\n      ATX LED Consultants Inc - Set 2nd Address \n')

text = input("Which DALI address ( 0-63, 127=all ) : ")
address = int(text)*2
text = input("    What destination ( 0-63, 127, 255) : ")
SAddr = int(text)

# dtr1, 0 as 0:16
ser.write('hC300\n')
time.sleep(.1)
x=ser.read(2)
ser.write('hA310\n')
time.sleep(.1)
x=ser.read(2)
ser.write('t%02x81\n'%(address+1))
time.sleep(.1)
x=ser.read(2)
ser.write('hC9%02X\n'%(SAddr))   # write dest
time.sleep(.1)
x=ser.read(2)

