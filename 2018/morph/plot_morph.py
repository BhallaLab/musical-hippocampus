"""plot_morph.py: 

"""
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import networkx as nx
import subprocess
import swc
import cv2

plt.ion()

canvas_ = np.zeros( shape=(1000,1000,3) )
win_ = cv2.namedWindow( "NRN" )

def int2Clr( x ):
    r, g, b, a = cm.hot(x)
    return int(r*255), int(g*255), int(b*255)

def cvPos(p, offset = (100,100) ):
    x1, y1 = p
    xo, yo = offset
    return int(x1+xo), int(y1+yo)

def show_frame( img = None):
    global win_
    if img is None:
        img = canvas_
    cv2.imshow( "NRN", img )
    cv2.waitKey(1)

def plot_png_using_cv2(G):
    global win_
    global canvas_
    lines = []
    pos = nx.get_node_attributes(G, 'coordinate2D' )
    for n1, n2 in G.edges():
        x1, y1 = cvPos(pos[n1])
        x2, y2 = cvPos(pos[n2])
        c = G.node[n1]['color']
        cv2.line(canvas_, (x1,y1), (x1, y2),  int2Clr(c), 1 )

def update1(G, i):
    for n in reversed(list(nx.topological_sort(G))):
        # Get the flow from incoming.
        G.node[n]['color'] = G.node[n]['color'] * 0.75
        nn = list(G.predecessors(n))
        if len(nn) == 1:
            G.node[n]['color'] = G.node[nn[0]]['color']

def _tranfer(G, ss):
    tmp = []
    for s in ss:
        G.node[s]['color'] *= 0.9
        for n in G.successors(s):
            G.node[n]['color'] = G.node[s]['color']
            tmp.append(n)
    return tmp

def update(G, i):
    ns = [[1]]
    while len(ns) > 0:
        bunch = ns.pop(0)
        if bunch:
            ns.append( _tranfer(G, bunch) )


def main():
    g = swc.swc2nx( './hajos/CNG version/p110715-04-BC.CNG.swc' )
    g.node[1]['color'] = 255
    for i in range(1000):
        update(g, i)
        plot_png_using_cv2( g )
        show_frame( )

if __name__ == '__main__':
    main()

