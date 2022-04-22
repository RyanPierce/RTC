#!/usr/bin/python3

# Note: This is not a high accuracy method for setting the system clock!
# Expect errors +/- 1 second

import smbus
import syslog
import subprocess
import sys

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

syslog.openlog('SetSystemClock.py')

data = bus.read_i2c_block_data(address, 0x00, 16)

# First, make sure RTC time is valid. 
# No sense setting the clock to Jan 1, 2000

if data[0x0f] & 0x80:
	# RTC clock is invalid
	syslog.syslog('RTC time invalid; not setting system clock!')
	print('RTC time invalid; not setting system clock!')
	sys.exit(-1)

# We have a valid time, stop the time service
print ("Shutting down network time service")
command = ['sudo', 'systemctl', 'stop', 'systemd-timesyncd.service']
subprocess.call(command)

print("The sysdate before setting with RTC is:")
subprocess.call('date')

# Get the data again from the RTC in case there were any big delays
data = bus.read_i2c_block_data(address, 0x00, 16)
secs = data[0] & 0x0f
secs += ((data[0] & 0x70) >> 4) * 10
mins = data[1] & 0x0f
mins += ((data[1] & 0x70) >> 4) * 10
hours = data[2] & 0x0f
hours += ((data[2] & 0x30) >> 4) * 10 # Assume 24h
date = data[4] & 0x0f
date += ((data[4] & 0x30) >> 4) * 10
mon = data[5] & 0x0f
mon += ((data[5] & 0x10) >> 4) * 10
year = 2000
year += data[6] & 0x0f
year += ((data[6] & 0xf0) >> 4) * 10
if data[5] & 0x80:
	year += 100

date_time = "%02d %s %02d %02d:%02d:%02d" % (date, getMonthText(mon), 
	year, hours, mins, secs)

print("Setting system time via RTC:", date_time)
syslog.syslog("Setting system time via RTC")

command = ['sudo', 'date', '-u', '-s', date_time]
subprocess.call(command)

print("Set system time via RTC")
syslog.syslog("Set system time via RTC")

print("The sysdate after setting with RTC is:")
subprocess.call('date')

print ("restarting network time service")
command = ['sudo', 'systemctl', 'start', 'systemd-timesyncd.service']
subprocess.call(command)

