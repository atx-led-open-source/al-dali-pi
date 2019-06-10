# Test the DALI bus
# input the address to control
# then input the level
# send to bus
# loop to input

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

print('\n      ATX LED Consultants Inc - Group  On/Off\n')

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
	print(' Missing Firmware \n\n')
	exit()

x=ser.read(2)
print('HW version: %s'%(x))
y=ser.read(2)
print('FW version: %s'%(y))
x=ser.read(1)

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


while 1 :
	text = input("Which DALI Group ( 0-15 ) : ")
	address = int(text)
	address = (address & 15) *2 + 128
	text = input("      What Level ( 0-254) : ")
	level = int(text)

	ser.write('h%02X%02X\n'%(address,level))   # send level
	time.sleep(.1)

	

