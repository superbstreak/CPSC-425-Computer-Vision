from PIL import Image, ImageDraw
import numpy as np
import csv
import math

def ReadKeys(image):
    """Input an image and its associated SIFT keypoints.

    The argument image is the image file name (without an extension).
    The image is read from the PGM format file image.pgm and the
    keypoints are read from the file image.key.

    ReadKeys returns the following 3 arguments:

    image: the image (in PIL 'RGB' format)

    keypoints: K-by-4 array, in which each row has the 4 values specifying
    a keypoint (row, column, scale, orientation).  The orientation
    is in the range [-PI, PI] radians.

    descriptors: a K-by-128 array, where each row gives a descriptor
    for one of the K keypoints.  The descriptor is a 1D array of 128
    values with unit length.
    """
    im = Image.open(image+'.pgm').convert('RGB')
    keypoints = []
    descriptors = []
    first = True
    with open(image+'.key','rb') as f:
        reader = csv.reader(f, delimiter=' ', quoting=csv.QUOTE_NONNUMERIC,skipinitialspace = True)
        descriptor = []
        for row in reader:
            if len(row) == 2:
                assert first, "Invalid keypoint file header."
                assert row[1] == 128, "Invalid keypoint descriptor length in header (should be 128)."
                count = row[0]
                first = False
            if len(row) == 4:
                keypoints.append(np.array(row))
            if len(row) == 20:
                descriptor += row
            if len(row) == 8:
                descriptor += row
                assert len(descriptor) == 128, "Keypoint descriptor length invalid (should be 128)."
                #normalize the key to unit length
                descriptor = np.array(descriptor)
                descriptor = descriptor / math.sqrt(np.sum(np.power(descriptor,2)))
                descriptors.append(descriptor)
                descriptor = []
    assert len(keypoints) == count, "Incorrect total number of keypoints read."
    print "Number of keypoints read:", int(count)
    return [im,keypoints,descriptors]

def AppendImages(im1, im2):
    """Create a new image that appends two images side-by-side.

    The arguments, im1 and im2, are PIL images of type RGB
    """
    im1cols, im1rows = im1.size
    im2cols, im2rows = im2.size
    im3 = Image.new('RGB', (im1cols+im2cols, max(im1rows,im2rows)))
    im3.paste(im1,(0,0))
    im3.paste(im2,(im1cols,0))
    return im3

def DisplayMatches(im1, im2, matched_pairs):
    """Display matches on a new image with the two input images placed side by side.

    Arguments:
     im1           1st image (in PIL 'RGB' format)
     im2           2nd image (in PIL 'RGB' format)
     matched_pairs list of matching keypoints, im1 to im2

    Displays and returns a newly created image (in PIL 'RGB' format)
    """
    im3 = AppendImages(im1,im2)
    offset = im1.size[0]
    draw = ImageDraw.Draw(im3)
    for match in matched_pairs:
        draw.line((match[0][1], match[0][0], offset+match[1][1], match[1][0]),fill="red",width=2)
    im3.show()
    return im3

def match(image1,image2):
    """Input two images and their associated SIFT keypoints.
    Display lines connecting the first 5 keypoints from each image.
    Note: These 5 are not correct matches, just randomly chosen points.

    The arguments image1 and image2 are file names without file extensions.

    Returns the number of matches displayed.

    Example: match('scene','book')
    """
    im1, keypoints1, descriptors1 = ReadKeys(image1)
    im2, keypoints2, descriptors2 = ReadKeys(image2)
    #
    # REPLACE THIS CODE WITH YOUR SOLUTION (ASSIGNMENT 5, QUESTION 3)
    #
    #Generate five random matches (for testing purposes)

    # initialize values
    print 'Debug - Setp 1: Initilizing values'
    matched_pairs = []
    descriptor_lengthOne = len(descriptors1)
    descriptor_lengthTwo = len(descriptors2)
    threshold = 0.7

    # loop through each item in descriptors1
    print 'Debug - Setp 2: Loop through descriptors'
    for x in range(descriptor_lengthOne):
        
        # initlaize dot product array
        dotproduct_arr = []

        # loop through each item in descriptors2
        # print 'Debug - Setp 3: Calculating dot products'
        for y in range (descriptor_lengthTwo):

            # compute the dot product and insert into the array
            dotproduct = np.dot(descriptors1[x], descriptors2[y])
            dotproduct_arr.append(dotproduct)

        # initilize arrays for angles
        angle_arr = []

        # loop through the array of dot products we just calculated
        # print 'Debug - Setp 4: Calculating angles'
        for dotpos in range (len(dotproduct_arr)):

            # compute the angle theta (cos theta = a dot b over mag(a)mag(b))
            angle_arr.append(math.acos(dotproduct_arr[dotpos]))

        # sort the angle array we calcauted above and grab the two smallest val
        # print 'Debug - Setp 5: Sorting angle array'
        sorted_angle_arr = sorted(angle_arr)
        best_angle = sorted_angle_arr[0]
        runnerup_angle = sorted_angle_arr[1]

        # compute the ratio and initalize index
        angle_ratio = best_angle/runnerup_angle
        index = 0

        # if the ratio is less than the threshold, we proceed
        # print 'Debug - Setp 6: Checking threshold'
        if (angle_ratio <= threshold):
            
            # calculate the index and insert pair into match_pairs and print out
            index  = angle_arr.index(best_angle)
            matched_pairs.append([keypoints1[x], keypoints2[index]])

    print 'Debug - Setp 7: End of MP'
            
    # initalize values that is used in RANSAC
    delta_orientation_between_keypoints = 20 # plus or minus (+/-)
    delta_of_scale = 0.8
    matched_pairs_len = len(matched_pairs)
    ransac_all = []

    # do it 10 times
    for i in range(10):
        ransac_current = []
        mp_pos = np.random.randint(matched_pairs_len)
        random_matchpairs = matched_pairs[mp_pos]

        print 'Debug - Setp 8: Cal delata s/o'
        # calculate change in scale and orientation
        scale_change = abs(random_matchpairs[0][2] - random_matchpairs[1][2])
        orientation_change = random_matchpairs[0][3] - random_matchpairs[1][3]

        # loop through all the matched pairs and check for consistancy
        print 'Debug - Setp 9: looping mp for consistancy check'
        for m in range(matched_pairs_len):
            mp = matched_pairs[m]
            orientation_change_compare = mp[0][3] - mp[1][3]
            diff_in_angle = abs(math.degrees(orientation_change) + 360 - math.degrees(orientation_change_compare) + 360) % 180

            # if the change in angle fits our specfication and check for consistancy
            # print 'Debug - Setp 10: angle check'
            if (diff_in_angle <= delta_orientation_between_keypoints):

                # then we compare scale change and consistancy
                # print 'Debug - Setp 11: cal scale'
                scale_change_compare = abs(mp[0][2] - mp[1][2])
                scale_change_upper = max(scale_change, scale_change_compare)
                scale_change_lower = min(scale_change, scale_change_compare)
                scale_with_deltaval = scale_change_upper * delta_of_scale

                # if it is consistant enough, we add it to the current array
                # print 'Debug - Setp 12: scale check'
                if (scale_with_deltaval <= scale_change_lower):
                    ransac_current.append(mp)

                # consistancy check failed (scale), skip this item
                else:
                    continue;
            # consistancy check failed (angle), skip item
            else:
                continue;
        # compare the length of array and only keep the largest
        print 'Debug - Setp 13: length check'
        if (len(ransac_current) > len(ransac_all)):
            ransac_all = ransac_current;
    #
    # END OF SECTION OF CODE TO REPLACE
    #
    im3 = DisplayMatches(im1, im2, ransac_all)
    return im3

#Test run...
match('library','library2')

