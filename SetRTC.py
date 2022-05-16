#!/usr/bin/python3

# Note: This is not a high accuracy method for setting the system clock!
# Expect errors +/- 1 second

import smbus
import time
import syslog

#####
##### Main code starts here
#####

bus = smbus.SMBus(1)
address = 0x68

# Read current RTC state
dataIn = bus.read_i2c_block_data(address, 0x00, 16)

# Read the current time
now = time.gmtime()
dataOut = bytearray(7)
dataOut[0x00] = now.tm_sec % 10 + ((now.tm_sec // 10) << 4)
dataOut[0x01] = now.tm_min % 10 + ((now.tm_min // 10) << 4)
dataOut[0x02] = now.tm_hour % 10 + ((now.tm_hour // 10) << 4)
# Python considers Monday = 0, Linux considers Sunday = 0, but the
# RTC starts with 1
dataOut[0x03] = now.tm_wday + 2
if dataOut[0x03] == 8:
	dataOut[0x03] = 1
dataOut[0x04] = now.tm_mday % 10 + ((now.tm_mday // 10) << 4)
dataOut[0x05] = now.tm_mon % 10 + ((now.tm_mon // 10) << 4)
if now.tm_year >= 2100:
	dataOut[0x05] |= 0x80
dataOut[0x06] = now.tm_year % 10 + (((now.tm_year // 10) % 10) << 4)

# Set the RTC
bus.write_byte_data(address, 0x00, dataOut[0x00])
bus.write_byte_data(address, 0x01, dataOut[0x01])
bus.write_byte_data(address, 0x02, dataOut[0x02])
bus.write_byte_data(address, 0x03, dataOut[0x03])
bus.write_byte_data(address, 0x04, dataOut[0x04])
bus.write_byte_data(address, 0x05, dataOut[0x05])
bus.write_byte_data(address, 0x06, dataOut[0x06])

# Set INTCN - this turns on the second alarm (we don't use) and turns off
# the square wave generator - which drops power from 1.5 uA to 600 nA
bus.write_byte_data(address, 0x0e, dataIn[0x0e] | 0x04)

# Clear the Oscillator Stop Flag as time is now valid
bus.write_byte_data(address, 0x0f, dataIn[0x0f] & 0x7f)

# Log to syslog
syslog.openlog('SetRTC.py')
syslog.syslog('RTC set from system clock')

print('RTC set from system clock')
