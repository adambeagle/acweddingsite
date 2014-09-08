from os import listdir, path, symlink
import re
from sys import argv

from PIL import Image

BREAKPOINTS_RES = [480, 768, 992, 1200]
SUFFIXES = ['xs', 's', 'm', 'l']
FORMATS = ['png', 'jpg', 'jpeg']
PATTERN = r'.+\.(?:{0})$'.format('|'.join(FORMATS))
SHRINK_RATIOS = (.8, .7, .6, .5)

def optimize_image(srcpath):
    """ """
    srcpath = path.abspath(srcpath)
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
            dir, 
            '{0}_{1}{2}'.format(base_filename, suffix, ext)
        )
        
        if orig_w > w:
            resized_image = image.resize(
                (w, int(height_ratio*w)), 
                Image.ANTIALIAS
            )
            
            resized_image.save(resized_image_path, optimize=True)
            print('Image {0} saved.'.format(resized_image_path))
        else:
            symlink(srcpath, resized_image_path)
            print('Created symlink: {0} -> {1}'.format(resized_image_path, srcpath))
            
    image.save(srcpath, optimize=True)
    print('Original image {0} optimized and saved.'.format(srcpath))

##############################################################################
if __name__ == '__main__':
    try:
        src = path.abspath(argv[1])
    except IndexError:
        raise ArgumentsError('Usage: python make_banner.py <src>')
        
    if not path.exists(src):
        raise ArgumentsError(
            "Error: {0} is not a valid path".format(src)
        )
    
    # If directory, optimize every image in directory
    if path.isdir(src):
        for file in listdir(src):
            if re.match(PATTERN, file, re.IGNORECASE):
                optimize_image('{0}/{1}'.format(src, file))
                
    # If file, optimize only file
    elif path.isfile(src):
        optimize_image(src)