#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division
import pygame
import random
import cv2
import canvas
import numpy as np
import itertools
import time
import config
import play
import multiprocessing 
import arduino_client
import config

black_ = 0, 0, 0

# If no activity is detected for timeout_ second, starts random activity.
timeout_ = 10.0
timeWithoutActivity_ = 0

# OpenCV highgui
def on_mouse(event, x, y, flag, params ):
    global timeWithoutActivity_
    if event == 1:
        timeWithoutActivity_ = 0
        W = config.w_ / config.num_notes_
        note = int(x / W) + 1
        if y > 400:
            canvas.inject_alphabet_ca3(note, do_play = True)
            if note == 8:
                canvas.resetAll()

cv2.setMouseCallback( canvas.winName_, on_mouse )

def handle_arduio_command( line, q ):
    cmd, arg = line[:2], line[2:]
    if  len(line) < 2:
        return 
    if cmd == '#B':
        canvas.inject_alphabet_ca3(1+int(arg))
        timeWithoutActivity_ = 0
    elif cmd == '#P':
        canvas.progressFromArduino(arg)
    elif cmd == '#R':
        print( 'Arduino said reset everything.' )
        play.play('a1')
        play.play('a1')
        canvas.resetAll()
        while not q.empty():
            q.get()
    elif cmd == '#T':
        play.play( arg )
    else:
        print( 'Uknown command: %s' % line )


def runApp(q):
    global timeWithoutActivity_, timeout_
    canvas.init()
    t = 0
    for i in itertools.count():
        t0 = time.time()
        canvas.update_graphs()
        if i % 2 == 0:
            canvas.plot_graphs()

        k = 0.85
        #  img = k*config.canvas_ + (1-k)*config.backgroundImg_
        img = config.canvas_
        canvas.show_frame(np.uint8(img))
        dt = time.time() - t0
        t += dt
        timeWithoutActivity_ += dt

        # check for arduino input.
        if not q.empty():
            line = q.get()
            handle_arduio_command( line, q )

        ## if auto is enabled then inject random stimulus.
        #if timeWithoutActivity_ > timeout_:
        #    canvas.inject_alphabet_ca3( random.choice(config.alphabets_))

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
