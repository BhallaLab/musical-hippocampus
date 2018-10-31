#!/usr/bin/python
#  This is a modified version of https://github.com/JesseKuntz/my-piano

try:
    from Tkinter import Tk, Frame, BOTH, Label, PhotoImage
except ImportError:
    from tkinter import Tk, Frame, BOTH, Label, PhotoImage

from piano import *

class Hippocampus():

    def __init__(self, parent, controller = None):
        self.parent = parent
        piano = Piano(parent)
        piano.pack()


def main():
    root = Tk()
    app = Hippocampus(root)
    root.mainloop()

if __name__ == '__main__':
    main()
