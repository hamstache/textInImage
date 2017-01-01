Text In Image Project

Written by Josh Moynihan

This project writes plain text into a JPG photo and exports the photo as PNG. The plain text can then be extracted from the PNG photo and displayed in the console. The program uses Python's Pillow to obtain a list of each pixel's RGB values for the photo. The least significant bit of each RGB value is altered to the binary bits representing the plain text message we want to embed. 

To encrypt an image enter the following command in the directory of textInImage.py:

python textInImage.py -e [name of JPG image to encrypt] -o [name of PNG image to output to] -t [string of plain text to encrypt into photo]

To decrypt an image enter the following command in the directory of textInImage.py:

python textInImage.py -d [name of PNG image to decrypt message from]