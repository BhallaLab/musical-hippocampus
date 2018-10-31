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
import numpy as np
import networkx as nx
import subprocess
import swc
import cv2

plt.ion()

canvas_ = np.zeros( shape=(1000,1000,3) )
win_ = cv2.namedWindow( "NRN" )

def cvPos(p, t = 100):
    x1, y1 = p
    return int(x1+t), int(y1+t)

def show_frame( img = None):
    global win_
    if img is None:
        img = canvas_
    cv2.imshow( win_, img )
    cv2.waitKey(10)

def plot_png_using_cv2(G):
    global win_
    global canvas_
    lines = []
    pos = nx.get_node_attributes(G, 'coordinate2D' )
    for n1, n2 in G.edges():
        x1, y1 = cvPos(pos[n1])
        x2, y2 = cvPos(pos[n2])
        c = G.node[n1]['color']
        cv2.line(canvas_, (x1,y1), (x1, y2), (c,c,c) )

def update( i ):
    pass

def main():
    g = swc.swc2nx( './hajos/CNG version/p110715-04-BC.CNG.swc' )
    g.node[1]['color'] = 255
    plot_png_using_cv2( g )
    for i in range(100):
        update(i)
        show_frame( )

if __name__ == '__main__':
    main()

