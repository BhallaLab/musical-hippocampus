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
import threading

class SeqRecognizer():

    def __init__( self, seq, thres = 0.5 ):
        self.seq = seq 
        self.txtSeq = ''.join(map(str,seq))
        self._historyLen = 2 * len(seq)
        self.history = [0] * self._historyLen
        self.output =  0
        self._output = 0
        self.threshold = thres

    def inject(self, x):
        self.output *= 0.95
        self.history.pop()
        self.history.insert(0, x)
        a = self.txtSeq
        b = ''.join(map(str, self.history[:len(self.seq)]))
        s = difflib.SequenceMatcher(None, a, b)
        self._output = s.ratio()
        if self._output >= self.threshold:
            self.output = 1

    def __hash__(self):
        return id(self)

    def __str__(self):
        s = map(str, self.history)
        histStr = ''.join(s)
        return '%10s → %.2f' % (histStr, self._output)

    def reset(self):
        self.history = [0] * self._historyLen
        self.output = 0
        self._output = 0

def test():
    a = SeqRecognizer( [1,2,3,4,5] )
    for i in range(20):
        x = random.choice( config.alphabets_ )
        a.inject( x )
        print(a)

if __name__ == '__main__':
    test()
