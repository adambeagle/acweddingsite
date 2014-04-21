"""
NOTE: This file requires PIL/Pillow, which is not part of the acwedding_project
requirements. See docs/installation.rst.

PURPOSE:

This module was written to automate creating thumbnails for static images
in a Django project.

Please note that much of this file wasn't written with general usage in mind;
my particular repository and Django project structure are assumed.
The make_thunbnails function could be easily used as-is in any project,
however.

USAGE:

1. Change PROJECT_NAME to match the name of your Django project.
   Note this is only necessary for usage as described in 3b.

2. If desired, change MAX_SIZE and FORMATS below, just below the imports. 
   See the Pillow docs for supported formats.
   
There are two ways to use the module:

3a. If called with no arguments, a thumbnail will be made of any images 
    located in the same folder as this file whose extension matches one
    found in FORMATS. The thumbnail will be created in this folder as 
    <file>.<original extension>.thumbnail
    
3b. If called with two arguments, srcdir and destdir, thumbnails will be made
    of images in '<repo root>/acwedding/static/images/<srcdir>' and placed in 
    '<repo root>/<PROJECT_NAME>/static/images/<destdir>.' Thumbnails will have the
    file format <original filename>.<original extension>.thumbnail

USAGE NOTES:

* Thumbnails are saved using the png format, regardless of the
  original image's format. The original extension of the image remains in
  its thumbnail filename to make accessing a thumbnail within a template
  easy (merely append '.thumbnail' to the file's original complete name).
  
* srcdir is not traversed recursively.
   
EXAMPLE USAGE:

To create thumbnails of every image found in 
<repo root>/<PROJECT_NAME>/static/gallery and place them in 
<repo root>/<PROJECT_NAME>/static/thumbnails,
run 'python make_thumbnails.py gallery thumbnails' at the command line.

"""

from os import listdir, path
from re import match, IGNORECASE
from sys import argv

from PIL import Image
from unipath import Path

PROJECT_NAME = 'acwedding'
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
            image.thumbnail(MAX_SIZE, Image.ANTIALIAS)
            
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
        
        repoRoot = Path(path.abspath(__file__)).ancestor(2)
        srcdir = str(repoRoot.child(PROJECT_NAME, 'static', 'images', srcdir))
        destdir = str(repoRoot.child(PROJECT_NAME, 'static', 'images', destdir))
        
        if not path.isdir(srcdir):
            raise DirectoryDoesNotExistError(srcdir)
            
        if not path.isdir(destdir):
            raise DirectoryDoesNotExistError(destdir)
    
    # If no arguments passed, thumbnails will be made of any images in the 
    # same folder as this file.
    else:
        filePath = Path(path.abspath(__file__)).parent
        srcdir = destdir = str(filePath)
        
    make_thumbnails(srcdir, destdir)
