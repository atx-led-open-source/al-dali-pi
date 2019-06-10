# This program sets a fixture fade time
# enter the decimal address and fade time/rate
# enters test mode until user exits


import time
import serial
import sys

ProgTimes = [ 0, 7, 10, 14, 20, 28, 40, 56, 80, 113, 160, 226, 320, 452, 640, 900 ]


ser = serial.Serial(
	port ='/dev/ttyS0',
	baudrate = 19200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1,
)

text = input("Which DALI address 0-63, 127=all : ")
address = int(text)*2+1

if address < 64 :
	ser.write('h%02xA5\n'%(address))   # read current setting
	x=ser.read(1)
	if x == 'J' :
		text=ser.read(2)
		down = int(text,16)&15
		Down = ProgTimes[down]

		up = int(text,16)/16
		Up = ProgTimes[up]

		print('Address %d is set to %d Up and %d Down seconds'% (address/2,Up,Down) )
		text=ser.read(1)
	if x == 'N' :
		print(' No device at that address')
		exit()		

up = 20
while up > 15 :
	text = input("Fade setting   (up) 0-15 : ")
	up = int(text)
	Up = ProgTimes[up]
	print('Set to %d Up seconds'% (Up) )


down = 20
while down > 15 :
	text = input("Fade setting (down) 0-15 : ")
	down = int(text)
	Down = ProgTimes[down]
	print('Set to %d Down seconds'% (Down) )


ser.write('hA3%02X\n'%(up))   # load DTR
time.sleep(.1)
ser.write('t%02X2E\n'%(address))   # DTR to fade time - send twice
time.sleep(.1)
ser.write('hA3%02X\n'%(down))   # load DTR
time.sleep(.1)
ser.write('t%02X2F\n'%(address))   # DTR to fade rate - send twice
time.sleep(.1)

print('Cycle on/off until ^C break')

# now cycle

while 1 :
	ser.write('h%02X06\n'%(address))
	time.sleep(2)
	ser.write('h%02X05\n'%(address))
	time.sleep(2)

	

