import os
import numpy as np
import cv2

sdir_       = os.path.dirname( __file__ )
background_ = 0
h_, w_      = 480, 800
canvas_     = np.zeros( shape=(h_,w_,3) ) + background_
#  win_        = cv2.namedWindow( "NRN" )
hippoImg_   = cv2.imread( os.path.join( sdir_, 'hippocampus-800x480-1.png' ) )
size        = (w_, h_)
