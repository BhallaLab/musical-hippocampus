#!/usr/bin/env python
"""main.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import numpy as np
import itertools
import matplotlib as mpl
import matplotlib.pyplot as plt
import config as _c

axes_ = {} 

# global variable to stop drawing.
break_ = False

plt.ion()

def init_axes():
    global axes_
    gridSize = (6, 6)
    ax1 = plt.subplot2grid( gridSize, (0,0), colspan = 6, rowspan=4 )
    ax2 = plt.subplot2grid( gridSize, (4,0), colspan = 6, rowspan=2 )
    axes_['hippo'] = ax1
    axes_['user'] = ax2

def init_canvas( ):
    global axes_

def update():
    return 

def main():
    init_axes()
    fig = init_canvas( )
    for i in itertools.count():
        if i % 10 == 0:
            plt.suptitle( 'Step %d' % i )
        update()
        plt.show( )
        plt.pause(0.0001)
    plt.close()
    print( 'All done' )


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        break_ = True
        plt.close()
        quit()

