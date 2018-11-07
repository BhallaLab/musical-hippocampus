"""config.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import cv2

args_ = None

refFig_ = cv2.imread('./hippocampus-800x480.png', 1)
alphabets_ = [1,2,3,4,5,6,7]
ca1_ = [ 
        ((377, 129), 210, './swcs/cell1-11b-CA1.CNG.swc'),
        ((397, 125), 250, './swcs/cell1-2a-CA1.CNG.swc' ),
        ((414, 123), -120,  './swcs/cell1-3-CA1.CNG.swc' ),
        ((430, 124), 60, './swcs/cell1-3a-CA1.CNG.swc'  ),
        ((456, 120), -30,'./swcs/cell1-5b-CA1.CNG.swc'  ),
        ]

ca3_ = [ 
        ((165, 320), -90, './swcs/cell1-CA3.CNG.swc'    ),
        ((158, 308), -150, './swcs/cell1-3a-CA3.CNG.swc' ),
        ((153, 289),  -30, './swcs/cell1-8b-CA3.CNG.swc' ),
        ((153, 275), 90, './swcs/cell13-CA3.CNG.swc'   ),
        ((153, 269), 0, './swcs/cell1-8b-CA3.CNG.swc' ),
        ((151, 251), -60, './swcs/cell1-CA3.CNG.swc'    ),
        ]

# Assign sequences to each neuron.
# Each ca1 neuron must have an entry here.
# Triplet (n1,S, ) where n1 recognize seq S and do the task
connections_ = [
        (0,[4,4,4,4,4,4,4,6,1,3,4]),
        (1,[1,1,3,1,5,4]),
        (2,[5,4,3,4,2,3,3]),
        (3,[1,1,6,6,7,7,6]),
        (4,[4,4,4,8,7,8]),
        ]

alphabetToNrn_ = { 0:0, 1:1, 2:2, 3:3, 4:4, 5:0, 6:1, 7:2, 8:3, 9:4 }
