#!/usr/bin/python
#  This is a modified version of https://github.com/JesseKuntz/my-piano

try:
    import Tkinter as tk
except ImportError as e:
    import tkinter as tk

from piano import *

class Hippocampus():

    def __init__(self, parent, controller = None):
        self.parent = parent
        canvas = tk.Canvas()
        piano = Piano(parent)
        canvas.pack()
        piano.pack()


def main():
    root = tk.Tk()
    app = Hippocampus(root)
    root.mainloop()

if __name__ == '__main__':
    main()
