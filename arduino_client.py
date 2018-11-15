#!/usr/bin/env python

import io
import os
import re
import sys
import serial

stop_ = False

def read_and_execute( serial, q ):
    line = serial.readline().strip()
    if not line:
        return 
    if '#' in line[0]:
        if q is not None:
            q.put(line)

def main( q = None, port = '/dev/ttyACM0', baud = 19200 ):
    global port_
    with serial.Serial( port, baud ) as ser:
        while True:
            if not stop_:
                read_and_execute(ser, q)
            else:
                break

if __name__ == '__main__':
    try:
        main( )
    except Exception as e:
        print( "[WARN ] Could not launch Arduino handler:" % e )
        
