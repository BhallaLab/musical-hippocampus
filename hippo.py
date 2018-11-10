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
import multiprocessing 
import arduino_client

black_ = 0, 0, 0

# If no activity is detected for timeout_ second, starts random activity.
timeout_ = 10.0
timeWithoutActivity_ = 0

# OpenCV highgui
def on_mouse(event, x, y, flag, params ):
    global timeWithoutActivity_
    if event == 1:
        timeWithoutActivity_ = 0
        W = arena.canvas_.shape[1] / len(sound.notes)
        note = int(x / W) + 1
        if y > 400:
            canvas.inject_alphabet_ca3(note)
            if note == 8:
                canvas.reset_all()

cv2.setMouseCallback( canvas.winName_, on_mouse )

def runApp(q):
    global timeWithoutActivity_, timeout_
    canvas.init()
    t = 0
    for i in itertools.count():
        t0 = time.time()
        if i % 2 == 0:
            canvas.update_canvas( )
        k = 0.85
        img = k*arena.canvas_ + (1-k)*config.refFig_
        canvas.show_frame(np.uint8(img))
        dt = time.time() - t0
        t += dt
        timeWithoutActivity_ += dt
        if i % 10 == 0:
            print( "[INFO ] Current FPS %.2f" % (i/t) )

        # check for arduino input.
        if not q.empty():
            line = q.get()
            if  len(line) < 2:
                continue
            if line[:2] == '#B':
                canvas.inject_alphabet_ca3(1+int(line[2:]))
                timeWithoutActivity_ = 0
            elif line[:2] == '#P':
                progress = line[3:]
                canvas.progressFromArduino(progress)
            elif line[:2] == '#R':
                print( 'Arduino said reset everything.' )
                canvas.resetAll()

        # if auto is enabled then inject random stimulus.
        if timeWithoutActivity_ > timeout_:
            canvas.inject_alphabet_ca3( random.choice(config.alphabets_))

def main( args ):
    config.args_ = args

    # Launch the arduino client in a separate process.
    q = multiprocessing.Queue()
    p = multiprocessing.Process( target=arduino_client.main, args=(q,))
    p.start()
    runApp(q)
    p.join()

if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''Hippocampus.'''
    parser = argparse.ArgumentParser(description=description)
    class Args: pass 
    args = Args()
    parser.parse_args(namespace=args)
    try:
        main( args )
    except KeyboardInterrupt as e:
        pass
