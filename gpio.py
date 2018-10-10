"""gpio.py: 

GPIO operations.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import RPi.GPIO as gpio
import time
import random

# Use BCM mode i.e. pin number is identified by xx by GPIOxx in labels. Use
# pinout command to see the pin labellings.
gpio.setmode( gpio.BCM )

read_in_ = 16
test_out_ =  19
gpio.setup( read_in_, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup( test_out_, gpio.OUT )

def main():
    while True:
        gpio.output( test_out_, random.choice([0,1]))
        time.sleep(0.01)
        v = gpio.input( read_in_ )
        time.sleep(0.01)
        print( 'x, %d' % v )



if __name__ == '__main__':
    main()
