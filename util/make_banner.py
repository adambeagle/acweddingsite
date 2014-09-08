"""
make_banner.py
Author: Adam Beagle
"""
from os import path
from sys import argv, exit

from PIL import Image

import optimize_images_responsive as oir

if __name__ == '__main__':
    try:
        srcpath = path.abspath(argv[1])
    except IndexError:
        exit('Usage: python[3] {0} <srcfile>'.format(__file__))
    
    oir.SUFFIXES = [str(w) for w in oir.BREAKPOINTS_RES]
    oir.SHRINK_RATIOS = [1 for w in oir.BREAKPOINTS_RES]
    oir.optimize_image(srcpath, 'jpg', progressive=True)
    