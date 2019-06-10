#
#
# program to read and set Groups
# request which short address
# read the groups
# allow add, subtract, exit
# loop
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


print('\n      ATX LED Consultants Inc - Read and Set Group\n')

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
if x == '' :
	print(' Missing Firmware ')
	exit()

print(' ')


while 1 :
	x=ser.read(4)
	text = input("Which DALI address ( 0-63, 127=all ) : ")
	address = int(text)*2

	ser.write('h%02xC0\n'%(address+1))
	time.sleep(.1)
	x=ser.read(1)
	if x == 'N' :
		exit()
	text=ser.read(2)
	g07=int(text,16)
	bit=1
	bitp=0
	crlf=ser.read(1)
	while bit<256 :
		if(g07 & bit ) :
			print(' Group %2d enabled'%bitp);
		bit = bit *2
		bitp = bitp + 1

	ser.write('h%02xC1\n'%(address+1))
	time.sleep(.1)
	x=ser.read(1)
	if x == 'N' :
		exit()
	text=ser.read(2)
	g815=int(text,16)
	bit=1
	bitp=8
	crlf=ser.read(1)
	while bit<256 :
		if(g815 & bit ) :
			print(' Group %2d enabled'%bitp);
		bit = bit *2
		bitp = bitp + 1

	text = raw_input("Add Group, Subtract Group, Exit (A,S,E) : ")
	text = text.upper()
	if text == "A"  :
		text = input("Group # : ")
		bit = int(text)
		ser.write('t%02x6%X\n'%(address+1,bit))
	
	elif text == "S" :
		text = input("Group # : ")
		bit = int(text)
		ser.write('t%02x7%X\n'%(address+1,bit))

	elif 1 :
		exit()		

print (' ')