#!/usr/bin/python
#
# program to read the info about all devices on a DALI bus
# loop from 0-63 to get on/off/level and dali type
#

import RPi.GPIO as GPIO
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

GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.IN)
GPIO.setup(6,GPIO.IN)

print('\n      ATX LED Consultants Inc - Fixture Read Status, \n')

if GPIO.input(6) == 0:
	print('Power: Primary Power missing')
else:
	print('Power: Primary Power OK')

if GPIO.input(5) == 0:
	print('Power: Secondary Power missing')
else:
	print('Power: Secondary Power OK')


ser.write('v\n')  # lets get version number first
x=ser.read()
if x == "" :
	print(' Missing Firmware \n')
	exit()

x=ser.read(2)
print('HW version: %s'%(x))
y=ser.read(2)
print('FW version: %s'%(y))
y=ser.read(1)

ser.write('d\n')  # now check if Power is good
x=ser.read(1)
if x == 'D' :
	y=ser.read(2)
	y=int(y,16)
	if y == 0 :
		print('DALI BUS: power is lost')
	if y == 1 :
		print('DALI BUS: power is stuck high')
	if y == 2 :
		print('DALI BUS: power is good')
	if y == 3 :
		print('DALI BUS: power is not yet known')

print( ' ')

while 1:
	x=ser.read(100)

	TotalPower = 0
	CumHours = 0

	i=0
	print('Scan DALI bus')
	while ( i< 64):
		sa2 = ( i * 2 ) + 1
		ser.write('h%02xA0\n' % sa2 )
		x=ser.read(1)
		if( x == 'J'):
			x=ser.read(2)
			y=int(x,16)
			x=ser.read(1)
			ser.write('h%02xA6\n'%(sa2))
			x=ser.read(1)
			z="  "
			if( x == 'J'):
				z=ser.read(2)
			x=ser.read(1)
			ser.write('h%02x99\n'%(sa2))
			x=ser.read(1)
			dt="  "
			if( x == 'J'):
				dt=ser.read(2)
			x=ser.read(1)
			print('address %2d is Model %s Type %s level %3d'%(i,z,dt,y)),

			# dtr1, 0 as 4:3 
			ser.write('hC304\n')
			x=ser.read(2)

			# read Up Time
			ser.write('hA303\n')
			x=ser.read(2)
			ser.write('h%02xC5\n'% sa2) 
			x=ser.read(1)
			if x == 'J' :
				x=ser.read(3)
				Hours=int(x,16)
				ser.write('h%02xC5\n'% sa2) 
				x=ser.read(1)
				x=ser.read(2)
				Hours = Hours + 256*int(x,16)
				if( Hours != 65535 ) :
					print('Up: %5d '% Hours ),
			x=ser.read(1)

			# read On Time
			ser.write('hA305\n')
			x=ser.read(2)
			ser.write('h%02xC5\n'% sa2) 
			x=ser.read(1)
			if x == 'J' :
				x=ser.read(3)
				Hours=int(x,16)
				ser.write('h%02xC5\n'% sa2) 
				x=ser.read(1)
				x=ser.read(2)
				Hours = Hours + 256*int(x,16)
				if( Hours != 65535 ) :
					print('On: %5d '% Hours ),
					CumHours = CumHours + Hours
			x=ser.read(1)

			ser.write('hA307\n')
			x=ser.read(2)
			ser.write('h%02xC5\n'% sa2) 
			x=ser.read(1)
			if x == 'J' :
				x=ser.read(3)
				Power=int(x,16)
				ser.write('h%02xC5\n'% sa2) 
				x=ser.read(1)
				x=ser.read(2)
				Power = 256*int(x,16) + Power
				if( Power != 65535 ) :
					print('Usage: %7ld Wh '%(Power*24)),
					TotalPower = TotalPower + Power*24
			x=ser.read(1)

			print(' ')

		else :
			x=ser.read(1)
		i = i+1

	if TotalPower > 0 :
		print( ' Total Power = %ld kWh ' % (TotalPower/1000))	
		print( ' Operating Hours = %d ' % CumHours )	
		print( ' Effective Dimming = %d pct ' % (TotalPower*100/(CumHours*24)))	