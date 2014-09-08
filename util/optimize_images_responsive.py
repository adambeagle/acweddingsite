"""
optimize_images_responsive.py
Author: Adam Beagle

PURPOSE
======
  This script saves resized and optimized versions of images.
  It is intended to create images for use in responsive websites.
  
USAGE
=====
  python optimize_images_responsive.py <src>
  
  'src' must be a path to an existing file or directory.
  
  If 'src' points to a directory, optimized and resized versions of the images
  in the directory (non-recursive) will be placed in the same directory. The 
  original image will also be optimized, but not resized.
  
  If 'src' points to a file, its resized/optimized versions will be saved in the
  same directory as the file. Again, the original file will be optimized but
  not resized.
  
  A file for each size is always created, but an image is never upscaled. 
  If the intended size of the new image is larger than the source image, 
  the new file will be a symlink to the source image.
  
  There are three constants that control how the script behaves. All must
  have equal lengths. They are described below:
  
    BREAKPOINTS_RES : The width breakpoints for the website layout
    SUFFIXES               : What will be appended to the end of each filename
    SHRINK_RATIOS      : The result image's width will be no larger than 
                                    SHRINK_RATIOS[i] * BREAKPOINTS_RES[i].
                                    
EXAMPLE
======
Assuming the following directory structure:
  optimize_images_responsive.py
  images/
    image1.png  (width 800px)
    image2.jpg  (width 400px)

...and the following constants:
  BREAKPOINTS_RES = [480, 768]
  SUFFIXES = ['xs', 's']
  SHRINK_RATIOS = [0.5, 0.6]
  
...after running the following command:
  python optimize_images_responsive.py images
  
...the directory structure would be the following:
  optimize_images_responsive.py
  images/
    image1.png      (width 800px)
    image1_s.png    (width 460px)
    image1_xs.png   (width 240px)
    image2.jpg      (width 400px)
    image2_s.jpg    (symlink -> image2.jpg)
    image2_xs.jpg   (width 240px)
"""
from os import path, symlink
from sys import argv

from PIL import Image

from imageutil import iter_image_paths

BREAKPOINTS_RES = [480, 768, 992, 1200]
SUFFIXES = ['xs', 's', 'm', 'l']
SHRINK_RATIOS = (.8, .7, .6, .5)

def optimize_image(srcpath):
    """ """
    dir = path.dirname(srcpath)
    base_filename, ext = path.splitext(path.basename(srcpath))
    
    image = Image.open(srcpath)
    orig_w, orig_h = image.size
    height_ratio = orig_h / orig_w
    
    breakpoints_w = tuple(zip(
        [int(SHRINK_RATIOS[i]*w) for i, w in enumerate(BREAKPOINTS_RES)],
        SUFFIXES
    ))
    
    for w, suffix in breakpoints_w:
        resized_image_path = path.join(
            dir, '{0}_{1}{2}'.format(base_filename, suffix, ext)
        )
        
        # If new image width < source, save new optimized image
        if orig_w > w:
            resized_image = image.resize(
                (w, int(height_ratio*w)), Image.ANTIALIAS
            )
            resized_image.save(resized_image_path, optimize=True)
            print('Image {0} saved.'.format(resized_image_path))
            
        # If new image width > source image, create symlink to source
        else:
            symlink(srcpath, resized_image_path)
            print('Created symlink: {0} -> {1}'.format(
                resized_image_path, srcpath
            ))
            
    image.save(srcpath, optimize=True)
    print('Original image {0} optimized and saved.'.format(srcpath))

##############################################################################
if __name__ == '__main__':
    try:
        src = path.abspath(argv[1])
    except IndexError:
        raise ArgumentsError('Usage: python make_banner.py <src>')
    
    for imgpath in iter_image_paths(src):
        optimize_image(imgpath)