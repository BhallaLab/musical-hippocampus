# -*- coding: utf-8 -*-
from __future__ import print_function, division

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
import sequence
from collections import defaultdict

class SeqRecognizer():

    def __init__( self, seq, thres = 0.75 ):
        self.seq = seq 
        self.txtSeq = ''.join(map(str,seq))
        self._historyLen = 2 * len(seq)
        self.history = []
        self.output =  0
        self._output = 0
        self._x = 0
        self.threshold = thres

    def inject(self, x):
        self.history.append(x)
        if len(self.history) < len(self.seq):
            return
        a = self.seq
        s = sequence.match_two_seq(a, self.history)
        self._output = s
        self._x = x
        if self._output >= self.threshold:
            self.output = 1

    def __hash__(self):
        return id(self)

    def __str__(self):
        s = map(str, self.history)
        histStr = ''.join(s)
        return '%10s %25s → %.2f, %.2f' % (self.txtSeq
                ,histStr, self._output, self.output
                )

    def reset(self):
        self.history = []
        self.output = 0
        self._output = 0

    def inject_seq(self, seq):
        [ self.inject(s) for s in seq ]

def match_indices_seq_score( a ):
    newSeq = []
    for i, x in enumerate(a):
        y = a[max(0,i-1)]
        if x-y != 1:
            newSeq += range(x+1)
        else:
            newSeq.append(x)
    return (1+max(a))/len(newSeq)

def out_of_order_elems( a ):
    # Return the value and index  of elements which are out of order.
    outOfOrder = []
    i, j = 0, 1
    while True:
        if j >= len(a) or i >= len(a):
            break
        if a[j] - a[i] == 1:
            i = j
            j += 1
            continue
        outOfOrder.append((a[j],j))
        j += 1
    return outOfOrder

def out_of_order_elems_in_all_subseq(a):
    # Compute out of order elements in all subseqs. Usually not neccessary to
    # compute in very short sequences. Upto half the size is fine since we are
    # going to compute of reversed sequences as well.
    outOfOrderNums = []
    for i in range(len(a)//2):
        sa = a[i:]
        outOfOrderNums.append((len(sa), out_of_order_elems(sa)))
    return outOfOrderNums

def _compute_score( res ):
    scores = []
    for nSeq, outOfOrder  in res:
        s = nSeq ** 2 - sum([ (nSeq-1)**1.25 for x, i in outOfOrder])
        scores.append(s)
    return max(scores)

def match_by_penalizing_out_of_order_element( a ):
    # First find a subsequence which is in ascending order.
    outOfOrderA = out_of_order_elems_in_all_subseq(a)
    outOfOrderB = out_of_order_elems_in_all_subseq( list(reversed(a)) )
    scoreA = _compute_score( outOfOrderA )
    scoreB = _compute_score( outOfOrderB )
    score = max(scoreA, scoreB)
    return score

def match_two_seq(seq, baseseq):
    # Default dict is needed if element repeat in sequence e.g.
    # Match 113154 and 111354 etc. This is biologically relevant but may not be
    # important in mathematics.
    d = defaultdict(list)
    for i, x in enumerate(baseseq):
        d[x].append(i)
    seqI = [ d[x].pop(0) if d[x] else -1 for x in seq ]
    #  print( 'x', seq, seqI )
    r = match_by_penalizing_out_of_order_element(seqI)
    return r / len(baseseq) ** 2

def _join(seq):
    return ''.join(map(str,seq))

def test( ):
    seq1, seq2 = [4,5,1,3,1,1], [4,5,1,3,1,1]
    r = match_two_seq(seq2, seq1)
    print(seq1, seq2, r)
    for i in range(20):
        random.shuffle(seq2)
        r = match_two_seq(seq2, seq1)
        print( ' →', _join(seq1), _join(seq2), r)

    seq1, seq2 = [1,1,3,1,5,4], [1,1,3,1,5,4]
    r = match_two_seq(seq2, list(reversed(seq1)))
    print(seq1, seq2, r)
    for i in range(20):
        random.shuffle(seq2)
        r = match_two_seq(seq2, seq1)
        print( ' →', _join(seq1), _join(seq2), r)


if __name__ == '__main__':
    test()
