#
#
# program to set N-Way modes in ATX LED drivers
# see manual for more info ( AL-WS-DR2 etc)
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


print('\n      ATX LED Consultants Inc - Set N-Way mode')
print(' set how N-Way input works')
print(' 0 = rocker N-Way')
print(' 1 = Pushbutton N-Way')
print(' 2 = Split Outputs')
print(' 3 = PIR mode - dimmable')
print(' 4 = PIR mode - 100% ON')
print(' 5 = PIR transmit - transmits* on motion')
print(' 6 = FAN mode')
print(' 7 = Hotel Mode - N-Way turns lights off, transmits*')
print(' 8 = Nighttime - Lights at Minimum Dim for FADE DOWN seconds')
print(' 9 = Autodetect rocker/Pushbutton mode\n')


text = input("Which DALI address ( 0-63, 127=all ) : ")
address = int(text)*2
text = input("                    What mode (0-9)  : ")
SAddr = int(text)

# dtr1, 0 as 0:15
ser.write('hC300\n')
time.sleep(.1)
x=ser.read(2)
ser.write('hA30F\n')
time.sleep(.1)
x=ser.read(2)
ser.write('t%02x81\n'%(address+1))
time.sleep(.1)
x=ser.read(2)
ser.write('hC9%02X\n'%(SAddr))   # write dest
time.sleep(.1)
x=ser.read(2)

