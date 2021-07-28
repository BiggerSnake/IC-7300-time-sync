#! /usr/bin/python3
#
# IC-7300 time sync by Kevin Loughin, KB9RLW. June 2019
# Re-formatted and modified to also set the date, AD0YO. July 2021
# Ver. 2.0
# This script will set the Icom 7300 internal clock and date based on your computer
# clock.  Provided your computer clock is synced to network time, this
# should insure your radio's clock is within a fraction of a second of
# standard time.
#

#Import libraries we'll need to use
import time
import serial
import struct

# Below are three variables you need to change to pick time-zone to use and
# radio serial port.  If your computer clock is not set to Universal time, set
# USE_LOCAL_TIME to True.
# Also the baud rate and serial port name for your IC-7300 on your computer. Change to 
# match your setup. i.e. COM3 or similar for windows.
#
BAUDRATE = 9600         # change to match your radio
USE_LOCAL_TIME = False  # True if want to use local time.
SERIALPORT = "COM5"           # Serial port for Windows of your radios serial interface
#SERIALPORT = "/dev/ttyUSB0"  # Serial port for Linux

# true if verbose output
VERBOSE = True


def sendCommand(port, baudrate, command):
    # send command string to the IC-7300 a byte at a time
    with serial.Serial(port, baudrate) as ser:
        for cmd in command:
            senddata = int(bytes(cmd, 'UTF-8'), 16)
            ser.write(struct.pack('>B', senddata))

def buildTimeCommand(secs, useLocalTime):
    # build command string to set time on the IC-7300
    # Defining the command to set the radios time in hex.
    preamble = ["0xFE", "0xFE", "0x94", "0xE0", "0x1A", "0x05", "0x00", "0x95"]
    postamble = "0xFD"
    
    if useLocalTime:
        t = time.localtime(secs)
    else:
        t = time.gmtime(secs)

    command = preamble
    
    # Do the hour
    hours = time.strftime("%H", t)
    hours = int(hours)
    hours = str(hours)

    hours = ("0"+hours)[-2:] # prepend 0 if one char long
    hours = "0x" + hours
    command.append(hours)

    # Do the minute
    minutes = time.strftime("%M", t)
    minutes = int(minutes)
    minutes = str(minutes)

    minutes = ("0"+minutes)[-2:] # prepend 0 if one char long
    minutes = "0x" + minutes
    command.append(minutes)

    command.append(postamble)

    return command

def buildDateCommand(secs, useLocalTime):
    #build command string to set date
    #defining the command to set the radio date in hex.
    preamble = ['0xFE', '0xFE', '0x94', '0xE0', '0x1A', '0x05', '0x00', '0x94']
    postamble = "0xFD"
    
    command = preamble

    # get the input time in epoch secs in hours and minutes either local or gmt
    # using the input epoch secs
    if useLocalTime:
        t = time.localtime(secs)
    else:
        t = time.gmtime(secs)
        
    # get the month, day, and year
    mon = time.strftime("%m", t)
    day = time.strftime("%d", t)
    year = time.strftime("%Y", t)

    #do year as two bytes
    command.append("0x"+year[:2])
    command.append("0x"+year[2:])
    #do month
    command.append("0x"+mon)
    #do day of month
    command.append("0x"+day)

    command.append(postamble)
    
    return command


def waitToTop(useLocalTime, verbose=False):
    # Now get the current computer time in seconds.  Needed to set the time
    # at the top of the minute.
    if useLocalTime:
        t = time.localtime()
    else:
        t = time.gmtime()
    seconds = int(time.strftime("%S", t))

    # Now we wait for the top of the minute. Print dots each sec till top
    lastsec = 1
    while(seconds != 0):
       t = time.gmtime()
       seconds = int(time.strftime("%S", t))
       if(seconds != lastsec):
          lastsec = seconds
          if verbose:
              print('.',end='',flush=True)
       time.sleep(.01)
    if verbose:
        print()
        
def set7300TimeDate(verbose=False):
    secs = time.time()    # get secs since epoch
    secs += 60.0          # move ahead 1 minute to be able to set IC7300
                          # clock at the top of the minute
    # get time command string
    command = buildTimeCommand(secs, USE_LOCAL_TIME)
    
    # wait to top of minute
    waitToTop(USE_LOCAL_TIME, verbose)
    if verbose:
        print(command)
    # Now that we've reached the top of the minute, set the radios time!
    sendCommand(SERIALPORT, BAUDRATE, command)

    #get date command string
    command = buildDateCommand(secs, USE_LOCAL_TIME)
    if verbose:
        print(command)
    #set radio date
    sendCommand(SERIALPORT, BAUDRATE, command)
    
if __name__ == "__main__":
    #execute only if run as a script
    set7300TimeDate(VERBOSE)
    
# All done.  The radio is now in sync with the computer clock. And date!
