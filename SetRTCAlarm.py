#!/usr/bin/python3

import smbus
import syslog
import sys

#####
##### Main code starts here
#####

# Validate Input
if len(sys.argv) < 3 or len(sys.argv) > 4:
	print("Usage: %s hour minute [second]" % (sys.argv[0]))
	sys.exit(-1)
try:
	hour = int(sys.argv[1])
	min = int(sys.argv[2])
	if len(sys.argv) == 4:
		sec = int(sys.argv[3])
	else:
		sec = 0
except ValueError:
	print("Input error!")
	print("Usage: %s hour minute [second]" % (sys.argv[0]))
	sys.exit(-1)
if hour < 0 or hour > 23 or min < 0 or min > 59 or sec < 0 or sec > 59:
	print("Input out of range!")
	print("Usage: %s hour minute [second]" % (sys.argv[0]))
	sys.exit(-1)

bus = smbus.SMBus(1)
address = 0x68

# Read current RTC state
dataIn = bus.read_i2c_block_data(address, 0x00, 16)

dataOut = bytearray(16)
dataOut[0x07] = sec % 10 + ((sec // 10) << 4)
dataOut[0x08] = min % 10 + ((min // 10) << 4)
dataOut[0x09] = hour % 10 + ((hour // 10) << 4)

# Set the RTC
bus.write_byte_data(address, 0x07, dataOut[0x07])
bus.write_byte_data(address, 0x08, dataOut[0x08])
bus.write_byte_data(address, 0x09, dataOut[0x09])
bus.write_byte_data(address, 0x0a, 0x80) # Set A1M4
bus.write_byte_data(address, 0x0e, 0x19) # Set RS2, RS1, A1IE

# Log to syslog
syslog.openlog('SetRTCAlarm.py')
status = "RTC alarm 1 set: %02d:%02d:%02d" % (hour, min, sec)
syslog.syslog(status)
print(status)
