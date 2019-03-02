#!/usr/bin/env python3

# Takes in an image of a shipping receipt, extracts the tracking number, and verifies it
# Authors: Jason Giroux, Seth Phillips
# Uses tracking.py from LiterallyLarry. github.com/LiterallyLarry/USPS-Tracking-Python

import tracking
import pytesseract
import regex
import platform
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter

IMG_PATH = "receipts"  # Directory containing receipt images
PYTESS_CONF = '-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz#:;'

if platform.system() == 'Windows':
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    path_delimeter = '\\'
else:
    path_delimeter = '/'


def main():
    pathlist = Path(IMG_PATH).glob('**/*.jpg')
    for path in pathlist:
        image_path = str(path)
        print(image_path.split(path_delimeter)[1])
        tracking_num = ocr(image_path)
        if not tracking_num:
            print('OCR failed, no tracking number found.')
        else:
            print(tracking_num)
            print(tracking.usps_track(tracking_num))
        print('\n')



def ocr(image_path):
    with Image.open(image_path) as im:
        # im = enhance(im)
        ocr_out_raw = pytesseract.image_to_string(im, config=PYTESS_CONF, lang='eng')
        # print(ocr_out_raw)

    try:
        tracking_num = regex.search('(?:#:)([0-9\\s]+)', ocr_out_raw)[1]
        tracking_num = ''.join(tracking_num.split())  # There's probably a more elegant way to do this.
        return tracking_num

    except TypeError:
        return


def enhance(im):
    t_cont = 112  # Target contrast for image processing

    im = im.convert("RGBA")  # Converts image (usually JPG) data to RGBA data for editing
    im_data = im.getdata()

    newimdata = []
    for pixel in im_data:
        if pixel[0] < t_cont or pixel[1] < t_cont or pixel[2] < t_cont:
            newimdata.append(pixel)
        else:
            newimdata.append((255, 255, 255))
    im.putdata(newimdata)

    im = im.filter(ImageFilter.MedianFilter())  # Apply median filter
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    im = im.convert('1')  # Converts RGBA data to JPG
    im.save(IMG_PATH.split('.')[0] + '_contrast.jpg')
    return im


if __name__ == "__main__":
    main()
