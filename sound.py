"""sound.py: 
"""
from __future__ import print_function, division
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import pygame
import time
import glob
import config

import pygame.midi
import pygame.mixer

pygame.init()
pygame.midi.init()
pygame.mixer.init()

sdir_ = os.path.dirname( __file__ )
notes = glob.glob(os.path.join(sdir_, 'sounds/*.wav'))
notes = { 1:'C1',2:'D1',3:'E1',4:'F1',5:'G1',6:'A1',7:'B1', 8:'F#1' }

def play(note, duration = 2e-1 ):
    global player_
    wavfile = os.path.join( sdir_, 'sounds/%s.wav' % note )
    if not os.path.isfile(wavfile):
        print( "[WARN ] Note %s not found" % note )
        return 
    pygame.mixer.music.load(wavfile)
    pygame.mixer.music.play()

def play_int(i):
    play( notes[i%7+1] )

def play_seq( seq ):
    global notes 
    seq = list(seq)
    for i in seq:
        if not i:
            time.sleep(0.1)
        else:
            play(notes[i])
            time.sleep(0.2)
    time.sleep(1)

def main():
    for i, seq in config.connections_:
        seq.insert(1, 0)
        play_seq( seq )
        time.sleep(1)

if __name__ == '__main__':
    main()
