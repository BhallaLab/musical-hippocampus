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
import glob
import numpy as np

args_ = None
sdir_       = os.path.dirname( __file__ )

image_files_ = glob.glob( os.path.join(sdir_, 'images', '*.jpg' ))

inset_w_, inset_h_ = 75, 75
images_      = { os.path.basename(f) : cv2.resize(cv2.imread(f,1), 
                (inset_w_,inset_h_)) for f in image_files_ }

# scale the arena by this factor. To make computation faster. After computation
# is done, we rescale the image back to its original size.
h_, w_      = 480, 800
sh_, sw_    = 1, 1

background_ = 0
canvas_     = np.zeros(shape=(int(sh_*h_),int(sw_*w_),3)) + background_

# DO not rescale the background. We can add them later.
backgroundImg_ = cv2.resize( cv2.imread('./hippocampus-800x480.png', 1),(w_, h_))

ca1_ = [ 
        ((sw_*377, sh_*129), 210, './swcs/cell1-11b-CA1.CNG.swc'),
        ((sw_*397, sh_*125), 250, './swcs/cell1-2a-CA1.CNG.swc' ),
        ((sw_*414, sh_*123), -120,  './swcs/cell1-3-CA1.CNG.swc' ),
        ((sw_*430, sh_*124), 60, './swcs/cell1-3a-CA1.CNG.swc'  ),
        ((sw_*456, sh_*120), -30,'./swcs/cell1-5b-CA1.CNG.swc'  ),
        ]

ca3_ = [ 
        ((sw_*165, sh_*320), -90, './swcs/cell1-CA3.CNG.swc'    ),
        ((sw_*158, sh_*308), -150, './swcs/cell1-3a-CA3.CNG.swc' ),
        ((sw_*153, sh_*289),  -30, './swcs/cell1-8b-CA3.CNG.swc' ),
        ((sw_*153, sh_*275), 90, './swcs/cell13-CA3.CNG.swc'   ),
        ((sw_*153, sh_*269), 0, './swcs/cell1-8b-CA3.CNG.swc' ),
        ((sw_*151, sh_*251), -60, './swcs/cell1-CA3.CNG.swc'    ),
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

notes = ["c4","c#4","d4","d#4"
        , "e4","f4","f#4","g4"
        , "g#4", "a5","a#5","b5"
        ,"a2" ];

alphabets_ = list(range(len(notes)))
alphabetToNrn_ = { i : i % 4 for i in alphabets_ }

notes_ = dict( zip(range(1,len(notes)), notes) )

num_notes_ = len(notes_)
