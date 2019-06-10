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

print('\n\n')
print('      ATX LED Consultants Inc - Fixture Minimum ')
print('')
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


text = input("Which DALI address ( 0-63, 127=All) : ")
address = int(text)*2+1

text = input("                   What Minimum Dim : ")
dim = int(text)

ser.write('hA3%02X\n'%(dim)) # load DTR
time.sleep(.1)
ser.write('t%02X2B\n'%(address))  # set DTR to Min level
time.sleep(.1)

# now cycle until ^C

print('Now Cycle Min / Max until ^C exit')

while 1 :
	ser.write('h%02X06\n'%(address))
	time.sleep(2)
	ser.write('h%02X05\n'%(address))
	time.sleep(2)
