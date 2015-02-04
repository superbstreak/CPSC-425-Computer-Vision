Python 2.7.6 | 64-bit | (default, Sep 15 2014, 17:36:35) [MSC v.1500 64 bit (AMD64)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> # Assignment 3
>>> from PIL import Image, ImageDraw
>>> import numpy as np
>>> import math
>>> from scipy import signal
>>> import ncc
>>> 
>>> # Question 1
>>> # =====================================================================>

>>> # Done.
>>> 
>>> # Question 2
>>> # =====================================================================>

>>> def MakePyramid(image, minsize):
	# Initialize and Create an empty array
	resulting_pyramid = []
	im = image;
	status = True
	
	# Loop through as long as X and Y are bigger than minsize
	while (status):

		# append the current image to the pyramid
		resulting_pyramid.append(im)
		
		# resize image by multipling 0.75
		newsize0 = im.size[0] * 0.75
		newsize1 = im.size[1] * 0.75
		
		# replace previous image with newly resized image
		im = im.resize((int(newsize0), int(newsize1)), Image.BICUBIC)

		# status check to see if we should keep looping
		status = (im.size[0] >= minsize) and (im.size[1] >= minsize)
		
	return resulting_pyramid

>>> 
>>> judybats = Image.open('C:/Users/Rob/Desktop/faces/judybats.jpg')
>>> print MakePyramid(judybats, 5)
[<PIL.JpegImagePlugin.JpegImageFile image mode=L size=358x342 at 0x63AD748>, <PIL.Image.Image image mode=L size=268x256 at 0x6393BC8>, <PIL.Image.Image image mode=L size=201x192 at 0x6393C08>, <PIL.Image.Image image mode=L size=150x144 at 0x63F4B08>, <PIL.Image.Image image mode=L size=112x108 at 0x63F4BC8>, <PIL.Image.Image image mode=L size=84x81 at 0x63F4C08>, <PIL.Image.Image image mode=L size=63x60 at 0x63F4C88>, <PIL.Image.Image image mode=L size=47x45 at 0x63F4D08>, <PIL.Image.Image image mode=L size=35x33 at 0x63F4D88>, <PIL.Image.Image image mode=L size=26x24 at 0x63F4E08>, <PIL.Image.Image image mode=L size=19x18 at 0x63F4E88>, <PIL.Image.Image image mode=L size=14x13 at 0x63F4F08>, <PIL.Image.Image image mode=L size=10x9 at 0x63F4F88>, <PIL.Image.Image image mode=L size=7x6 at 0x63F7048>]
>>> 
>>> # Question 3
>>> # =====================================================================>
>>> 
>>> def ShowPyramid(pyramid):
	# initilizing values
	w = 0
	h = 0
	offset_x = 0
	offset_y = 0
	
	# loop through every image in the pyramid and find the max w and h
	for im in pyramid:
		w = w + im.size[0]
		if (h < im.size[1]):
			h = im.size[1]
			
	# create a blank image (gray scaled) with the max w and h above
	image = Image.new("L", (w, h))
	
	# loop through the pyramid and paste each image onto the blank image
	for im in pyramid:
		# paste image to the left of the image
		image.paste(im, (offset_x, offset_y))
		
		# increment the offset in X direction to the current img's w
		offset_x = offset_x + im.size[0]
		
	# show the image
	image.show()

	
>>> 
>>> ShowPyramid(MakePyramid(judybats, 1))
>>> 
>>> # Question 4
>>> # =====================================================================>
>>> 
>>> def FindTemplate(pyramid, template, threshold):
	# initialize values
	tracker = []

	# NCC is expensive, so reduce to a more preferable width
	prefered_width = 15

	# resize the template with bicubic interpolation to prefered_width
	# since not all image are perfect suqare, we need to calcuate how much
	# to resize its Y and still retain the image's aspect ratio
	scaledown = template.size[0]/prefered_width
	template = template.resize((prefered_width, template.size[1]//scaledown), Image.BICUBIC)

	# loop through each image in pyramid, compute the NCC
	for im in pyramid:

		# the array of cross-correlation coefficients, in the range -1.0 to 1.0.
		# check whether the threshold is reached
		thresholdLevel = np.where(ncc.normxcorr2D(im, template) > threshold)
		thresholdLevelat0 = thresholdLevel[0]
		thresholdLevelat1 = thresholdLevel[1]

		# append the thresholdLvl to the tracker
		tracker.append(zip(thresholdLevelat1, thresholdLevelat0))

	# If img must support colour. If necessary, you can achieve this with img = img.convert('RGB').
	img = pyramid[0].convert('RGB')

	# For each pixel at which the normalized correlation result is above
	# the threshold, draw lines (forming a rectangle) to mark the boundary of the template
	# at that location. All lines should be shown overlayed on the original image.
	numofitem = len(tracker)
	for pos in range(numofitem):
		multiplier = 0.75 ** pos
		multiplier2X = 2 * multiplier
		# for each item in the array
		for thres in tracker[pos]:
			
			# rectangle
			x1 = (thres[0]//multiplier) - (template.size[0]//multiplier2X)
			y1 = (thres[1]//multiplier) - (template.size[1]//multiplier2X)
			x2 = (thres[0]//multiplier) + (template.size[0]//multiplier2X)
			y2 = (thres[1]//multiplier) + (template.size[1]//multiplier2X)

			# draw read line, calculated rectangle
			draw = ImageDraw.Draw(img)
			draw.rectangle((x1,y1,x2,y2),outline="red")
			del draw

	return img

>>> 
>>> # Question 5
>>> # =====================================================================>
>>> 
>>> # initilize all images
>>> judybats = Image.open('C:/Users/Rob/Desktop/faces/judybats.jpg')
>>> judybats = judybats.convert('L')
>>> students = Image.open('C:/Users/Rob/Desktop/faces/students.jpg')
>>> students = students.convert('L')
>>> tree = Image.open('C:/Users/Rob/Desktop/faces/tree.jpg')
>>> tree = tree.convert('L')
>>> temp = Image.open('C:/Users/Rob/Desktop/faces/template.jpg')
>>> temp = temp.convert('L')
>>> 
>>> # look for the best threshold with cloest to 0 error rate
>>> jb0 = FindTemplate(MakePyramid(judybats, 1), temp, 0.1)
>>> jb0.save('C:/Users/Rob/Desktop/jb0.jpg')
>>> jb1 = FindTemplate(MakePyramid(judybats, 1), temp, 0.2)
>>> jb1.save('C:/Users/Rob/Desktop/jb1.jpg')
>>> jb2 = FindTemplate(MakePyramid(judybats, 1), temp, 0.3)
>>> jb2.save('C:/Users/Rob/Desktop/jb2.jpg')
>>> jb3 = FindTemplate(MakePyramid(judybats, 1), temp, 0.4)
>>> jb3.save('C:/Users/Rob/Desktop/jb3.jpg')
>>> jb4 = FindTemplate(MakePyramid(judybats, 1), temp, 0.5)
>>> jb4.save('C:/Users/Rob/Desktop/jb4.jpg')
>>> jb5 = FindTemplate(MakePyramid(judybats, 1), temp, 0.6)
>>> jb5.save('C:/Users/Rob/Desktop/jb5.jpg')
>>> jb6 = FindTemplate(MakePyramid(judybats, 1), temp, 0.7)
>>> jb6.save('C:/Users/Rob/Desktop/jb6.jpg')
>>> # threshold 0.5 to 0.6 seems to be a good number for judybats
>>> 
>>> st0 = FindTemplate(MakePyramid(students, 1), temp, 0.5)
>>> st0.save('C:/Users/Rob/Desktop/st0.jpg')
>>> st1 = FindTemplate(MakePyramid(students, 1), temp, 0.6)
>>> st1.save('C:/Users/Rob/Desktop/st1.jpg')
>>> # 0.5 to 0.6 seems to be a good range for students as weel
>>> 
>>> tr0 = FindTemplate(MakePyramid(tree, 1), temp, 0.5)
>>> tr0.save('C:/Users/Rob/Desktop/tr0.jpg')
>>> tr1 = FindTemplate(MakePyramid(tree, 1), temp, 0.6)
>>> tr1.save('C:/Users/Rob/Desktop/tr1.jpg')
>>> # 0.5 to 0.6 seems to be a good range for tree as well
>>> 
>>> # Attempting range between 0.5 to 0.6 that would give the best error rate
>>> 
>>> # Checking out judybats
>>> jbx1 = FindTemplate(MakePyramid(judybats, 1), temp, 0.51)
>>> jbx1.save('C:/Users/Rob/Desktop/jbx1.jpg')
>>> jbx2 = FindTemplate(MakePyramid(judybats, 1), temp, 0.52)
>>> jbx2.save('C:/Users/Rob/Desktop/jbx2.jpg')
>>> jbx3 = FindTemplate(MakePyramid(judybats, 1), temp, 0.53)
>>> jbx3.save('C:/Users/Rob/Desktop/jbx3.jpg')
>>> jbx4 = FindTemplate(MakePyramid(judybats, 1), temp, 0.54)
>>> jbx4.save('C:/Users/Rob/Desktop/jbx4.jpg')
>>> jbx5 = FindTemplate(MakePyramid(judybats, 1), temp, 0.55)
>>> jbx5.save('C:/Users/Rob/Desktop/jbx5.jpg')
>>> jbx6 = FindTemplate(MakePyramid(judybats, 1), temp, 0.56)
>>> jbx6.save('C:/Users/Rob/Desktop/jbx6.jpg')
>>> jbx7 = FindTemplate(MakePyramid(judybats, 1), temp, 0.57)
>>> jbx7.save('C:/Users/Rob/Desktop/jbx7.jpg')
>>> jbx8 = FindTemplate(MakePyramid(judybats, 1), temp, 0.58)
>>> jbx8.save('C:/Users/Rob/Desktop/jbx8.jpg')
>>> jbx9 = FindTemplate(MakePyramid(judybats, 1), temp, 0.59)
>>> jbx9.save('C:/Users/Rob/Desktop/jbx9.jpg')
>>> 
>>> # Checking out students
>>> stx3 = FindTemplate(MakePyramid(students, 1), temp, 0.53)
>>> stx3.save('C:/Users/Rob/Desktop/stx3.jpg')
>>> stx4 = FindTemplate(MakePyramid(students, 1), temp, 0.54)
>>> stx4.save('C:/Users/Rob/Desktop/stx4.jpg')
>>> stx5 = FindTemplate(MakePyramid(students, 1), temp, 0.55)
>>> stx5.save('C:/Users/Rob/Desktop/stx5.jpg')
>>> stx6 = FindTemplate(MakePyramid(students, 1), temp, 0.56)
>>> stx6.save('C:/Users/Rob/Desktop/stx6.jpg')
>>> stx7 = FindTemplate(MakePyramid(students, 1), temp, 0.57)
>>> stx7.save('C:/Users/Rob/Desktop/stx7.jpg')
>>> stx8 = FindTemplate(MakePyramid(students, 1), temp, 0.58)
>>> stx8.save('C:/Users/Rob/Desktop/stx8.jpg')
>>> stx9 = FindTemplate(MakePyramid(students, 1), temp, 0.59)
>>> stx9.save('C:/Users/Rob/Desktop/stx9.jpg')
>>> 
>>> # Checking out tree
>>> trx7 = FindTemplate(MakePyramid(tree, 1), temp, 0.57)
>>> trx7.save('C:/Users/Rob/Desktop/trx7.jpg')
>>> trx8 = FindTemplate(MakePyramid(tree, 1), temp, 0.58)
>>> trx8.save('C:/Users/Rob/Desktop/trx8.jpg')
>>> trx6 = FindTemplate(MakePyramid(tree, 1), temp, 0.56)
>>> trx6.save('C:/Users/Rob/Desktop/trx6.jpg')
>>> trx5 = FindTemplate(MakePyramid(tree, 1), temp, 0.55)
>>> trx5.save('C:/Users/Rob/Desktop/trx5.jpg')
>>> trx4 = FindTemplate(MakePyramid(tree, 1), temp, 0.54)
>>> trx4.save('C:/Users/Rob/Desktop/trx4.jpg')
>>> trx3 = FindTemplate(MakePyramid(tree, 1), temp, 0.53)
>>> trx3.save('C:/Users/Rob/Desktop/trx3.jpg')
>>> trx2 = FindTemplate(MakePyramid(tree, 1), temp, 0.52)
>>> trx2.save('C:/Users/Rob/Desktop/trx2.jpg')
>>>
>>> # seems like between 0.53 and 0.54 is where the good threshold stands
>>> stx531 = FindTemplate(MakePyramid(students, 1), temp, 0.531)
>>> stx531.save('C:/Users/Rob/Desktop/stx531.jpg')
>>> jbx531 = FindTemplate(MakePyramid(judybats, 1), temp, 0.531)
>>> jbx531.save('C:/Users/Rob/Desktop/jbx531.jpg')
>>> trx531 = FindTemplate(MakePyramid(judybats, 1), temp, 0.531)
>>> trx531.save('C:/Users/Rob/Desktop/trx531.jpg')
>>> trx531 = FindTemplate(MakePyramid(tree, 1), temp, 0.531)
>>> trx531.save('C:/Users/Rob/Desktop/trx531.jpg')
>>> stx532 = FindTemplate(MakePyramid(students, 1), temp, 0.532)
>>> stx532.save('C:/Users/Rob/Desktop/stx532.jpg')
>>> jbx532 = FindTemplate(MakePyramid(judybats, 1), temp, 0.532)
>>> jbx532.save('C:/Users/Rob/Desktop/jbx532.jpg')
>>> trx532 = FindTemplate(MakePyramid(tree, 1), temp, 0.532)
>>> trx532.save('C:/Users/Rob/Desktop/trx532.jpg')
>>> stx533 = FindTemplate(MakePyramid(students, 1), temp, 0.533)
>>> stx533.save('C:/Users/Rob/Desktop/stx533.jpg')
>>> trx533 = FindTemplate(MakePyramid(tree, 1), temp, 0.533)
>>> trx533.save('C:/Users/Rob/Desktop/trx533.jpg')
>>> jbx533 = FindTemplate(MakePyramid(judybats, 1), temp, 0.533)
>>> jbx533.save('C:/Users/Rob/Desktop/jbx533.jpg')
>>> 
>>> # error rate calcualtion = missed face - non face seen
>>> threshold = 0.400, error rate = +3
>>> threshold = 0.533, error rate = +1
>>> threshold = 0.532, error rate =  0
>>> threshold = 0.521, error rate = -1
>>> threshold = 0.300, error rate = -2
>>> # Therefore, threshold = 0.532 seems like the most 
