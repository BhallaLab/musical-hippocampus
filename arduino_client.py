#!/usr/bin/env python

import io
import os
import re
import sys
import serial

stop_ = False
def handle_arduio_command( line, q ):
    cmd, arg = line[:2], line[2:]
    if  len(line) < 2:
        return 
    if cmd == '#B':
        canvas.inject_alphabet_ca3(1+int(arg))
        timeWithoutActivity_ = 0
    elif cmd == '#P':
        canvas.progressFromArduino(arg)
    elif cmd == '#R':
        print( 'Arduino said reset everything.' )
        play.play('a1')
        canvas.resetAll()
        while not q.empty():
            q.get()
    elif cmd == '#T':
        play.play( arg )
    else:
        print( 'Uknown command: %s' % line )


def read_and_execute( serial, q ):
    line = serial.readline().strip()
    if not line:
        return 
    if '#' in line[0]:
        if q is not None:
            q.put(line)

def main( q = None, port = '/dev/ttyACM0', baud = 38400 ):
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
        
