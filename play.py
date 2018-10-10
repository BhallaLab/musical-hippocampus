#!/usr/bin/env python
import sys
import sound
sound.play_seq( map(int, sys.argv[1:]) )
