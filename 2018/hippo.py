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

pygame.init()
black_ = 0, 0, 0
screen_ = pygame.display.set_mode(arena.size)

def runApp():
    canvas.init()
    for i in itertools.count():
        canvas.update_canvas( )
        img = 0.8 * arena.canvas_ + 0.2 * config.refFig_
        img = np.flipud(np.rot90(img,k=1))
        surface = pygame.surfarray.make_surface(img)
        screen_.blit( surface, (0,0) )
        pygame.display.update()

        if (i+1) % 10 != 0:
            continue

        # handle event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type != 2:
                continue

            k = chr(event.key)
            if '0' < k < '8':
                canvas.inject_alphabet_ca3(int(k))
            if k in [ 'r', 'q' ]:
                canvas.reset_all()


def main():
    runApp()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        pygame.quit()
    pygame.quit()
