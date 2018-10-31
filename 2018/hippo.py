#!/usr/bin/python
#  This is a modified version of https://github.com/JesseKuntz/my-piano

try:
    import Tkinter as tk
except ImportError as e:
    import tkinter as tk

from piano import *

h_, w_ = 500, 800

class Hippocampus():

    def __init__(self, parent, controller = None):
        self.parent = parent
        self.canvas = tk.Canvas()
        self.piano = Piano( parent )
        self.canvas.pack( side=tk.TOP )
        self.piano.pack(side=tk.BOTTOM)

    def update(self):
        print( '.', end = '' )


def main():
    root = tk.Tk()
    root.title = 'Hippocampus'
    root.geometry( "%sx%s" % (w_,h_))
    app = Hippocampus(root)
    root.mainloop()

if __name__ == '__main__':
    main()
