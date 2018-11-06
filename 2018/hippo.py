#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import pygame
import random
from piano import *
import arena
import cv2
import plot_morph
import numpy as np
import itertools

pygame.init()
black_ = 0, 0, 0
screen_ = pygame.display.set_mode(arena.size)

def runApp():
    plot_morph.init()
    for i in itertools.count():
        plot_morph.update_canvas( )
        img = np.flipud(np.rot90(arena.canvas_,k=1))
        surface = pygame.surfarray.make_surface(img)
        screen_.blit( surface, (0,0) )
        pygame.display.update()
        if i % 20 == 0:
            plot_morph.inject_random_alphabet()

        # handle event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

def main():
    runApp()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        pygame.quit()
    pygame.quit()
