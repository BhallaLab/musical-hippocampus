#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division
import pygame
import random
import arena
import cv2
import canvas
import numpy as np
import itertools
import time
import config
import sound

black_ = 0, 0, 0

# OpenCV highgui
def on_mouse(event, x, y, flag, params ):
    if event == 1:
        W = arena.canvas_.shape[1] / len(sound.notes)
        note = int(x / W) + 1
        if y > 400:
            canvas.inject_alphabet_ca3(note)
            if note == 8:
                canvas.reset_all()

cv2.setMouseCallback( canvas.winName_, on_mouse )

def runApp():
    canvas.init()
    t = 0
    for i in itertools.count():
        t0 = time.time()
        if i % 2 == 0:
            canvas.update_canvas( )
        k = 0.85
        img = k*arena.canvas_ + (1-k)*config.refFig_
        canvas.show_frame(np.uint8(img))
        t += time.time() - t0
        if i % 10 == 0:
            print( "[INFO ] Current FPS %.2f" % (i/t) )
        
        # if auto is enabled then inject random stimulus.
        if config.args_.auto:
            canvas.inject_alphabet_ca3( random.choice(config.alphabets_))
            continue

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
