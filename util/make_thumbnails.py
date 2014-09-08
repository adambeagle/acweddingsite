"""
make_thumbnails.py
Author: Adam Beagle

NOTE: This file requires PIL/Pillow, which is not part of the acwedding_project
requirements. See docs/installation.rst.

PURPOSE
=======
  This module automates the creation of thumbnails.
  Thumbnails are ugly-cropped to fit a square.
  
USAGE
=====
  python make_thumbnails.py <src> <destdir>

  Two path arguments must be provided, 'src' and 'destdir.'
  
  If 'src' is a directory path, thumbnils of all image files within the 
  directory (non-recursive) will be placed in 'destdir.'
  
  If 'src' is a file path, its thumbnail will be placed in 'destdir.'
  
  The thumbnail files are the original filename, with extension,
  with ".thumbnail" appended. 

EXAMPLE
=======
  Assuming the following directory structure:
    make_thumbnails.py
    images/
      image1.png
      image2.jpg
    thumbnails/
    
  After running the following command...
    python make_thumbnails.py images thumbnails
  ...the directory structure would be the following:
  
  make_thumbnails.py
  images/
    image1.png
    image2.jpg
  thumbnails/
    image1.png.thumbnail
    image2.jpg.thumbnail
"""
from os import listdir, path
from re import match, IGNORECASE
from sys import argv

from PIL import Image, ImageOps

from imageutil import iter_image_paths

class ArgumentsError(Exception):
    pass
    
class DirectoryDoesNotExistError(Exception):
    pass

MAX_SIZE = (100, 100)

def make_thumbnail(srcpath, destdir, max_size=MAX_SIZE):
    """
    Saves a thumbnail of image pointed to by 'srcpath' in 'destdir.'
    MAX_SIZE expects length 2 container (width, height)
    """
    image = Image.open(srcpath)
    image = ImageOps.fit(image, MAX_SIZE, Image.ANTIALIAS)
    
    destpath = path.join(destdir, path.basename(srcpath)  + '.thumbnail')
    image.save(destpath, 'png')
    print('Thumbnail for {0} saved to {1}'.format(srcpath, destpath))

##############################################################################
if __name__ == '__main__':
    try:
        src, destdir = argv[1:3]
    except ValueError:
        raise ArgumentsError('Usage: python make_thumbnails.py' +
            ' <src> <destdir>')
    
    destdir = path.abspath(destdir)
    if not path.isdir(destdir):
        raise DirectoryDoesNotExistError(destdir)
        
    for imgpath in iter_image_paths(src):
        make_thumbnail(imgpath, destdir)
