# -*- coding: utf-8 -*-
from __future__ import print_function

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
import operator
import math
import swc
import cv2

plt.ion()

h_, w_ = 1000, 1000
canvas_ = np.zeros( shape=(h_,w_,3) ) + 255
win_ = cv2.namedWindow( "NRN" )

def int2Clr( x ):
    r, g, b, a = cm.hsv(x)
    return int(r*255), int(g*255), int(b*255)

def _sub(t1, t2):
    return tuple(map(operator.sub, t1, t2))

def _add(t1, t2):
    return tuple(map(operator.add, t1, t2))

def show_frame( img = None):
    global win_
    if img is None:
        img = canvas_
    cv2.imshow( "NRN", img )
    cv2.waitKey(1)

def preprocess( g, rotate=0, shift=(0,0) ):
    # Make 2d coords to int for opencv.
    pivot = g.node[1]['coordinate']
    #Put them into middle.
    _translate_graph(g, pivot)
    assert g.node[1]['coordinate'] == (0,0), g.node[1]['coordinate']
    _rotate_graph(g, rotate)
    _translate_graph(g, shift)

def _rotate_point( p, c, s ):
    return (int(c * p[0] - s * p[1]), int(s * p[0] + c * p[1]))

def _rotate_graph( g, ang ):
    # Rotate each node by theta
    theta = ang * math.pi / 180.0 
    c = math.cos(theta)
    s = math.sin(theta)
    for n in g.nodes():
        g.node[n]['coordinate'] = _rotate_point(g.node[n]['coordinate'], c, s)

def _translate_graph(g, p):
    x, y = p
    for n in g.nodes():
        g.node[n]['coordinate'] = _sub(g.node[n]['coordinate'], (-x,-y))

def plot_png_using_cv2(G):
    global win_
    global canvas_
    lines = []
    pos = nx.get_node_attributes(G, 'coordinate' )
    # draw the soma.
    cv2.circle( canvas_, pos[1], 5, int2Clr(G.node[1]['color']), -1 )
    for n1, n2 in G.edges():
        x1, y1 = pos[n1]
        x2, y2 = pos[n2]
        c = G.node[n1]['color']
        cv2.line(canvas_, (x1,y1), (x1, y2),  int2Clr(c), 2 )

def update_using_topologicl_sorting(G, i):
    for n in reversed(list(nx.topological_sort(G))):
        # Get the flow from incoming.
        G.node[n]['color'] = G.node[n]['color'] * 0.75
        nn = list(G.predecessors(n))
        for s in nn:
            G.node[n]['color'] = G.node[s]['color']

def _tranfer(G, ss):
    tmp = []
    for parent in ss:
        #  G.node[parent]['color'] *= 0.9
        for child in G.successors(parent):
            #  G.node[child]['color'] = G.node[parent]['color']
            tmp.append(child)
    return tmp

def update(G, i):
    ns = [[1]]
    while len(ns) > 0:
        bunch = ns.pop(0)
        if bunch:
            ns.append( _tranfer(G, bunch) )
            print(ns, end = ' | ' )
            sys.stdout.flush()


def main():
    g = swc.swc2nx( './pozzo-miller/CNG version/cell2-CA3.CNG.swc' )
    preprocess( g, rotate=-60, shift=(100,100) )
    g.node[1]['color'] = 255
    for i in range(1000):
        update_using_topologicl_sorting(g, i)
        plot_png_using_cv2( g )
        show_frame( )

if __name__ == '__main__':
    main()

