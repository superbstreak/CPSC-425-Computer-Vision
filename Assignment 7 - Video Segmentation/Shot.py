from PIL import Image, ImageDraw
import numpy as np
from scipy.cluster.vq import vq, kmeans, whiten
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt

# Computes the cost of given boundaries. Good boundaries have zero cost.
def get_boundaries_cost( boundaries, good_boundaries ):
    return np.sum( boundaries != good_boundaries );

# Finds the indices of color_histograms given a series of cluster centres.
def cluster2boundaries(histograms, centres):

    # Find the cluster assignment of each histogram
    distances = cdist( histograms, centres )
    idx       = np.argmin( distances, 1 )

    # Find the points where the index changes
    boundaries = np.zeros( len(idx)+1, dtype = np.bool )

    for i in range( len(idx)-1 ):
        boundaries[i+1] = idx[i] != idx[i+1];

    return boundaries

# Computes histograms from gray images
def compute_gray_histograms( grays, nbins ):
    gray_hs = np.zeros(( nframes, nbins ), dtype = np.uint16 );

    for i in range( len(grays) ):
        gray_im = grays[i]
        v1 = np.histogram(gray_im.flatten(),bins=nbins, range=(0,255))
        gray_hs[i] = v1[0]

    return gray_hs;


def compute_color_histograms( colors, nbins ):
    # === WRITE THE FUNCTION HERE ===
    
    # Initialize for Red, Green and Blue histogram
    r_hs = np.zeros(( nframes, nbins ), dtype = np.uint16 );
    g_hs = np.zeros(( nframes, nbins ), dtype = np.uint16 );
    b_hs = np.zeros(( nframes, nbins ), dtype = np.uint16 );

    # plt.imshow(colors[0,:,:,0]) slice preview
    
    for i in range (len(colors)):
        # Slice it by different color channel
        r_color_im = colors[i,:,:,0]    # slice by red
        g_color_im = colors[i,:,:,1]    # slice by green
        b_color_im = colors[i,:,:,2]    # slice by blue

        # Calculate historgram on the flatten sliced image
        rv = np.histogram(r_color_im.flatten(), bins=nbins, range=(0, 255))
        gv = np.histogram(g_color_im.flatten(), bins=nbins, range=(0, 255))
        bv = np.histogram(b_color_im.flatten(), bins=nbins, range=(0, 255))

        # Store value 
        r_hs[i] = rv[0]
        g_hs[i] = gv[0]
        b_hs[i] = bv[0]

    # Concat them into one
    c_hs = np.hstack((r_hs, g_hs, b_hs))
    return c_hs;


# === Main code starts here ===
fname     = 'colours' # folder name 
nframes   = 151       # number of frames
im_height = 90        # image height 
im_width  = 120       # image width

# define the list of (manually determined) shot boundaries here
good_boundaries = [33, 92, 143];

# convert good_boundaries list to a binary array
gb_bool = np.zeros( nframes+1, dtype = np.bool )
gb_bool[ good_boundaries ] = True

# Create some space to load the images into memory
colors = np.zeros(( nframes, im_height, im_width, 3), dtype = np.uint8);
grays  = np.zeros(( nframes, im_height, im_width   ), dtype = np.uint8);

# Read the images and store them in color and grayscale formats
for i in range( nframes ):
    imname    = '%s/dwc%03d.png' % ( fname, i+1 )
    im        = Image.open( imname ).convert( 'RGB' )
    colors[i] = np.asarray(im, dtype = np.uint8)
    grays[i]  = np.asarray(im.convert( 'L' ))

# Initialize color histogram
nclusters   = 4;
nbins       = range(2,13)
gray_costs  = np.zeros( len(nbins) );
color_costs = np.zeros( len(nbins) );

# === GRAY HISTOGRAMS ===
for n in nbins:
    # Calculate histogram for the gray
    grayhist = compute_gray_histograms(grays, n)
    # compute kmeans
    centeroid = kmeans(grayhist, nclusters)
    # calcualte the boundaries
    bound = cluster2boundaries (grayhist, centeroid[0])
    # test the cost
    boundres = get_boundaries_cost(bound, gb_bool)
    # store cost value
    gray_costs[n-2] = boundres
    pass
# === END GRAY HISTOGRAM CODE ===

plt.figure(1);
plt.xlabel('Number of bins')
plt.ylabel('Error in boundary detection')
plt.title('Boundary detection using gray histograms')
plt.plot(nbins, gray_costs)
plt.axis([2, 13, -1, 10])
plt.grid(True)
plt.show()

# === COLOR HISTOGRAMS ===
for n in nbins:
    # calculate historgram for color
    colorhist = compute_color_histograms(colors, n)
    # compute kmeans
    centeroid = kmeans(colorhist, nclusters)
    # calculate the boundaries
    cbound = cluster2boundaries(colorhist, centeroid[0])
    # test teh cost
    cboundres =  get_boundaries_cost(cbound, gb_bool)
    # store the cost value
    color_costs[n-2] = cboundres
    pass
# === END COLOR HISTOGRAM CODE ===

plt.figure(2);
plt.xlabel('Number of bins')
plt.ylabel('Error in boundary detection')
plt.title('Boundary detection using color histograms')
plt.plot(nbins, color_costs)
plt.axis([2, 13, -1, 10])
plt.grid(True)
plt.show()

fdiffs = np.zeros( nframes )
# === ABSOLUTE FRAME DIFFERENCES ===
# (1 - 0), (2 - 1), (3 - 2), (4 - 3), (5 - 4)
tempval = 0
for n in range(nframes):
    # Skip the first since it doesnt have any to compare to 
    if n > 0:
        tempval = grays[n-1]    # get the previous
        current = grays[n]      # get the current
        diff = np.sum(abs(current - tempval))   # calculate the diff
        fdiffs[n] = diff        # store the diff
    pass

plt.figure(4)
plt.xlabel('Frame number')
plt.ylabel('Absolute frame difference')
plt.title('Absolute frame differences')
plt.plot(fdiffs)
plt.show()

sqdiffs = np.zeros( nframes )
# === SQUARED FRAME DIFFERENCES ===
tempval = 0
for n in range(nframes):
    # Skip the first since it doesnt have any to compare to
    if n > 0:
        tempval = grays[n-1]    # previous
        current = grays[n]      # current
        diff = np.sum(pow((current - tempval), 2))  # square
        sqdiffs[n] = diff       # store the diff
    pass

plt.figure(5)
plt.xlabel('Frame number')
plt.ylabel('Squared frame difference')
plt.title('Squared frame differences')
plt.plot(sqdiffs)
plt.show()

avgdiffs = np.zeros( nframes )
# === AVERAGE GRAY DIFFERENCES ===
for n in range(nframes):
    # Skip the first since it doesnt have any to compare to
    if n > 0:
        tempval = grays[n-1]    # previous
        current = grays[n]      # current
        diff = np.average(current) - np.average(tempval)    # diff in avg
        avgdiffs[n] = diff      # store the diff
    pass

plt.figure(6)
plt.xlabel('Frame number')
plt.ylabel('Average gray frame difference')
plt.title('Average gray frame differences')
plt.plot(avgdiffs)
plt.show()

histdiffs = np.zeros( nframes )
# === HISTOGRAM DIFFERENCES ===
for n in range(nframes):
    # Skip the first since it doesnt have any to compare to
    if n > 0:
        tempval = grays[n-1]    # previous
        current = grays[n]      # current
        prev_hs = compute_gray_histograms(tempval, 10)  # gray hist of previous with 10
        curr_hs = compute_gray_histograms(current, 10)  # gray hist of current with 10
        dist = np.linalg.norm(curr_hs - prev_hs) # calculate distance
        histdiffs[n] = dist # store the value
    pass

plt.figure(7)
plt.xlabel('Frame number')
plt.ylabel('Histogram frame difference')
plt.title('Histogram frame differences')
plt.plot(histdiffs)
plt.show()
