Python 2.7.6 | 64-bit | (default, Sep 15 2014, 17:36:35) [MSC v.1500 64 bit (AMD64)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> from PIL import Image
>>> import numpy as np
>>> import math
>>> from scipy import signal
>>> 
>>> #========================= Question 1 ===================================
>>> def boxfilter(n):
	
	# Check remainder of n is 0 when divided by 2, if==0 it's even
	assert(n%2 != 0), "Dimension must be odd"

	# Initialize an empty list for output
	output = []

	# loop through the y value as we create a square of n X n
	for i in range(0,n):

		# Initialize an empty list for all the row vlaues
		row = []

		# loop through the x value as we create a square of n x n
		for j in range(0,n):		
			row.append(0.04)	# insert value to the row

		# insert completed row to output as the y-th row
		output.append(row)

	# output the list as an array
	return np.asarray(output)

>>> boxfilter(3)
array([[ 0.04,  0.04,  0.04],
       [ 0.04,  0.04,  0.04],
       [ 0.04,  0.04,  0.04]])
>>> 
>>> boxfilter(4)

Traceback (most recent call last):
  File "<pyshell#10>", line 1, in <module>
    boxfilter(4)
  File "<pyshell#8>", line 4, in boxfilter
    assert(n%2 != 0), "Dimension must be odd"
AssertionError: Dimension must be odd
>>> 
>>> boxfilter(5)
array([[ 0.04,  0.04,  0.04,  0.04,  0.04],
       [ 0.04,  0.04,  0.04,  0.04,  0.04],
       [ 0.04,  0.04,  0.04,  0.04,  0.04],
       [ 0.04,  0.04,  0.04,  0.04,  0.04],
       [ 0.04,  0.04,  0.04,  0.04,  0.04]])
>>> 
>>> 
>>> #========================= Question 2 ===================================
>>> def gauss1d(sigma):

        # On piazza instructor said sigma cannot be negative
        assert (sigma > 0), 'Sigma value should be positive'
	
	# multiply sigma by 6 and round up as the length of the array
	length = int(math.ceil(float(sigma) * 6))

	# if it is an even number, add 1 to make it odd
	if (length%2 == 0): length = length + 1

	# calcaute the mid point position
	center = length/2

	# create an array of distance from -mid position to +mid position
	x_dist = np.arange(-center, center + 1)

	# apply the Gaussian function to the array value
	gauss1d_result = np.exp(-(x_dist**2)/(2*sigma**2))

	# normalize the array so they sum up to 1
	gauss1d_result = gauss1d_result/np.sum(gauss1d_result)

	return gauss1d_result

>>> gauss1d(0.3)
array([ 0.00383626,  0.99232748,  0.00383626])
>>> 
>>> gauss1d(0.5)
array([ 0.10650698,  0.78698604,  0.10650698])
>>> 
>>> gauss1d(1)
array([ 0.00333577,  0.0670008 ,  0.18212707,  0.4950727 ,  0.18212707,
        0.0670008 ,  0.00333577])
>>> 
>>> gauss1d(2)
array([ 0.00219981,  0.00597971,  0.04418439,  0.04418439,  0.12010562,
        0.12010562,  0.32648093,  0.12010562,  0.12010562,  0.04418439,
        0.04418439,  0.00597971,  0.00219981])
>>> 
>>> 
>>> #========================= Question 3 ===================================
>>> def gauss2d(sigma):
	# convert a gauss1d array to a 2d array of the same size
	gauss2d_temp = gauss1d(sigma)[np.newaxis]

	# calculate a transpose of the array
	gauss2d_temp_trans = gauss2d_temp.T

	# Gaussian 2D = convolution of 1D Gaussian with its transpose
	gauss2d_result = signal.convolve2d(gauss2d_temp, gauss2d_temp_trans)
	
	return gauss2d_result

>>> gauss2d(0.5)
array([[ 0.01134374,  0.08381951,  0.01134374],
       [ 0.08381951,  0.61934703,  0.08381951],
       [ 0.01134374,  0.08381951,  0.01134374]])
>>> 
>>> gauss2d(1)
array([[  1.11273858e-05,   2.23499518e-04,   6.07534678e-04,
          1.65145048e-03,   6.07534678e-04,   2.23499518e-04,
          1.11273858e-05],
       [  2.23499518e-04,   4.48910782e-03,   1.22026602e-02,
          3.31702695e-02,   1.22026602e-02,   4.48910782e-03,
          2.23499518e-04],
       [  6.07534678e-04,   1.22026602e-02,   3.31702695e-02,
          9.01661409e-02,   3.31702695e-02,   1.22026602e-02,
          6.07534678e-04],
       [  1.65145048e-03,   3.31702695e-02,   9.01661409e-02,
          2.45096982e-01,   9.01661409e-02,   3.31702695e-02,
          1.65145048e-03],
       [  6.07534678e-04,   1.22026602e-02,   3.31702695e-02,
          9.01661409e-02,   3.31702695e-02,   1.22026602e-02,
          6.07534678e-04],
       [  2.23499518e-04,   4.48910782e-03,   1.22026602e-02,
          3.31702695e-02,   1.22026602e-02,   4.48910782e-03,
          2.23499518e-04],
       [  1.11273858e-05,   2.23499518e-04,   6.07534678e-04,
          1.65145048e-03,   6.07534678e-04,   2.23499518e-04,
          1.11273858e-05]])
>>> 
>>> 
>>> #========================= Question 4 ===================================
>>> def gaussconvolved2d(array, sigma):
	# generate a gauss2d filter with defined sigma
	gauss2d_filter = gauss2d(sigma)

	# apply convolution 
	gauss2d_convo = signal.convolve2d(array, gauss2d_filter, 'same')
	
	return gauss2d_convo

>>> im = Image.open('C:\Users\Rob\Desktop\A2_image.png')
>>> im_gray = im.convert('L')
>>> im_array = np.asarray(im_gray)
>>> 
>>> gaussconvolved2d(im_array, 3)
array([[  94.23232072,  106.53824077,  118.84416082, ...,  118.84416082,
         106.53824077,   94.23232072],
       [ 106.53824077,  120.45120676,  134.36417276, ...,  134.36417276,
         120.45120676,  106.53824077],
       [ 118.84416082,  134.36417276,  149.88418469, ...,  149.88418469,
         134.36417276,  118.84416082],
       ..., 
       [ 118.84416082,  134.36417276,  149.88418469, ...,  149.88418469,
         134.36417276,  118.84416082],
       [ 106.53824077,  120.45120676,  134.36417276, ...,  134.36417276,
         120.45120676,  106.53824077],
       [  94.23232072,  106.53824077,  118.84416082, ...,  118.84416082,
         106.53824077,   94.23232072]])
>>> 
>>> im.show()
>>> im_gauss = graussconvolved2d(im_array, 3)
>>> im2 = Image.fromarray(im_gauss.astype('uint8'))
>>> im2.save('C:\Users\Rob\Desktop\A2_filtered.png')
>>> 
>>> 
>>> #======================== Question 5 ====================================
>>> # Convolution with a 2D GAussian filter is not the most efficient way
>>> # to perform Gaussian convolution on an image. The process can get slow
>>> # depending different factors, such as image size. An optimzed solution
>>> # can be achieved by taking advantage of the separability charateristic.
>>> # By applying two Fourier transforms and one inverse Fourier transformation,
>>> # the convolution process can be reduced to multiplication. By separating
>>> # the horizontal and vertical (2D example) and process them, the running
>>> # time will be lower than the original method (O(n^2)).
>>> 
>>> 
>>> def interaction():
	
	# Question 1
	print 'Q1-boxfilter(3)'
	print boxfilter(3)
	print ''
	
	print 'Q1-boxfilter(5)'
	print boxfilter(5)
	print ''

	# Question 2
	print 'Q2-1D(0.3)'
	print gauss1d(0.3)
	print ''
	
	print 'Q2-1d(0.5)'
	print gauss1d(0.5)
	print ''
	
	print 'Q2-1d(1)'
	print gauss1d(1)
	print ''
	
	print 'Q2-1d(2)'
	print gauss1d(2)
	print ''
	
	# Question 3
	print 'Q3=2d(0.5)'
	print gauss2d(0.5)
	print ''
	
	print 'Q3-2d(1)'
	print gauss2d(1)
	print ''
	
	# Question 4
	im = Image.open('C:\Users\Rob\Desktop\A2_image.png')
	im_gray = im.convert('L')
	im_array = np.asarray(im_gray)
	
	print 'Q4-convolve2d(3)'
	print gaussconvolved2d(im_array, 3)
	print ''
	
	im.show()
	im_gauss = gaussconvolved2d(im_array, 3)
	im2 = Image.fromarray(im_gauss.astype('uint8'))
	im2.save('C:\Users\Rob\Desktop\A2_filtered.png')

>>> interaction()
