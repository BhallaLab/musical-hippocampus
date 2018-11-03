#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""swc_to_tikz.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import codecs
import numpy as np
import re
import networkx as nx
import random
args_ = None

def _get_node_type( t ):
    types = { 0: 'undefined', 1 : 'soma', 2 : 'axon', 3 : 'dendrite'
            , 4 : 'apical dendrite', 5 : 'fork point', 6 : 'end point'
            , 7 : 'custom' }
    return types[int(t)]

def _parse_line( line ):
    n, T, x, y, z, R, P = line.split()
    x, y, z, R = [ float(a) for a in (x,y,z,R) ]
    n, P = int(n), int(P)
    nodeType = _get_node_type(T)
    return n, nodeType, x, y, z, R, P

def _add_coordinates( G, n, pos ):
    G.node[n]['coordinate'] = to2d(pos)
    G.node[n]['pos'] = '%f,%f!' % tuple(to2d(pos[:2]))

def _print_stats( morph ):
    print( ' Number of nodes: %d' % morph.number_of_nodes() )
    print( ' Number of edges: %d' % morph.number_of_edges() )

def to2d( point ):
    if len(point) > 2:
        point = point[:2]
    return tuple([int(x)//6 for x in point])

def add_axon( gid,  g, soma_path ):
    prev = 1
    for i, coord in enumerate(soma_path):
        x, y = map(int, coord)
        nName = 'axon%s%d' % (gid,i)
        g.add_node(nName, coordinate = (x,y))
        g.add_edge(prev, nName, width = 1)
        prev = nName

def _nx_to_paths( G ):
    # Create list of paths.
    g = G.copy()
    root = 1
    paths = []
    sinks = [ n for n, outd in list(G.out_degree()) if outd == 0 ]
    for s in sinks:
        # There is only one path from each sink to source.
        path = [s]
        edges = []
        while g.in_degree(path[-1]) > 0:
            # select a incoming vertices
            v = path[-1]
            f = list(g.predecessors(v))[0]
            edges.append( (f,v) )
            path.append(f)
        paths.append(path)
        # Remove these edges
        g.remove_edges_from(edges)
    return paths

def do_save_png( G, outfile):
    global args_
    fig = plt.figure()
    if args_.engine == 'networkx':
        do_save_png_using_nx(G, outfile)
    elif args_.engine == 'matplotlib':
        do_save_png_using_mpl3d(G, outfile)
    else:
        raise UserWarning( "Unknown engine %s" % engine )
    plt.savefig( outfile )

def _distance( p1, p2):
    d = 0
    for a, b in zip(p1,p2):
        d += (a-b)**2
    return d**0.5

def _smooth_path( path ):
    import scipy.interpolate as sci
    import numpy as np
    path = np.array(path)
    if len(path) > 3:
        X, Y, Z = path[:,0], path[:,1], path[:,2]
        tck, u = sci.splprep( [X,Y,Z])
        newX = np.linspace(0, 1, len(X))
        res = sci.splev(newX, tck)
        path = zip(*res)
    return path

def _length(s, t, G):
    p1 = G.node[s]['coordinate']
    p2 = G.node[t]['coordinate']
    return sum([(a-b)**2 for (a,b) in zip(p1,p2)]) ** 0.5

def _sanitize_morphology(G):
    # Housekeeping.
    # Make sure each node has 'pos' attribute
    remove = [ n for n in G.nodes() if 'coordinate' not in G.node[n]]
    G.remove_nodes_from(remove)

def resample( g, every ):
    G = nx.DiGraph()
    sinks = [ n for n, outd in list(g.out_degree()) if outd == 0 ]
    for s in sinks:
        # There is only one path from each sink to source.
        path = [s]
        while g.in_degree(path[-1]) == 1:
            # select a incoming vertices
            v = path[-1]
            f = list(g.predecessors(v))[0]
            path.append(f)
        sampled = path[::every] 
        if sampled[-1] != path[-1]:
            sampled.append(path[-1])
        for n2, n1 in zip(sampled, sampled[1:]):
            G.add_node(n1, **g.node[n1] )
            G.add_node(n2, **g.node[n2] )
            G.add_edge(n1, n2)
    return G

def swc2nx( swcfile, scale = 1 ):
    morph = nx.DiGraph()
    with codecs.open( swcfile, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line or line[0] == '#':
                continue
            n, T, x, y, z, R, P = _parse_line(line)
            morph.add_node(n, type=T, shape='point', radius=R, color=1 )
            _add_coordinates(morph, n, (x,y,z))
            if P < 0:
                continue
            morph.add_edge(P, n, length = _length(P,n,morph) )
    _sanitize_morphology(morph)

    everyN = int(1 / scale)
    morph = resample(morph, everyN)
    return morph
