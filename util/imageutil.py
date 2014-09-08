"""
imageutil.py

Purpose:
  This module contains functionalty common to 
  image processing tasks.
"""
from os import listdir, path
import re

FORMATS = ['png', 'jpg', 'jpeg']

def iter_image_paths(srcpath, formats=FORMATS):
    """
    Yield absolute paths of all images in path given by 'srcpath.'
    
    A file is considered an image if its extension matches those given in
    container 'formats' (case insensitive).
    
    If srcpath points to a file, its absolute path will be yielded if it is 
    an image.
    
    If srcpath does not point to an existing file or directory, or it points 
    to a single file that is not an image, ValueError will be raised.
    """
    pattern = r'.+\.(?:{0})$'.format('|'.join(formats))
    srcpath = path.abspath(srcpath)
    if not path.exists(srcpath):
        raise ValueError(
            "{0} not a path to an existing file or directory".format(srcpath)
        )
    
    # If srcpath is directory, yield all image paths
    if path.isdir(srcpath):
        for file in listdir(srcpath):
            if re.match(pattern, file, re.IGNORECASE):
                yield path.join(srcpath, file)
                
    # If srcpath is file, yield if image, otherwise raise ValueError
    elif path.isfile(srcpath):
            if re.match(pattern, srcpath, re.IGNORECASE):
                yield srcpath
            else:
                raise ValueError('{0} is not an image'.format(srcpath))