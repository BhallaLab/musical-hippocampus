#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import pygame
import random
import arena
import cv2
import canvas
import numpy as np
import itertools
import time
import config

#pygame.init()
black_ = 0, 0, 0
#screen_ = pygame.display.set_mode(arena.size)

def runApp():
    canvas.init()
    for i in itertools.count():
        canvas.update_canvas( )
        #img = 0.75*arena.canvas_ #+ 0.25*config.refFig_
        img = arena.canvas_
        #img = np.flipud(np.rot90(img,k=1))
        #s1 = pygame.surfarray.make_surface(img)
        #screen_.blit( s1, (0,0) )
        #pygame.display.update()
        cv2.imshow( "hey", img )
        cv2.waitKey(1)

        #if (i+1) % 20 != 0:
        #    continue

        # if auto is enabled then inject random stimulus.
        if config.args_.auto:
            canvas.inject_alphabet_ca3( random.choice(config.alphabets_))
            continue

        ## handle event
        #for event in pygame.event.get():
        #    if event.type == pygame.QUIT:
        #        quit()

        #    if event.type != 2:
        #        continue

        #    k = chr(event.key)
        #    if '0' < k < '8':
        #        canvas.inject_alphabet_ca3(int(k))
        #    if k in [ 'r', 'q' ]:
        #        canvas.reset_all()


def main( args ):
    config.args_ = args
    runApp()

if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''Hippocampus.'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--auto', '-a'
        , required = False, default = False, action = 'store_true'
        , help = 'Run automatically.'
        )
    class Args: pass 
    args = Args()
    parser.parse_args(namespace=args)
    try:
        main( args )
    except KeyboardInterrupt as e:
        pygame.quit()
    pygame.quit()
