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
import numpy as np
import pygame
import networkx as nx
import operator
import math
import swc
import cv2
import bezier
import random
import sequence
import sound
import time
from arena import *
from config import *

nrns_              = {}
ca3nrnsNames_      = None
ca1nrnsNames_      = None
max_num_press_     = 20
current_num_press_ = 0
reset_all_         = False

def smooth_line(ps):
    ps = np.array(ps)
    X, Y = ps[:,0], ps[:,1]
    fs = sci.splrep(X, Y)
    x = np.linspace(min(X), max(X), 20)
    y = sci.splev(x, fs)
    return zip(map(int,x),map(int, y))

def schaffer_collateral( segments = 10, zigzag = 0, origin = None ):
    nodes = [ (150,330), (130,312), (130,254), (100,200),
              (185,211), (308,156), (355,151), (432,158), 
              (500,158)
            ]
    if origin:
        nodes[0] = origin
    if zigzag > 0:
        nodes = [ (x+random.randint(-zigzag,zigzag),
            y+random.randint(-zigzag,zigzag)) for x, y in nodes ]
    X, Y  = zip(*(nodes))
    nodes = np.asfortranarray([list(X), list(Y)], dtype=float)
    curve = bezier.Curve(nodes, degree=2)
    path  = curve.evaluate_multi(np.linspace(0, 1, segments)).T
    return path

def ca1Toca3( ):
    global ca1_, ca3_
    path = schaffer_collateral()
    g = nx.path_graph(len(path), create_using=nx.DiGraph() )
    for n, p in zip(g.nodes(), path):
        g.node[n]['color'] = 255
        g.node[n]['coordinate'] = tuple(map(int,p))
    for n1, n2 in g.edges():
        g[n1][n2]['width'] = 3
    return g

def int2Clr( x ):
    b = int(x)
    left = 255 - b
    r = max(10, left//2)
    g = max(5, left//2)
    b = 255 - r - g
    return (r, g, b)

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
    _translate_graph(g, pivot)
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
    somaColor = int2Clr(G.graph['SeqRec']._output*128  + 0.5*G.node[1]['color'])
    cv2.circle( canvas_, pos[1], 5, somaColor, -1 )
    for n1, n2 in G.edges():
        (x1, y1), (x2, y2) = pos[n1], pos[n2]
        cv2.line(canvas_, (x1,y1), (x2, y2)
                , int2Clr(G.node[n2]['color'])
                , G[n1][n2].get('width', 1)
                , 4
                )

def plot_graphs( ):
    global hippoImg_
    global canvas_
    global nrns_
    #  canvas_ = hippoImg_.copy()
    canvas_.fill(0)
    [plot_png_using_cv2(g, canvas_) for k, g in nrns_.items()]

def update_using_topologicl_sorting(G, i):
    for n in reversed(list(nx.topological_sort(G))):
        # Get the flow from incoming.
        nn = list(G.predecessors(n))
        for s in nn:
            G.node[n]['color'] = G.node[s]['color']
        G.node[n]['color'] = 0

def update(g):
    aps = g.graph['AP']
    nexts = []
    for n in aps:
        c = g.node[n]['color']
        if c == 0:
            break
        g.node[n]['color'] = c * 0.9
        for p in g.successors(n):
            g.node[p]['color'] = g.node[n]['color']
            nexts.append(p)
    g.graph['AP'] = nexts

def inject_ap(g):
    g.graph['AP'] = [1]
    for n in g.nodes():
        g.node[n]['color'] = 0
    g.node[1]['color'] = 255

def create_canvas( ):
    for i, (pos, theta, k) in enumerate(ca1_):
        g = swc.swc2nx(k, scale=0.3)
        preprocess( g, rotate=theta, shift=pos )
        inject_ap(g)
        g.graph['SeqRec'] = sequence.SeqRecognizer([])
        n1, seq = connections_[i]
        g.graph['SeqRec'] = sequence.SeqRecognizer(seq)
        nrns_['ca1.%d'%i] = g

    for i, (pos, theta, k) in enumerate(ca3_):
        g = swc.swc2nx(k, scale=0.1)
        preprocess( g, rotate=theta, shift=pos )
        scPath = schaffer_collateral( zigzag=4, origin= g.node[1]['coordinate'] )
        swc.add_axon(i, g, scPath)
        g.graph['SeqRec'] = sequence.SeqRecognizer([])
        nrns_['ca3.%d'%i] = g 
        inject_ap(g)

def update_canvas( ):
    global nrns_
    [update(g) for g in nrns_.values()]
    plot_graphs()

def init():
    global ca3nrnsNames_
    global ca1nrnsNames_
    create_canvas()
    ca3nrns = { k : v for k, v in nrns_.items() if 'ca3.' in k }
    ca1nrns = { k : v for k, v in nrns_.items() if 'ca1.' in k }
    ca3nrnsNames_ = list( ca3nrns.keys() )
    ca1nrnsNames_ = list( ca1nrns.keys() )

def inject_random_alphabet( ):
    global ca3nrnsNames_
    global nrns_
    gn = random.choice(ca3nrnsNames_)
    g = nrns_[gn]
    x = random.choice( alphabets_ )
    inject_alphabet_ca3(x, g )

def inject_alphabet( x, g = None ):
    g.graph['SeqRec'].inject(x)

def playback(g):
    sound.play_seq( g.graph['SeqRec'].seq )

def playback_background( g ):
    import subprocess
    seq = [str(x) for x in g.graph['SeqRec'].seq]
    subprocess.Popen( [ "timeout", "5", "python", "./play.py" ] + seq )

def inject_alphabet_ca3(x, g = None):
    global ca1nrnsNames_
    global reset_all_
    global max_num_press_
    global current_num_press_
    current_num_press_ += 1

    if g is None:
        g = nrns_['ca3.%d'% alphabetToNrn_[x] ]
    inject_ap(g)
    sound.play_int(x)

    # same alphabets gets injected into ca1
    for k in ca1nrnsNames_:
        g = nrns_[k]
        inject_alphabet(x, g)
        print( '\t%s' % k, g.graph['SeqRec'] )
        if g.graph['SeqRec'].output == 1:
            inject_ap(g)
            playback_background( g )
            g.graph['SeqRec'].reset()
            reset_all_ = True

    if current_num_press_ >= max_num_press_:
        current_num_press_ = 0
        reset_all_ = True

    if reset_all_:
        reset_all()

def reset_all( delay = 1 ):
    global reset_all_
    global current_num_press_
    # remove all events from pygame.
    print( 'RESETTING' )
    pygame.event.clear()
    for k in ca1nrnsNames_:
        g = nrns_[k]
        g.graph['SeqRec'].reset()
    reset_all_ = False
    current_num_press_ = 0
    time.sleep( delay )

def main():
    nrns = init()
    ca3nrns = { k : v for k, v in nrns.items() if 'ca3' in k }
    ca3nrnsNames = list( ca3nrns.keys() )
    for i in range(1000):
        [update(g, i) for g in nrns.values()]
        plot_graphs(nrns)
        if i % 20 == 0:
            gn = random.choice(ca3nrnsNames)
            g = nrns[gn]
            x = random.choice( alphabets_ )
            g['SN'].apply(x)

if __name__ == '__main__':
    main()

