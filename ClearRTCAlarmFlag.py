#!/usr/bin/python3

import smbus
import syslog

#####
##### Main code starts here
#####

bus = smbus.SMBus(1)
address = 0x68

# Read current RTC state
dataIn = bus.read_i2c_block_data(address, 0x00, 16)

syslog.openlog('ClearRTCAlarmFlag.py')

if dataIn[0x0f] & 0x01:
	# Clear A1F
	bus.write_byte_data(address, 0x0f, dataIn[0x0f] & 0xfe)
	syslog.syslog('Cleared A1F flag')
	print('Cleared A1F flag')
else:
	syslog.syslog('A1F flag not set, doing nothing')
	print('A1F flag not set, doing nothing')




# Clear the Oscillator Stop Flag as time is now valid
# bus.write_byte_data(address, 0x0f, dataIn[0x0f] & 0x7f)

