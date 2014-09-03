"""
NOTE: This file requires PIL/Pillow, which is not part of the acwedding_project
requirements. See docs/installation.rst.

PURPOSE:
  This script automatically creates resized banner images based on Twitter
  Bootstrap breakpoints.
  
USAGE:
  Invoke with 'python make_banner.py <srcfile>' where <srcfile> is the path
  to a full size banner image.
  
  The script will create and save new images, with their widths appended to
  their filename, in the same directory as the source image.
  
  The largest banner that will be created has a width of 1200px. Only images
  with widths smaller than the source image will be created.
  
EXAMPLE:
  If invoked with 'python make_banner.py foo/bar/banner.png' then several
  new images will appear in the foo/bar/ directory with names such as:
      banner-480.png
      banner-768.png
      ect...
"""
from os import path
from sys import argv

from PIL import Image

class ArgumentsError(Exception):
    pass

def make_banner_sizes(srcfile):
    srcfile = path.abspath(srcfile)
    dir = path.dirname(srcfile)
    base_filename, ext = path.splitext(path.basename(srcfile))
    
    image = Image.open(srcfile)
    orig_w, orig_h = image.size
    height_ratio = orig_h / orig_w

    for w in (480, 768, 992, 1200):
        if orig_w > w:
            resized_image = image.resize((w, int(height_ratio*w)), Image.ANTIALIAS)
            resized_image_path = path.join(
                dir, 
                '{0}-{1}{2}'.format(base_filename, w, ext)
            )
            resized_image.save(resized_image_path, optimize=True)
            print('Image {0} saved.'.format(resized_image_path))
    
if __name__ == '__main__':
    try:
        srcfile = argv[1]
        if not path.isfile(srcfile):
            raise ArgumentsError()
    except:
        raise ArgumentsError('Usage: python make_banner.py <srcfile>')
        
    make_banner_sizes(srcfile)