import argparse
import sys
import re

from PIL import Image

def embedBinary(imageBands, binary, startingPoint):
	index = startingPoint
	binary = list(binary)
	reverseImageBands = list(reversed(imageBands))
	newImageBands = []


	while binary: #keep storing data until the binary list is exhausted
		r, g, b = reverseImageBands[index]
		index += 1

		rBin = list(format(r, 'b'))
		rBin[-1] = binary[0]
		rBin = ''.join(rBin)
		#setting least significant bit of the binary string of our red value to the binary value in our list
		r = int(rBin, 2)
		binary.pop(0) 
		if not binary:
			newImageBands.append((r, g, b))
			break
		
		gBin = list(format(g, 'b'))
		gBin[-1] = binary[0]
		gBin = ''.join(gBin)
		g = int(gBin, 2)
		binary.pop(0)
		if not binary:
			newImageBands.append((r, g, b))
			break
		
		bBin = list(format(b, 'b'))
		bBin[-1] = binary[0]
		bBin = ''.join(bBin)
		b = int(bBin, 2)
		binary.pop(0)
		newImageBands.append((r, g, b))

	return (newImageBands, index)


#stores the text length and actual text in the photo starting on the bottom right and moving up to the top left
def encryptImage(imageBands, inputString):
	lengthBinary = textLengthToBinary(inputString)
	lengthBinary = extendTo32Bits(lengthBinary)
	textBinary = textToBinary(inputString)
	reverseImageBands = list(reversed(imageBands))

	modifiedImage = []
	(newImageBands, index) = embedBinary(imageBands, lengthBinary, 0)
	modifiedImage += newImageBands
	(newImageBands, index) = embedBinary(imageBands, textBinary, 11)
	modifiedImage += newImageBands
	modifiedImage += reverseImageBands[index:]
	newModifiedImage = list(reversed(modifiedImage))
	return newModifiedImage



#converts each letter in inputString to an 8 bit binary number and appends it to binaryString
def textToBinary(inputString):
	binaryString = ""
	for letter in inputString:
		letterAsciiVal = ord(letter)
		letterAsBinary = format(letterAsciiVal, '08b')
		binaryString += letterAsBinary
	return binaryString

#converts the length of the inputString from an integer to its respective binary representation
def textLengthToBinary(inputString):
	stringLength = len(inputString)
	stringLength = stringLength*8
	lengthAsBinary = format(stringLength, '08b')
	return lengthAsBinary

def extendTo32Bits(string):
	extendedString = '0' * (32-len(string))
	extendedString = extendedString + string
	return extendedString

def decryptLength(imageBands, sizeOfData, startingPoint):
	#we first need to flip our pixels to start from the bottom right pixels first
	reversedImageBands = list(reversed(imageBands))
	index = 0
	lengthOfText = ""

	while index <= 32:
		r, g, b = reversedImageBands[index]
		index +=1

		rBin = list(format(r, 'b'))
		lengthOfText += rBin[-1]

		gBin = list(format(g, 'b'))
		lengthOfText += gBin[-1]

		bBin = list(format(b, 'b'))
		lengthOfText += bBin[-1]

	return lengthOfText[:32]

def parseBinary(string):
	byteList = re.findall('........', string)
	text = ''
	for byte in byteList:
		integer = int(byte, 2)
		text += chr(integer)
	return text

def decryptText(imageBands, lengthOfText, startingPoint):
	reversedImageBands = list(reversed(imageBands))
	index = startingPoint
	text = ""

	while index <= (lengthOfText+startingPoint):
		r, g, b = reversedImageBands[index]
		index +=1

		rBin = list(format(r, 'b'))
		text += rBin[-1]

		gBin = list(format(g, 'b'))
		text += gBin[-1]

		bBin = list(format(b, 'b'))
		text += bBin[-1]
	string = text[:lengthOfText]
	text = parseBinary(string)
	return text

def decryptImage(imageBands):

	#first we need to get the length of the text that is embedded in the image
	lengthOfText = decryptLength(imageBands, 32, 0)
	lengthOfText = int (lengthOfText, 2)
	#now that we know the length, we can decrypt the text itself
	text = decryptText(imageBands, lengthOfText, 11)

	return text

def main(image, output, text, encrypt):
	#opening image
	image = Image.open(image)
	imageBands = list(image.getdata()) #this saves a list of all the RGB bands in the photo
	#encrypting image
	if encrypt:
		newImage = encryptImage(imageBands, text) #hides our text argument into the imageBands
		image.putdata(newImage)
		output_file = output
		image.save(output_file, 'PNG')

	#decrypting image
	else:
		text = decryptImage(imageBands)
		print text

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	option = parser.add_mutually_exclusive_group(required=True)
	option.add_argument('--encrypt','-e', action='store_true')
	option.add_argument('--decrypt','-d', action='store_true')
	parser.add_argument('image')
	parser.add_argument('--text','-t')
	parser.add_argument('--output','-o')
	args = parser.parse_args()
	main(args.image, args.output, args.text, args.encrypt)
