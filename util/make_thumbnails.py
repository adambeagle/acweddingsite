"""
NOTE: This file requires PIL/Pillow, which is not part of the acwedding_project
requirements. See docs/installation.rst.

PURPOSE:

This module was written to automate the creation of thumbnails.

"""
from os import listdir, path
from re import match, IGNORECASE
from sys import argv

from PIL import Image, ImageOps

MAX_SIZE = (100, 100)
FORMATS = ('png', 'jpg', 'jpeg') # Case-insensitve

class ArgumentsError(Exception):
    pass

class DirectoryDoesNotExistError(Exception):
    pass

def make_thumbnails(srcdir, destdir):
    pattern = '.+\.(?:{0})$'.format('|'.join(FORMATS))
    
    for f in listdir(srcdir):
        if match(pattern, f, IGNORECASE):
            image = Image.open(path.join(srcdir, f))
            image = ImageOps.fit(image, MAX_SIZE, Image.ANTIALIAS)
            
            destfile = path.join(destdir, f + '.thumbnail')
            image.save(destfile, 'png')
            print('Thumbnail for {0} saved to {1}'.format(f, destfile))
            

if __name__ == '__main__':
    # Get names of source and destination directories from argv and 
    # append them to absolute path of project's static/images/.
    if len(argv) > 1:
        try:
            srcdir, destdir = argv[1:]
        except ValueError:
            raise ArgumentsError('Usage: python make_thumbnails.py' +
                ' <srcdir> <destdir>')
        
        if not path.isdir(srcdir):
            raise DirectoryDoesNotExistError(srcdir)
            
        if not path.isdir(destdir):
            raise DirectoryDoesNotExistError(destdir)
        
    make_thumbnails(path.abspath(srcdir), path.abspath(destdir))
