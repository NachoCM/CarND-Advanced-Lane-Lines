import pickle
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob

# Read in the saved camera matrix and distortion coefficients
# Calculated in camera_calibration.py
dist_pickle = pickle.load(open("camera_cal/camera_dist_pickle.p", "rb"))
mtx = dist_pickle["mtx"]
dist = dist_pickle["dist"]

def undistort(img):
    return cv2.undistort(img, mtx, dist, None, mtx)

#src=np.float32([(240,695),(635,425),(1070,695),(645,425)])
src=np.float32([(240,695),(595,450),(1070,695),(685,450)])
#src=np.float32([(260,680),(595,450),(1050,680),(685,450)])
dest=np.float32([(400,720),(400,50),(800,720),(800,50)])

def top_view(img):
    #undistorted = cv2.undistort(img, mtx, dist, None, mtx)
    M = cv2.getPerspectiveTransform(src, dest)
    warped = cv2.warpPerspective(img, M, img.shape[1::-1], flags=cv2.INTER_LINEAR)
    return warped

# img = cv2.imread('test_images/straight_lines1.jpg')
# undistorted=cv2.undistort(img,mtx,dist,None,mtx)
# cv2.imwrite('test_images/straight_lines1_undistorted.jpg',undistorted)
# cv2.imwrite('test_images/straight_lines1_warped.jpg',warped)
#
#file_name='test_images/straight_lines2'

#cv2.imwrite(file_name+'_warped.jpg',top_view(cv2.imread(file_name+'.jpg')))

def binarize(img, s_thresh=(130, 255), sx_thresh=(15, 135)):
    img = np.copy(img)
    # Convert to HLS color space and separate the V channel
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS).astype(np.float)
    l_channel = hls[:, :, 1]
    s_channel = hls[:, :, 2]
    # Sobel x
    sobelx = cv2.Sobel(l_channel, cv2.CV_64F, 1, 0)  # Take the derivative in x
    abs_sobelx = np.absolute(sobelx)  # Absolute x derivative to accentuate lines away from horizontal
    scaled_sobel = np.uint8(255 * abs_sobelx / np.max(abs_sobelx))

    # Threshold x gradient
    sxbinary = np.zeros_like(scaled_sobel)
    sxbinary[(scaled_sobel >= sx_thresh[0]) & (scaled_sobel <= sx_thresh[1])] = 1

    # Threshold saturation channel
    s_binary = np.zeros_like(s_channel)
    s_binary[(s_channel >= s_thresh[0]) & (s_channel <= s_thresh[1])] = 1

    combined_binary = np.zeros_like(sxbinary)
    combined_binary[(s_binary == 1) | (sxbinary == 1)] = 1
    return combined_binary

def pipeline(img):
    undistorted = undistort(img)
    binarized = binarize(undistorted)
    return top_view(binarized)





