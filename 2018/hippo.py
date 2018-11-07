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

pygame.init()
black_ = 0, 0, 0
screen_ = pygame.display.set_mode(arena.size)

def runApp():
    canvas.init()
    for i in itertools.count():
        canvas.update_canvas( )
        img = np.flipud(np.rot90(arena.canvas_,k=1))
        surface = pygame.surfarray.make_surface(img)
        screen_.blit( surface, (0,0) )
        pygame.display.update()

        # handle event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type != 2:
                continue

            k = chr(event.key)
            if '0' < k < '8':
                reset = canvas.inject_alphabet_ca3(int(k))


def main():
    runApp()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        pygame.quit()
    pygame.quit()
