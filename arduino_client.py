#!/usr/bin/env python

import io
import os
import re
import sys
import serial
import sound
import play
import canvas

stop_ = False

with open( './songs_format.txt', 'r' ) as f:
    txt = f.read()

seqs_ = [ x for x in txt.split( '\n' ) if x.strip() ]

def _handle_arduio_command( line, q = None):
    cmd, arg = line[:2], line[2:]
    print( cmd, arg )
    if  len(line) < 2:
        return 
    if cmd == '#B':
        timeWithoutActivity_ = 0
    elif cmd == '#P':
        pass
    elif cmd == '#R':
        play.play('a1')
        canvas.resetAll()
    elif cmd == '#T':
        play.play( arg )
    elif cmd == '#S':
        play.play_seq( seqs_[int(arg)] )
    else:
        print( 'Uknown command: %s' % line )


def read_and_execute( serial, q ):
    line = serial.readline().strip()
    if not line:
        return 
    if '#' in line[0]:
        if q is not None:
            q.put(line)
        else:
            _handle_arduio_command(line)

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
        print( "[WARN ] Could not launch Arduino handler: %s" % e )
        
