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

pygame.init()
black_ = 0, 0, 0
screen_ = pygame.display.set_mode(arena.size)

def runApp():
    nrns = plot_morph.init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        
        #  cv2.line( arena.canvas_, (10,10), (random.randint(10,100),100), (255,255,255), 3 )
        plot_morph.update_canvas( nrns )
        surface = pygame.surfarray.make_surface(
                    np.flipud(np.rot90(arena.canvas_,k=1))
                )
        screen_.blit( surface, (0,0) )
        pygame.display.update()

def main():
    runApp()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        pygame.quit()
    pygame.quit()
