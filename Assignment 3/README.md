# CPSC-425-Computer-Vision
Assignment 2: Gaussian filters

The purpose of this assignment is to get some initial experience with Python and to learn the basics of constructing and using linear filters.

-----------------------------------------------------------------------------------------------------------------------------

#1 (3 points)
In CPSC 425, we follow the convention that 2D filters always have an odd number of rows and columns (so that the center row/column of the filter is well-defined).

As a simple warm-up exercise, write a Python function, ‘boxfilter(n)’, that returns a box filter of size n by n. You should check that n is odd, checking and signaling an error with an ‘assert’ statement. The filter should be a Numpy array. For example, your function should work as follows:

>>> boxfilter(5)
array([[ 0.04,  0.04,  0.04,  0.04,  0.04],
       [ 0.04,  0.04,  0.04,  0.04,  0.04],
       [ 0.04,  0.04,  0.04,  0.04,  0.04],
       [ 0.04,  0.04,  0.04,  0.04,  0.04],
       [ 0.04,  0.04,  0.04,  0.04,  0.04]])

>>> boxfilter(4)
Traceback (most recent call last):
  ...
AssertionError: Dimension must be odd
HINT: The generation of the filter can be done as a simple one-line expression. Of course, checking that n is odd requires a bit more work.

Show the results of your boxfilter(n) function for the cases n=3, n=4, and n=5.

#2 (5 points)
Write a Python function, ‘gauss1d(sigma)’, that returns a 1D Gaussian filter for a given value of sigma. The filter should be a 1D array with length 6 times sigma rounded up to the next odd integer. Each value of the filter can be computed from the Gaussian function, exp(- x^2 / (2*sigma^2)), where x is the distance of an array value from the center. This formula for the Gaussian ignores the constant factor. Therefore, you should normalize the values in the filter so that they sum to 1.

HINTS: For efficiency and compactness, it is best to avoid ‘for’ loops in Python. One way to do this is to first generate a 1D array of values for x, for example [-3 -2 -1 0 1 2 3] for a sigma of 1.0. These can then be used in a single Numpy expression to calculate the Gaussian value corresponding to each element.

Show the filter values produced for sigma values of 0.3, 0.5, 1, and 2.

#3 (5 points)
Create a Python function ‘gauss2d(sigma)’ that returns a 2D Gaussian filter for a given value of sigma. The filter should be a 2D array. Remember that a 2D Gaussian can be formed by convolution of a 1D Gaussian with its transpose. You can use the function ‘convolve2d’ in the Scipy Signal Processing toolbox to do the convolution. You will need to provide signal.convolve2d with a 2D array. To convert a 1D array, f, to a 2D array f, of the same size you use ‘f = f[np.newaxis]’

Show the 2D Gaussian filter for sigma values of 0.5 and 1.

#4 (7 points)
Write a function ‘gaussconvolve2d(array,sigma)’ that applies Gaussian convolution to a 2D array for the given value of sigma. The result should be a 2D array. Do this by first generating a filter with your ‘gauss2d’, and then applying it to the array with signal.convolve2d(array,filter,'same'). The ‘same’ option makes the result the same size as the image.

The Scipy Signal Processing toolbox also has a function ‘signal.correlate2d’. Applying the filter ‘gauss2d’ to the array with signal.correlate2d(array,filter,'same') produces the same result as with signal.convolve2d(array,filter,'same'). Why does Scipy have separate functions ‘signal.convolve2d’ and ‘signal.correlate2d’? HINT: Think of a situation in which ‘signal.convolve2d’ and ‘signal.correlate2d’ (with identical arguments) produce different results.

Try downloading an image of your choice from the web (right-click on an image in your browser and choose “save as”). Load this image into Python, convert it to a greyscale, Numpy array and run your ‘gaussconvolve2d’ on it with a sigma of 3.

Use PIL to show both the original and filtered images.

#5 (5 points)
Convolution with a 2D Gaussian filter is not the most efficient way to perform Gaussian convolution on an image. In a few sentences, explain how this could be implemented more efficiently taking advantage of separability and why, indeed, this would be faster. NOTE: It is not necessary to implement this. Just the explanation is required. Your answer will be graded for clarity.
