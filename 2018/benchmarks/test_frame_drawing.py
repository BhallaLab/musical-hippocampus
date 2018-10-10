import cv2
import numpy as np
import time

winName_ = 'Hey'
win_ = cv2.namedWindow( winName_ )
img_ = np.zeros( shape=(800,480,3) )

try:
    cv2.setWindowProperty(winName_, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
except Exception as e:
    # Older version
    cv2.setWindowProperty(winName_, cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)

def int2Clr( x ):
    import matplotlib.cm as cm
    c = [int(a*255) for a in cm.rainbow(x/255.0)]
    return c
    #  b = int(x)
    #  left = 255 - b
    #  r = max(0, left//2)
    #  g = max(0, left//2)
    #  b = 255 - r - g
    #  return (r, g, b)

def add_piano( pressed = 0 ):
    # Note that surface rotate is by 180 degree.
    global img_
    h, w, _ = img_.shape 
    stripeW = 20
    stripeH = 80
    for i in range(w//stripeW):
        color =  255 if i % 2 else 0
        p1, p2 = (i*stripeW, h-stripeH), ((i+1)*stripeW, h-1)
        p0 = (i*stripeW+stripeW//2, h-stripeH//2)
        img = np.ascontiguousarray(img_, dtype=np.uint8)
        cv2.rectangle( img, p1, p2, int2Clr(color), -1)
        cv2.putText( img, str(i+1), p0,  cv2.FONT_HERSHEY_SIMPLEX, 1, int2Clr(128), 2)
    return img


def main():
    i, t = 0, 0
    while True:
        i += 1
        t0 = time.time()
        img_ = np.random.randint(0,256, size=(800,480,3))
        img_ = add_piano()
        cv2.imshow( winName_, np.uint8(img_) )
        cv2.waitKey(1)
        dt = time.time() - t0
        t += dt 
        i += 1
        if i % 10 == 0:
            print( 'Rate is %.2f' % (i/t))


main()
