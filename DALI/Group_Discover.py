#
#
# program to find Group members
# request which group
# read the addresses
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
if x == '' :
	print(' Missing Firmware ')
	exit()
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

print(' ')
x=ser.read(10)

group = 0
while group < 16 :

	ser.write('h%02x91\n'%(group*2+129))
	x=ser.read(1)
	if x == 'J' :
		x=ser.read(2)
		print('member(s)        in group %2d' % group)
	if x == 'D' :
		x=ser.read(2)
		print('Multiple members in group %2d' % group)
		x=ser.read(10)
		ser.write('hA300\n')
		x=ser.read(1)
	if x == 'X' :
		print('Multiple members in group %2d' % group)
#	if x == 'N' :
#		print('No       members in group %2d' % group)
	x=ser.read(1)
	if x == 'D' :
		x=ser.read(3)

	group = group + 1
	time.sleep(.03)

text = 'A'

while text != 'E' :

	text = input("Search members in Group ( 0-15 ) : ")
	if text != 'E' :
	
		group = int(text)

		sa=0
		gread = "C0"
		bit = 1 << ( group & 7)
		if group > 7 :
			gread = "C1"

		found = 0

		while sa < 64 :

			ser.write('h%02x%s\n'%(sa*2+1,gread))
			x=ser.read(1)
			if x == 'D' :
				x=ser.read(2)
				print('DALI power up/down %2s' % x)
			if x == 'J' :
				text=ser.read(2)
				response = int(text,16)
				if response & bit :
					print('Address %d is a member'% (sa) )
					found = 1
			x=ser.read(1)
			sa = sa+1
			time.sleep(.02)

		if found == 0 :
			print(' no members ')

		print(' ')

