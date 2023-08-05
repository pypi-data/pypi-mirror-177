"""
Usage:
    ppm-disp -i
    ppm-disp [-d] <file>...

Options:
    -i  about the tool
    -d  display ppm/pgm images
"""

from docopt import docopt
import cv2 as cv

def show_img(id: int, filepath: str) -> None:
    window_name = "img %d| %s" %(id, cut_string(filepath))
    img = cv.imread(filepath)
    cv.namedWindow(window_name, cv.WINDOW_NORMAL)
    
    width, height, _ = img.shape
    if max(width, height) > 800:
        ratio = width / height
        if width > height:
            cv.resizeWindow(window_name, 600, 600 // ratio)
        else:
            cv.resizeWindow(window_name, round(600 * ratio), 600)
            
    cv.imshow(window_name, img)

def cut_string(x: str) -> None:
    if len(x) > 20:
        return x[:17] + '...'
    return x

def parse_args(args: dict) -> list:
    paths = [i.replace("\\", "/") for i in args["<file>"]]
    return paths

if __name__ == "__main__":
    args = docopt(__doc__)
    if args["-i"] == True:
        print("This tool was written by Hugo in 2022 to display ppm and pgm files.")
    elif args["-d"] == True:
        data = parse_args(args=args)
        for i, val in enumerate(data):
            show_img(i, val);
        cv.waitKey(0)
        cv.destroyAllWindows()