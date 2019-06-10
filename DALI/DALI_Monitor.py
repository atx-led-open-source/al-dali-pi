#!/usr/bin/python
# program to monitor the DALI bus and report status
# displays the traffic on the DALI Bus
# 

import RPi.GPIO as GPIO
import time
import datetime
import serial
import sys

base = sys.path[0]

ProgTimes = [ 0, 7, 10, 14, 20, 28, 40, 56, 80, 113, 160, 226, 320, 452, 640, 900 ]

ser = serial.Serial(
	port ='/dev/ttyS0',
	baudrate = 19200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1,
)

serfast = serial.Serial(
	port ='/dev/ttyS0',
	baudrate = 19200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=.2,
)


# program to monitor and print out all DALI bus traffic.

GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.IN)
GPIO.setup(6,GPIO.IN)

print('\n\n')
print('      ATX LED Consultants Inc - DALI bus debugger')
print('')
ser.write('v\n')  # lets get version number first
x=serfast.read()
if x == "" :
	print(' Missing Firmware \n\n')
	exit()

x=ser.read(2)
print('AL-DALI-Hat: HW version: %s'%(x))
y=ser.read(2)
print('AL-DALI-Hat: FW version: %s'%(y))

if GPIO.input(6) == 0:
 	print('Power:       Primary missing')
else:
 	print('Power:       Primary OK')

if GPIO.input(5) == 0:
 	print('Power:       Secondary missing')
else:
	print('Power:       Secondary OK')

print('')
print('Destination <= Data ')
print('        Axxx = Short Address')
print('        Gxx  = Group Address')
print('        All  = Broadcast')
print('')
print('Date Time    Data')
print('')


ser.write('d\n')  # now check if Power is good

nl = 0
DT = 0
DT1 = 0
DT2 = 0

log = open("%s/../DALI_log.txt" % base, "a+")

FlushFlag = 0

PacketCount=0;
PacketTime=0;
ts1 = 0


while 1:
	x=ser.read(1)
	ts = time.time()

	if x == 'H' :
		PacketCount = PacketCount+2
		PacketTime = PacketTime + 25
		if ts1 == 0 :
			ts1 = time.time()

		st = datetime.datetime.fromtimestamp(ts).strftime('%d %H:%M:%S ')
		print st,
		if nl != 0 :
			print('%3d nak'%(nl))
			nl = 0
		x=ser.read(2)
		x=int(x,16)
		yt=ser.read(2)
		y=int(yt,16)

		if ( x & 1 )== 0 :  # arc command
			if x & 128 == 0 :
				print('A%2d <= level %3d'%(x/2,y))
				log.write('%s : A%2d <= level %3d'%(st,x/2,y))
			if x & 192 == 128 :
				print('G%2d <= level %3d'%(x/2-64,y))
				log.write('%s : A%2d <= level %3d'%(st,x/2-64,y))
			if x == 254 :
				print('all <= level %3d'%(y))
				log.write('%s : All <= level %3d'%(st,y))

		else:
			Cmd = "Command %3d" % y
			if DT < 16:
				Time = ProgTimes[DT]

			if y == 0:
				Cmd = "Off"
			if y == 6:
				Cmd = "Set to Min level"
			if y == 5:
				Cmd = "Set to Max level"
			if y == 35:
				Cmd = "Set Mode to %d " % (DT)
			if y == 42:
				Cmd = "Set Max Level to %d" % (DT)
			if y == 43:
				Cmd = "Set Min Level to %d" % (DT)
			if y == 44:
				Cmd = "Set System Failure Level to %d" % (DT)
			if y == 45:
				Cmd = "Set Power On Level to %d" % (DT)
			if y == 46:
				Cmd = "Set Fade Up %d seconds" % ( Time )
			if y == 47:
				Cmd = "Set Fade Down %d seconds" % ( Time )
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
			if y > 95 :
				if y < 112 :
					Cmd = "Add to Group %d" % (y-96)
			if y > 111 :
				if y < 128 :
					Cmd = "Remove from Group %d" % (y-112)
			if y == 129:
				Cmd = "Enable Memory Write"
			if y == 145:
				Cmd = "Ping Driver"
			if y == 148:
				Cmd = "Query Range Error"
			if y == 155:
				Cmd = "Query power failure"
			if y == 160:
				Cmd = "Query Arc Level"
			if y == 161:
				Cmd = "Query Max Level"
			if y == 162:
				Cmd = "Query Min Level"
			if y == 163:
				Cmd = "Query Power On Level"
			if y == 192:
				Cmd = "Query Group 0-7"
			if y == 193:
				Cmd = "Query Group 8-15"
			if y == 197:
				Cmd = "Read Memory"
			if y == 226:
				Cmd = "Activate Color"
			if y == 231:
				w = 4000 -  ( 368 - DT1 * 256 - DT ) * 5.2
				Cmd = "Set Color temp to %4d K " % (w)

			z = x/2+176 

			if x & 128 == 0 :
				print('A%2d <= %s '%(x/2,Cmd))
				log.write('%s : A%2d <= %s'%(st,x/2,Cmd))

			if x & 224 == 128 :
				print('G%2d <= %s '%(x/2-64,Cmd))
				log.write('%s : G%2d <= %s'%(st,x/2-64,Cmd))


			if x & 224 == 160 :
				Cmd = "all <= Send command %3d data %3d " % (z,y)

				if z == 256:
					Cmd = "Terminate Addressing mode"

				if z == 257:
					Cmd = "all <= Load DT Register with %3d "%(y)
					DT = y

				if z == 267:
					Cmd = "%3d <= Set Short Address "%(y/2)

				print('%s '%(Cmd))
				log.write('%s : %s'%(st,Cmd))

			if x & 224 == 192 :
				
				if z == 272 :
					print('all <= Enable Device Type %3d'%(y) )
				elif z == 273 :
					print('all <= Load DT1 Register with %3d '%(y))
					DT1 = y 
				elif z == 274 :
					print('all <= Load DT2 Register with %3d '%(y))
					DT2 = y
				elif z == 276:
					print('all <= Write %3d to Memory at %3d:%3d'%(y,DT1,DT) )
				else :
					print('all <= Send command %3d data %3d '%(z,y))

				log.write('%s : command %3d value %3d'%(st,z,y))
	

			if x == 255 :
				print('all <= %s '%(Cmd))
				log.write('%s : all <= %s'%(st,Cmd))

		log.write('\r\n')
		FlushFlag = 11

	if x == 'D' :
		st = datetime.datetime.fromtimestamp(ts).strftime('%d %H:%M:%S ')
		print st,
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
		log.write('%s : DALI Power => %d\r\n'%(st,y))
		log.flush()
		

	if x == 'N' :
		print('.'),  # normal: no response to most commands, just a dot
		nl = nl + 1
	if x == 'J' :
		PacketCount = PacketCount+1
		PacketTime = PacketTime + 13
		st = datetime.datetime.fromtimestamp(ts).strftime('%d %H:%M:%S ')
		print st,
		if nl != 0 :
			print('%3d nak'%(nl))  
			nl = 0
		y=ser.read(2)
		y=int(y,16)
		print('                      Answer %02x Hex %d Decimal'%(y,y))
		log.write('%s :                  Response %d\r\n'%(st,y))
		FlushFlag = 2
	if x == 'X' :
		st = datetime.datetime.fromtimestamp(ts).strftime('%d %H:%M:%S ')
		print st,
		if nl != 0 :
			print('%3d nak'%(nl))
			nl = 0
		print('Framing Error')
		log.write('%s : Framing Error %d\r\n'%(st,y))
		FlushFlag = 3

	if x == 10 :
		print('newline')

	if x == '' :
		if(PacketCount > 20) :
			lt = ts-ts1
			st = datetime.datetime.fromtimestamp(lt).strftime('%M minutes %S seconds ')
			Eff = (PacketTime*100) / (lt*1000)
			print('last burst was %d packets in %s = %d pct utilization '% ( PacketCount/2,st,Eff) )
		if PacketCount > 0  :
			PacketCount = 0
			PacketTime = 0
			ts1 = 0

	if FlushFlag > 0 :
		FlushFlag -= 1
		if FlushFlag == 1 :
			log.flush()
			


