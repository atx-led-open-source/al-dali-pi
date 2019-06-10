# program to monitor the DALI bus and report status
# displays the traffic on the DALI Bus
# 

import RPi.GPIO as GPIO
import time
import serial
ProgTimes = [ 0, 7, 10, 14, 20, 28, 40, 56, 80, 113, 160, 226, 320, 452, 640, 900 ]

ser = serial.Serial(
	port ='/dev/ttyS0',
	baudrate = 19200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=86400,
)

serfast = serial.Serial(
	port ='/dev/ttyS0',
	baudrate = 19200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1,
)


# program to monitor and print out all DALI bus traffic.

GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.IN)
GPIO.setup(6,GPIO.IN)

print('\n\n')
print('      ATX LED Consultants Inc - DALI bus debugger - log one address')
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
x=serfast.read()
if x == "" :
	print(' Missing Firmware \n\n')
	exit()

x=ser.read(2)
print('HW version: %s'%(x))
y=ser.read(2)
print('FW version: %s\n'%(y))

text = input("Which DALI address ( 0-63, 127=all ) : ")
address = int(text)*2



print('')
print('Destination <= Data ')
print('A = short address')
print('G = Group')
print('all = Broadcast')
print('')


ser.write('d\n')  # now check if Power is good


nl = 0
DT = 0
DT1 = 0
DT2 = 0

while 1:
	x=ser.read(1)

	if x == 'H' :
		if nl != 0 :
			print('%3d nak'%(nl))
			nl = 0
		x=ser.read(2)
		SAddr =int(x,16)
		yt=ser.read(2)
		y=int(yt,16)
		if ( SAddr & 1 )== 0 :  # arc command
			if SAddr & 128 == 0 :
				if SAddr == address:
					print('A%2d <= level %3d'%(SAddr/2,y))
			if SAddr == 255 :
				print('all <= level %3d'(y))
		else:
			Cmd = "Command %3d" % y
			if DT < 16:
				Time = ProgTimes[DT]

			if y == 0:
				Cmd = "Off"
			if y == 6:
				Cmd = "Min level"
			if y == 5:
				Cmd = "Max level"
			if y == 35:
				Cmd = "Set Mode to %d " % (DT)
			if y == 46:
				Cmd = "Fade Up %d seconds" % ( Time )
			if y == 47:
				Cmd = "Fade Down %d seconds" % ( Time )
			if y == 49:
				Cmd = "UPS Mode - Temporary Max Light %d pct " % (DT*100/254)
			if y == 50:
				Cmd = "Fan Idle speed %d pct " % (DT*100/254)
			if y == 51:
				if(DT) :
					Cmd = "Fan Delay %d seconds" % ( Time )
				else :
					Cmd = "Fan Delay disabled "
			if y == 52:
				if(DT) :
					Cmd = "Fan Hold %d seconds" % ( Time*4 )
				else :
					Cmd = "Fan disabled "
			if y == 53:
				Cmd = "Fan Speed %d pct " % (DT*100/255)
			if y == 129:
				Cmd = "Enable Memory Write"
				if SAddr == address :
					MemoryWriteOn = 1
			if y == 197:
				Cmd = "Read Memory"
			if y == 226:
				Cmd = "Activate Color"
			if y == 231:
				w = 4000 -  ( 368 - DT1 * 256 - DT ) * 5.2
				Cmd = "Set Color temp to %4d K " % (w)

			z = SAddr/2+176 

			if SAddr & 128 == 0 :
				if SAddr == address +1 :
					print('A%2d <= %s '%(SAddr/2,Cmd))
			if SAddr & 224 == 160 :
				if z == 257:
					DT = y
				else:
					print('all <= Send command %3d data %3d '%(z,y))
			if SAddr & 224 == 192 :

				if z == 272 :
					print('all <= Enable Device Type %3d'%(y) )
				elif z == 273 :
					DT1 = y 
				elif z == 274 :
					DT2 = y
				elif z == 276:
					if MemoryWriteOn == 1 :
	 					print('all <= Write %3d to Memory at %3d:%3d'%(y,DT1,DT) )
					MemoryWriteOn = 0
				else :
					print('all <= Send command %3d data %3d '%(z,y))
			if SAddr == 255 :
				print('all <= %s '%(Cmd))
	if x == 'D' :
		if nl != 0 :
			print('%3d nak'%(nl))
			nl = 0
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
	if x == 'N' :
		print('.'),  # normal no response to most commands, just a dot
		nl = nl + 1
	if x == 'J' :
		if nl != 0 :
			print('%3d nak'%(nl))  
			nl = 0
		y=ser.read(2)
		y=int(y,16)
		if SAddr == address+1 :
			print('                      Answer %02x'%(y))
	if x == 'X' :
		if nl != 0 :
			print('%3d nak'%(nl))
			nl = 0
		print('Framing Error')
	if x == 10 :
		print('newline')

