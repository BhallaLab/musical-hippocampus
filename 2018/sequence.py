__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import random
import numpy as np
import config
import sound
import difflib

class SeqRecognizer():

    def __init__( self, seq, thres = 0.5 ):
        self.seq = seq 
        self.txtSeq = ''.join(map(str,seq))
        self._historyLen = 2 * len(seq)
        self.compartment = [0] * (1+len(config.alphabets_))
        self.history = [0] * self._historyLen
        self.output =  0
        self._output = 0
        self._ninput = 0
        self._x = 0
        self.threshold = thres

    def inject(self, x):
        self.output *= 0.95
        self.history.pop()
        self.history.insert(0, x)
        a = self.txtSeq
        b = ''.join(map(str, self.history[:len(self.seq)]))
        s = difflib.SequenceMatcher(None, a, b)
        self._output = s.ratio()
        self._x = x
        self._ninput += 2
        self.update(x)
        if self._output >= self.threshold:
            self.output = 1

    def flow_left(self, i):
        #  print( 'l1', self.compartment, end = ' | ' )
        for ii in range(i, 0, -1):
            d = self.compartment[ii] - self.compartment[ii-1]
            #  assert d >= 0, (d, ii, ii-1, self.compartment)
            self.compartment[ii-1] += d / 2.0
        #  print( 'l2', self.compartment )

    def flow_right(self, i):
        #  print( 'r1', self.compartment, end = ' | ' )
        for ii in range(i, len(self.compartment)-1):
            d = self.compartment[ii] - self.compartment[ii+1]
            #  assert d >= 0, (d, ii, ii+1, self.compartment)
            self.compartment[ii+1] += d / 2.0
        #  print( 'r2', self.compartment )

    def update(self, j):
        self.compartment[j] += 1
        # Now the flow.
        #  print( 'Input at %s' % j )
        self.flow_left( j )
        self.flow_right( j )
        # Decay
        for i, x in enumerate(self.compartment):
            self.compartment[i] *= 0.9

    def __hash__(self):
        return id(self)

    def __str__(self):
        s = map(str, self.history)
        histStr = ''.join(s)
        return '%10s → %.2f, %.2f' % (histStr, self._output, max(self.compartment))

    def reset(self):
        self.history = [0] * self._historyLen
        self.compartment = [0] * len(self.compartment)
        self.output = 0
        self._output = 0
        self._ninput = 0

    def inject_seq(self, seq):
        [ self.inject(s) for s in seq ]

def test():
    seq = [1,2,3,4,5] 
    a = SeqRecognizer( seq )
    a.inject_seq(seq)
    print( a )
    for i in range(5):
        a.reset()
        random.shuffle(seq)
        a.inject_seq( seq )
        print(a)

if __name__ == '__main__':
    test()
