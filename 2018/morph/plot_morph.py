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
import matplotlib.cm as cm
import numpy as np
import networkx as nx
import operator
import math
import swc
import cv2
import scipy.interpolate as sci


sdir_       = os.path.dirname( __file__ )
background_ = 0
h_, w_      = 480, 800
canvas_     = np.zeros( shape=(h_,w_,3) ) + background_
win_        = cv2.namedWindow( "NRN" )
hippoImg_   = cv2.imread( os.path.join( sdir_, 'hippocampus-800x480-1.png' ) )

ca1_ = [ 
        ((377, 129),   210, './swcs/cell1-11b-CA1.CNG.swc' ),
        ((397, 125),  250, './swcs/cell1-2a-CA1.CNG.swc'  ),
        ((414, 123),  -120,  './swcs/cell1-3-CA1.CNG.swc' ),
        ((430, 124),  60, './swcs/cell1-3a-CA1.CNG.swc'  ),
        ((456, 120),  -30,'./swcs/cell1-5b-CA1.CNG.swc'  ),
        ]

ca3_ = [ 
        ((151, 251), -60, './swcs/cell1-CA3.CNG.swc'    ),
        ((153, 269), 0, './swcs/cell1-8b-CA3.CNG.swc' ),
        ((153, 275), 0, './swcs/cell13-CA3.CNG.swc'   ),
        ((153, 289),  -30, './swcs/cell1-8b-CA3.CNG.swc' ),
        ((158, 308), -150, './swcs/cell1-3a-CA3.CNG.swc' ),
        ((165, 320), -120, './swcs/cell1-CA3.CNG.swc'    ),
        ]

def smooth_line(ps):
    ps = np.array(ps)
    X, Y = ps[:,0], ps[:,1]
    fs = sci.splrep(X, Y)
    x = np.linspace(min(X), max(X), 20)
    y = sci.splev(x, fs)
    return zip(map(int,x),map(int, y))

def ca1Toca3( ):
    global ca1_, ca3_
    path = [ x[0] for x in ca3_+ca1_ ]
    path += [(100,100), (80,120) ]
    path = sorted(path, key=lambda x: swc._distance(x, (100,500) ))
    path = smooth_line(path)
    g = nx.path_graph(len(path), create_using=nx.DiGraph() )
    for n, p in zip(g.nodes(), path):
        g.node[n]['color'] = 255
        g.node[n]['coordinate'] = p
    return g


def int2Clr( x ):
    r, g, b, a = cm.hot(x)
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
    #  assert g.node[1]['coordinate'] <= (5,5), g.node[1]['coordinate']
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

def plot_png_using_cv2(G, canvas_):
    global win_
    pos = nx.get_node_attributes(G, 'coordinate' )
    # draw the soma.
    cv2.circle( canvas_, pos[1], 5, int2Clr(G.node[1]['color']), -1 )
    for n1, n2 in G.edges():
        x1, y1 = pos[n1]
        x2, y2 = pos[n2]
        c = G.node[n1]['color']
        cv2.line(canvas_, (x1,y1), (x2, y2),  int2Clr(c), 1)

def plot_graphs( gs ):
    global hippoImg_
    global canvas_
    canvas_ = hippoImg_
    [ plot_png_using_cv2(g, canvas_) for g in gs]

def update_using_topologicl_sorting(G, i):
    for n in reversed(list(nx.topological_sort(G))):
        # Get the flow from incoming.
        G.node[n]['color'] = G.node[n]['color'] * 0.1
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

def create_canvas( ):
    nrns = []
    for pos, theta, k in ca1_:
        print( k, theta, pos )
        g = swc.swc2nx(k, scale=0.2)
        preprocess( g, rotate=theta, shift=pos )
        g.node[1]['color'] = 255
        nrns.append( g )

    for pos, theta, k in ca3_:
        g = swc.swc2nx(k, scale=0.1)
        preprocess( g, rotate=theta, shift=pos )
        g.node[1]['color'] = 255
        nrns.append( g )
    #  g = ca1Toca3()
    nrns.append(g)
    return nrns

def main():
    nrns = create_canvas()
    for i in range(100):
        [update_using_topologicl_sorting(g, i) for g in nrns]
        plot_graphs(nrns)
        show_frame( )

if __name__ == '__main__':
    main()

