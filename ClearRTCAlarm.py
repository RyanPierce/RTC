#!/usr/bin/python3

import smbus
import syslog
import sys

#####
##### Main code starts here
#####

# Set the RTC
bus = smbus.SMBus(1)
address = 0x68
bus.write_byte_data(address, 0x07, 0x00)
bus.write_byte_data(address, 0x08, 0x00)
bus.write_byte_data(address, 0x09, 0x00)
bus.write_byte_data(address, 0x0a, 0x00)
bus.write_byte_data(address, 0x0e, 0x18) # Set RS2, RS1, clear A1IE

# Log to syslog
syslog.openlog('ClearRTCAlarm.py')
syslog.syslog('Cleared RTC Alarm 1, Cleared A1IE')
print('Cleared RTC Alarm 1, Cleared A1IE')

