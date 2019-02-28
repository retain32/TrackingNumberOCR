import pytesseract
from pytesseract.pytesseract import image_to_string

# pytesseract.pytesseract.tesseract_cmd = r"/usr/local/bin/tesseract"
import regex
from PIL import Image, ImageEnhance, ImageFilter

IMG_PATH = "usps_sample.jpg"
T_CONT = 112  #Target contrast for image processing
PYTESS_CONF = '-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz#:;'

im = Image.open(IMG_PATH)
im = im.convert("RGBA") #Converts image (usually JPG) data to RGBA data for editing
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
im = im.convert('1')  #Converts RGBA data to JPG
# im.save(IMG_PATH.split('.')[0] + '_contrast.jpg')
ocr_output = pytesseract.image_to_string(im, config=PYTESS_CONF, lang='eng')
# print(ocr_output)

sudhfasdjf = regex.search('(?:#:)([0-9\\s]+)', ocr_output)[1]
print(sudhfasdjf)
