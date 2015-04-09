# CPSC-425-Computer-Vision
The purpose of this assignment is to understand and implement the optical flow algorithm of Bruce D. Lucas and Takeo Kanade.

The assignment

This assignment is based on work described in the classic 1981 paper, “An iterative image registration technique with an application to stereo vision,” (PDF) by Lucas and Kanade. If you read this paper, you will realize two things. First, the term “optical flow” does not appear in the paper. As the title suggests, the target application was stereo vision. Second, the method described in the paper is much more general (and therefore more complicated) than the simple version we use here for optical flow. It is not necessary to understand the Lucas–Kanade paper in detail for this assignment. Sufficient for our purposes is to understand the Wikipedia article Lucas–Kanade method.

The zip file containing an eight frame image sequence and skeleton code is hw6.zip. Download this file to your directory and unzip with the command

unzip hw6.zip
The assign directory contains one sequence of images demonstrating optical flow taken from the Middlebury optical flow dataset. The images we use were created synthetically, an approach often used in optical flow research. Information about the dataset (Grove2), other datasets, and a paper comparing state–of–the–art approaches to optical flow, can be found at:

http://vision.middlebury.edu/flow/
You can run the skeleton program by typing

python OpticalFlow.py
at the command prompt. The script will display the first frame in the image sequence.

The Lucas–Kanade optical flow method is a dense method. That is, the method computes optical flow at every pixel in each frame. To keep things simple for this assignment, we instead compute optical flow only at a given point in each frame. The point you are assigned is based on your student number, as described in the skelton program.

As written, the script displays a red cross at the given point and a yellow diamond at the location where the given point has moved to in the next image. Of course, in the skeleton program, no actual optical flow has yet been computed. Instead, the skeleton program displays a hard-coded optical flow value (set as [-1,2]). This will allow you to orient yourself to the coordinate system used.

In this assignment, you will re-use functions from Assignment 2. Of course, you'll need to be sure your functions from Assignment 2 are debugged and working correctly.

(5 points)
We consider input images two frames at a time. The first step is to estimate the partial derivatives Ix, Iy and It. Note: Ix and Iy are partial derivatives with respect to position, x and y, in the first frame. It is the partial derivative with respect to time from the first frame to the second.

Derivatives are estimated in the function Estimate_Derivatives. A simple approach suffices. The first frame is smoothed with a 2D Gaussian (default sigma=1.5). Do this by uncommenting the first line in the function definition (where gaussconvolve2d is the function you wrote in Assignment 2).

If in doubt, display the smoothed image to confirm that it is being correctly computed.

To complete the function, estimate the partial derivatives Ix, Iy for the first frame using first central differences in the x and y directions respectively. Hint: Use the numpy function np.gradient to compute both central differences efficiently.

Finally, estimate the partial derivative It using pixel differences between the first frame and the second frame. To make this estimate a bit more robust, smooth both original frames with a boxfilter of size n (default n=3) prior to computing the pixel differences. Use your function boxfilter from Assignment 2 to compute the required boxfilter.

Before proceeding, check your implementation of Estimate_Derivatives to make sure all your partial derivative estimates returned are the same size as the original image.

(10 points)
Complete the definition of the function Optical_Flow given in the skeleton program. This is where you compute

v = (ATA)-1ATb
as described in the Wikipedia article Lucas–Kanade method.

Make sure that you compute optical flow at the single (x, y) position assigned to you, based on student number. You compute optical flow using a square window of size window_size centered at your given (x, y). We will follow the convention that window_size is an odd number (so that its center row and column are well defined). Hints: You can stack two numpy arrays using the function np.vstack. Similarly, you can flatten a 2-dimenstional numpy array to a 1-dimensional array using the function np.flatten. Also, you can use the function pinv in the numpy linalg module to compute the (Moore-Penrose) pseudo-inverse of a matrix.

A test script to run optical flow code on frame07.png and frame08.png, the first two frames in the test sequence, is included in the skeleton program. Run this for the point that you have been assigned. It will be difficult to judge the accuracy of the computed optical flow when the displacement in small. For debugging purposes, the script draws the flow directly on the first frame, increasing its magnitude (by a factor scale) so that you can confirm that the direction of optical flow is (at least qualitatively) correct.

(5 points)
There are a total of 8 frames in the test sequence. By uncommenting the last portion of the skeleton program, you can run the Optical_Flow function iteratively, using the (updated) position of your given (x,y) point at frame k as the initial point for estimating optical flow to frame k+1, for k=7,8,9,10,11,12,13,14.

You may or may not be successful in tracking your given feature over all 8 frames, given the default settings. Try experimenting with different window sizes and choices of sigma for the Gaussian smoothing that work best for your given feature. Here, “work best” means that the original feature remains within the window used to compute optical flow and continues to be well located at the window's centre row and column.

Report the last frame at which tracking was successful and document the sequence of (x, y) positions of your feature in each frame successfully tracked. Include a side-by-side image of the initial frame and the final frame (successfully tracked) with a line drawn between the initial feature location and the final feature location. Be sure to report the window size and Gaussian sigma used to obtain your best result.

Of course, you're free to experiment with other feature locations and with other image sequences. But, you are only required to report results for your assigned feature point.

(5 points)
There are locations in an image where Lucas–Kanade optical flow will fail, regardless of choice of window size and sigma for Gaussian smoothing. Describe two such situations. Note: It is sufficient to describe situations. It is not necessary to demonstrate them.
