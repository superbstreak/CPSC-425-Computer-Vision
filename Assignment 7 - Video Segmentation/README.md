# CPSC-425-Computer-Vision
The purpose of this assignment is to understand and implement methods for shot boundary detection in a video sequence.

The assignment

In this assignment we'll detect shot boundaries in 151 frames from a well known cartoon (google “Snow White and the Seven Dwarfs Heigh Ho Song”). The images are from that video. Here are the seven dwarfs.

Shot boundaries mark transitions between “shots.” A shot is a sequence of frames where the camera sees more or less the same scene. In this case, shot boundaries mark the transition from one dwarf to another.

We can identify shot boundaries in two different ways:

identify groups of images that are similar to each other (clustering), label them as belonging to a group, and then see where in the sequence the group label changes, or
detect abrupt changes in image content by measuring inter-frame change (frame differences).
We experiment with 6 methods: the first two use clustering and the last four use frame differences.
You are given skeleton code for the assignment, Shot.py

The data

You are given 151 frames in a directory of .jpg files, each of size 90 by 120. You can get the images from colours.zip. Download this file to your directory and unzip it with the command

unzip colours.zip
This will create a sub-directory, colours, containing the 151 video frames.
Manually find the shot boundaries. Record the last frame number of each shot (i.e., if the shot changes from frame 3 to 4, you should record 3 as a shot boundary). Note that the first and last frames in the entire sequence do not count as shot boundaries.

(1 mark) Write the frame numbers of the shot boundaries as a list in the variable good_boundaries in the skeleton code, Shot.py.
Detecting boundaries using k-means

First, we will try k-means as a method to detect the shot boundaries. kmeans is a SciPy function that implements the k-means clustering algorithm -- look at its documentation to see how it works.

We are going to construct features for each frame using histograms of pixel values. The code to read the images and to create gray histograms is provided (see the function compute_gray_histograms).

Once we have the histograms for each frame, the task is to cluster them using k-means. We know, a priori, that there are 4 shots. Therefore, we use k=4 clusters. Once we have the cluster centers, we assign each frame's histogram to its associated cluster. Finally, we find frames where the cluster assignment changes, using the function cluster2boundaries provided. As a test, use the function get_boundaries_cost to evaluate how good this prediction is.

(4 marks) Write the loop inside the code section starting with # === GRAY HISTOGRAMS ===, to compute histograms, to cluster them using k-means, to obtain shot boundaries and to evaluate the detected boundaries (storing the associated cost in the array gray_costs). This will produce a plot showing “Error in boundary detection” (vertical axis) versus the “Number of bins” used (horizontal axis).
(2 marks) Write the body of the function compute_color_histograms. The function is analogous to compute_gray_histograms, but should compute one histogram for each color channel, and then concatenate the three histograms into one larger histogram. Hint: You can “concatenate” numpy arrays using the function np.vstack, as was suggested in Assignment 6.
(4 marks) Write the loop inside the code section starting with # === COLOR HISTOGRAMS ===, analogous to the gray histogram loop above, but using the color histograms. This will produce a plot showing “Error in boundary detection” (vertical axis) versus the “Number of bins” used (horizontal axis).
Detecting boundaries using frame differences

Another way to detect shot boundaries is to detect changes between successive frames. For this part of the assignment, use only the gray value images.

Add code to your Shot.py file to implement the following measures of change between successive frames:

(2 marks) Absolute frame difference: Compute the sum of the absolute pointwise differences between successive frames.
(2 marks) Squared frame difference: Compute the sum of the squared pointwise differences between successive frames.
(2 marks) Average gray level difference: Compute the average gray level for each frame and compute the difference between the averages in successive frames.
(2 marks) Histogram difference: Compute the gray level histogram for each frame and compute the Euclidean distance between the histograms in successive frames. For the histograms, use 10 bins.
In each part, 5–8, produce the indicated titled/labeled plots of the difference measure (vertical axis) versus the frame number (horizontal axis).
Answer the following written questions:

(2 marks) Which frame difference method is better? Why?
(2 marks) We could use other features such as edges, corners, or other image descriptors to identify shot boundaries (by clustering, by looking at differences, or by some other means). Which would likely be most effective?
(2 marks) We worked with shots without camera movement. Which of our six methods do you think would work best if the camera were slowly moving instead of static?
