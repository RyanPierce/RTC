#!/usr/bin/python3

import smbus

def getDayText(day):
	# This is arbitrary, we align with Unix order but starting on 1
	if day == 1:
		return "SUN"
	elif day == 2:
		return "MON"
	elif day == 3:
		return "TUE"
	elif day == 4:
		return "WED"
	elif day == 5:
		return "THU"
	elif day == 6:
		return "FRI"
	elif day == 7:
		return "SAT"
	else:
		return "ERROR"

def getMonthText(mon):
	if mon == 1:
		return "JAN"
	elif mon == 2:
		return "FEB"
	elif mon == 3:
		return "MAR"
	elif mon == 4:
		return "APR"
	elif mon == 5:
		return "MAY"
	elif mon == 6:
		return "JUN"
	elif mon == 7:
		return "JUL"
	elif mon == 8:
		return "AUG"
	elif mon == 9:
		return "SEP"
	elif mon == 10:
		return "OCT"
	elif mon == 11:
		return "NOV"
	elif mon == 12:
		return "DEC"
	else:
		return "ERROR"

#####
##### Main code starts here
#####

bus = smbus.SMBus(1)
address = 0x68

data = bus.read_i2c_block_data(address, 0x00, 16)

secs = data[0] & 0x0f
secs += ((data[0] & 0x70) >> 4) * 10
mins = data[1] & 0x0f
mins += ((data[1] & 0x70) >> 4) * 10
hours = data[2] & 0x0f
hours += ((data[2] & 0x30) >> 4) * 10 # Assume 24h
day = data[3] & 0x07
date = data[4] & 0x0f
date += ((data[4] & 0x30) >> 4) * 10
mon = data[5] & 0x0f
mon += ((data[5] & 0x10) >> 4) * 10
year = 2000
year += data[6] & 0x0f
year += ((data[6] & 0xf0) >> 4) * 10
if data[5] & 0x80:
	year += 100
almsecs = data[7] & 0x0f
almsecs += ((data[7] & 0x70) >> 4) * 10
almmins = data[8] & 0x0f
almmins += ((data[8] & 0x70) >> 4) * 10
almhours = data[9] & 0x0f
almhours += ((data[9] & 0x30) >> 4) * 10 # Assume 24h
if data[7] & 0x80:
	A1M1 = 1
else:
	A1M1 = 0
if data[8] & 0x80:
	A1M2 = 1
else:
	A1M2 = 0
if data[9] & 0x80:
	A1M3 = 1
else:
	A1M3 = 0
if data[0x0a] & 0x80:
	A1M4 = 1
else:
	A1M4 = 0
if data[0x0a] & 0x40:
	DYDT = 1
else:
	DYDT = 0
if data[0x0e] & 0x01:
	A1IE = 1
else:
	A1IE = 0
if data[0x0e] & 0x04:
	INTCN = 1
else:
	INTCN = 0
if data[0x0f] & 0x01:
	A1F = 1
else:
	A1F = 0
if data[0x0f] & 0x80:
	OSF = 1
else:
	OSF = 0


print("Time: %02d:%02d:%02d" % (hours, mins, secs))
print("Date: %s %s %d, %d" % (getDayText(day), getMonthText(mon), date, year))
print("Alarm 1 Time: %02d:%02d:%02d" % (almhours, almmins, almsecs))
print("DYDT=%d A1M1=%d A1M2=%d A1M3=%d A1M4=%d" % (DYDT, A1M1, A1M2,
	A1M3, A1M4))
print("A1IE=%d INTCN=%d A1F=%d OSF=%d" % (A1IE, INTCN, A1F, OSF))

