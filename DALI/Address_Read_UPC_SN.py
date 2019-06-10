#
#
# program to read the info about one DALI device
# display the serial number, UPC code and firmware versions
#
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

print('\n      ATX LED Consultants Inc - Fixture Read UPC, Version, SN \n')

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
print('Hat HW version: %s'%(x))
y=ser.read(2)
print('Hat FW version: %s'%(y))
y=ser.read(1)


if len(sys.argv) < 2 :
	text = input("input device to read : ")
else:
	text = sys.argv[1]
device = int(text)*2+1

# dtr1, 0 as 0:3 
ser.write('hC300\n')
time.sleep(.1)
x=ser.read(2)
ser.write('hA303\n')
time.sleep(.1)
x=ser.read(2)

# read memory - upc msb
ser.write('h%02xC5\n'%device) 
time.sleep(.1)
x=ser.read(1)
x=ser.read(3)
UPC=int(x,16)
ser.write('h%02xC5\n'%(device)) 
time.sleep(.1)
x=ser.read(1)
x=ser.read(3)
UPC = UPC*256+int(x,16)
ser.write('h%02xC5\n'%(device)) 
time.sleep(.1)
x=ser.read(1)
x=ser.read(3)
UPC = UPC*256+int(x,16)
ser.write('h%02xC5\n'%(device)) 
time.sleep(.1)
x=ser.read(1)
x=ser.read(3)
UPC = UPC*256+int(x,16)
ser.write('h%02xC5\n'%(device)) 
time.sleep(.1)
x=ser.read(1)
x=ser.read(3)
UPC = UPC*256+int(x,16)
ser.write('h%02xC5\n'%(device)) 
time.sleep(.1)
x=ser.read(1)
x=ser.read(3)
UPC = UPC*256+int(x,16)
if( UPC != 281474976710655 ) :
	print('UPC: %ld'%(UPC))
else:
	print(' No UPC')

ser.write('h%02xC5\n'%(device)) 
time.sleep(.1)
x=ser.read(1)
x=ser.read(2)
print('FW version: %s'%(x))
ser.write('h%02xC5\n'%(device)) 
time.sleep(.1)
x=ser.read(2)
x=ser.read(2)
print('HW version: %s'%(x))

ser.write('h%02xC5\n'%(device)) 
time.sleep(.1)
x=ser.read(2)
x=ser.read(3)
SN= int(x,16)
ser.write('h%02xC5\n'%(device)) 
time.sleep(.1)
x=ser.read(1)
x=ser.read(3)
SN = SN*256+int(x,16)
ser.write('h%02xC5\n'%(device)) 
time.sleep(.1)
x=ser.read(1)
x=ser.read(3)
SN = SN*256+int(x,16)
ser.write('h%02xC5\n'%(device)) 
time.sleep(.1)
x=ser.read(1)
x=ser.read(3)
SN = SN*256+int(x,16)
if(SN != 4294967295):
	print('SN version: %08X'%(SN))

ser.write('h%02xC5\n'%(device)) 
time.sleep(.1)
x=ser.read(1)
x=ser.read(3)
y=int(x,16)
if(y != 255):
	print('N-Mode: %d'%(y))

ser.write('h%02xC5\n'%(device)) 
time.sleep(.1)
x=ser.read(1)
x=ser.read(3)
y=int(x,16)
if( y < 64):
	print('2nd Short Address is : %d'%(y))
elif (y == 127):
	print('2nd is Broadcast')
elif (y < 127):
	print('2nd is Group : %d'%(y&15))
elif (y == 255):
	print('2nd SA/Group is disabled')
print('\n\n')

	
