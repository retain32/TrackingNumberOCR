#!/usr/bin/env python3

# Takes in an image of a shipping receipt, extracts the tracking number, and verifies it
# Authors: Jason Giroux, Seth Phillips
# Uses tracking.py from LiterallyLarry. github.com/LiterallyLarry/USPS-Tracking-Python


import pytesseract
import regex
import platform
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter

IMG_PATH = "receipts"  # Directory containing receipt images
T_CONT = 112  # Target contrast for image processing
PYTESS_CONF = '-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz#:;'

if platform.system() == 'Windows':
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"


def main():
    pathlist = Path(IMG_PATH).glob('**/*.jpg')
    for path in pathlist:
        image_path = str(path)
        print(image_path)
        ocr(image_path)


def ocr(image_path):
    with Image.open(image_path) as im:
        # im = enhance(im)
        ocr_out_raw = pytesseract.image_to_string(im, config=PYTESS_CONF, lang='eng')
        # print(ocr_out_raw)

    try:
        tracking_num = regex.search('(?:#:)([0-9\\s]+)', ocr_out_raw)[1]
        tracking_num = ''.join(tracking_num.split())  # There's probably a more elegant way to do this.
        print(tracking_num + '\n')

    except TypeError:
        print('OCR failed, no tracking number found.\n')


def enhance(im):
    im = im.convert("RGBA")  # Converts image (usually JPG) data to RGBA data for editing
    im_data = im.getdata()

    newimdata = []
    for pixel in im_data:
        if pixel[0] < T_CONT or pixel[1] < T_CONT or pixel[2] < T_CONT:
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
