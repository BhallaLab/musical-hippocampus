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
import numpy as np
import networkx as nx
import operator
import math
import swc
import cv2
import random
import sequence
import play
import time
import config
import matplotlib.cm as cm

nrns_              = {}
ca3nrnsNames_      = None
ca1nrnsNames_      = None
max_num_press_     = 20
current_num_press_ = 0
reset_all_         = False
note_loc_          = { }
winName_           = "HIPPOCAMPUS"
title_             = ''
match_arduino_     = ''

win_               = cv2.namedWindow( winName_ )
try:
    cv2.setWindowProperty(winName_, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
except Exception as e:
    # Older version
    cv2.setWindowProperty(winName_, cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)

def int2Clr2(x):
    b = int(x)
    left = 255 - b
    r = max(0, left//2)
    g = max(0, left//2)
    b = 255 - r - g
    return (r, g, b)

def int2Clr( x ):
    c = [int(a*255) for a in cm.rainbow(x/255.0)]
    return c

def add_piano( pressed = 0 ):
    # Note that surface rotate is by 180 degree.
    global note_loc_
    h, w, _ = config.canvas_.shape 
    stripeW = int(w/config.num_notes_)
    stripeH = int(80 * config.sh_)
    for i in range(w//stripeW):
        color =  255 if i % 2 else 0
        p1, p2 = (i*stripeW, h-stripeH), ((i+1)*stripeW, h-1)
        p0 = (i*stripeW+stripeW//2, h-stripeH//2)
        img = np.ascontiguousarray(config.canvas_, dtype=np.uint8)
        cv2.rectangle( img, p1, p2, int2Clr(color), -1)
        cv2.putText( img, str(i+1), p0,  cv2.FONT_HERSHEY_SIMPLEX, 1, int2Clr(128), 2)
        note_loc_[i+1] = (p0,p1,p2)
    if pressed:
        change_color(img, note_loc_[pressed])
    config.canvas_ = img

def change_color( img, ps ):
    p0, p1, p2 = ps
    #  cv2.rectangle( img, p1, p2, int2Clr(color), cv2.FILLED)
    cv2.circle( img, p0, 20, int2Clr(80), 2, -1 )

def schaffer_collateral( segments = 10, zigzag = 0, origin = None ):
    if os.path.isfile( 'sc.txt' ):
        # add zigzag
        path = np.loadtxt('sc.txt')
        path = np.multiply(path, [config.sw_, config.sh_])
        path = path[1:]
        path += np.random.randint(-zigzag, zigzag, size=(path.shape))
        return path
    return schaffer_collateral_bezier(segments, zigzag, origin)

def schaffer_collateral_bezier( segments=10, zigzag=10, origin=None):
    # otherwise use bezier module. It is not available on PI.
    import bezier
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
    np.savetxt('sc.txt', path )
    return path

def ca1Toca3( ):
    path = schaffer_collateral()
    g = nx.path_graph(len(path), create_using=nx.DiGraph() )
    for n, p in zip(g.nodes(), path):
        g.node[n]['color'] = 255
        g.node[n]['coordinate'] = tuple(map(int,p))
    for n1, n2 in g.edges():
        g[n1][n2]['width'] = 3
    return g


def _sub(t1, t2):
    return tuple(map(operator.sub, t1, t2))

def _add(t1, t2):
    return tuple(map(operator.add, t1, t2))

def show_frame( img, background = True):
    img = cv2.resize(config.canvas_, (config.w_, config.h_))
    if background:
        k = 0.8
        img = k * img + (1-k) * config.backgroundImg_
    cv2.imshow( winName_, np.uint8(img) )
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

def plot_png_using_cv2(G, every = 1):
    global win_
    global title_
    pos = nx.get_node_attributes(G, 'coordinate' )
    # draw the soma.
    somaColor = int2Clr(G.graph['SeqRec']._output*128  + 0.5*G.node[1]['color'])
    cv2.circle( config.canvas_, pos[1], 5, somaColor, -1 )
    for i, (n1, n2) in enumerate(G.edges()):
        if i % every != 0:
            continue
        (x1, y1), (x2, y2) = pos[n1], pos[n2]
        cv2.line( config.canvas_, (x1,y1), (x2, y2)
                , int2Clr(G.node[n2]['color'])
                , G[n1][n2].get('width', 1)
                )

    # write the current number and max numbers.
    txt =  '%d/%d' % (current_num_press_, max_num_press_)
    title = '%s: %s' % (txt, match_arduino_)
    p0 = (10,10)
    c = 50*(current_num_press_ / max_num_press_ )
    cv2.rectangle(config.canvas_, (0,0), (config.w_,20), int2Clr(c+230), -1)
    cv2.putText(config.canvas_, title, (10,10),  cv2.FONT_HERSHEY_SIMPLEX, 0.4, int2Clr(0), 1)

    # plot the progress bar.
    if match_arduino_:
        o = 0
        p = 100 * max([float(x) for x in match_arduino_.split(',') if x.strip()])
        cv2.rectangle( config.canvas_, (o,10), (o+int(p), 20), int2Clr(0), -1 ) 


def plot_graphs( every = 1 ):
    global hippoImg_
    global nrns_
    for g in nrns_.values():
        if g.graph['active']:
            plot_png_using_cv2(g, every)

def update(g):
    aps = g.graph['AP']
    if len(aps)==0:
        g.graph['active'] = False
    if not g.graph['active']:
        return 
    nexts = []
    for n in aps:
        c = g.node[n]['color']
        if c == 0:
            break
        g.node[n]['color'] = c 
        for p in g.successors(n):
            g.node[p]['color'] = g.node[n]['color']
            nexts.append(p)
        g.node[n]['color'] = 0
    g.graph['AP'] = nexts

def inject_ap(g):
    g.graph['AP'] = [1]
    g.graph['active'] = True
    for n in g.nodes():
        g.node[n]['color'] = 0
    g.node[1]['color'] = 255

def create_canvas( ):
    add_piano( )
    for i, (pos, theta, k) in enumerate(config.ca1_):
        pos = tuple(int(x) for x in pos)
        g = swc.swc2nx(k, scale=0.1 )
        #  print( g.number_of_nodes() )
        preprocess( g, rotate=theta, shift=pos )
        inject_ap(g)
        g.graph['SeqRec'] = sequence.SeqRecognizer([])
        n1, seq = config.connections_[i]
        g.graph['SeqRec'] = sequence.SeqRecognizer(seq)
        nrns_['ca1.%d'%i] = g

    for i, (pos, theta, k) in enumerate(config.ca3_):
        pos = tuple(int(x) for x in pos)
        g = swc.swc2nx(k, scale=0.1)
        preprocess( g, rotate=theta, shift=pos )
        scPath = schaffer_collateral( zigzag=4, origin= g.node[1]['coordinate'] )
        swc.add_axon(i, g, scPath)
        g.graph['SeqRec'] = sequence.SeqRecognizer([])
        nrns_['ca3.%d'%i] = g 
        inject_ap(g)

def update_graphs():
    global nrns_
    [update(g) for g in nrns_.values()]

def update_canvas( ):
    global nrns_
    update_graphs()
    plot_graphs( )

def init():
    global ca3nrnsNames_
    global ca1nrnsNames_
    create_canvas()
    ca3nrns = { k : v for k, v in nrns_.items() if 'ca3.' in k }
    ca1nrns = { k : v for k, v in nrns_.items() if 'ca1.' in k }
    ca3nrnsNames_ = list( ca3nrns.keys() )
    ca1nrnsNames_ = list( ca1nrns.keys() )
    add_piano()

def inject_alphabet( x, g, do_play=False):
    # Arduino has sequence recognizer.
    #  g.graph['SeqRec'].inject(x)
    if do_play:
        play.play(config.notes_[x])

def playback_background( g ):
    import subprocess
    seq = [str(x) for x in g.graph['SeqRec'].seq]
    subprocess.Popen( [ "timeout", "5", "python", "./play.py" ] + seq )

def inject_alphabet_ca3(x, g = None, do_play = False):
    global ca1nrnsNames_
    global reset_all_
    global max_num_press_
    global current_num_press_
    global title_
    current_num_press_ += 1

    if g is None:
        g = nrns_['ca3.%d'% config.alphabetToNrn_[x] ]
    inject_ap(g)

    if do_play:
        play.play(config.notes_[x])

    add_piano(x)

    # same alphabets gets injected into ca1. Print the status of their output.
    title_ = ''
    for k in ca1nrnsNames_:
        g = nrns_[k]
        inject_alphabet(x, g)
        #  print( '\t%s' % k, g.graph['SeqRec'] )
        title_ += '%.2f|' % g.graph['SeqRec']._output
        if g.graph['SeqRec'].output == 1:
            inject_ap(g)
            g.graph['SeqRec'].reset()
            reset_all_ = True

    if current_num_press_ >= max_num_press_:
        current_num_press_ = 0
        reset_all_ = True

    if reset_all_:
        resetAll()

def resetAll( delay = 1 ):
    global reset_all_
    global current_num_press_
    global title_
    init()
    for k in ca1nrnsNames_:
        g = nrns_[k]
        g.graph['SeqRec'].reset()
    reset_all_ = False
    current_num_press_ = 0
    time.sleep( delay )

def main():
    global nrns_
    init()
    ca3nrns = { k : v for k, v in nrns_.items() if 'ca3' in k }
    for i in range(1000):
        [update(g) for g in nrns_.values()]
        plot_graphs( )
        if i % 10 == 0:
            gn = random.choice(ca3nrnsNames_)
            g = nrns_[gn]
            x = random.choice( config.alphabets_ )
            inject_alphabet_ca3( x )
        
        cv2.imshow( 'test', config.canvas_ )
        cv2.waitKey(1)

def progressFromArduino( progress ):
    global match_arduino_
    match_arduino_ = progress

if __name__ == '__main__':
    main()

