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
#src=np.float32([(240,695),(635,425),(1070,695),(645,425)])
src=np.float32([(240,695),(595,450),(1070,695),(685,450)])
#src=np.float32([(260,680),(595,450),(1050,680),(685,450)])
dest=np.float32([(400,720),(400,50),(800,720),(800,50)])

130,255
15,135

def top_view(img):
    undistorted = cv2.undistort(img, mtx, dist, None, mtx)
    M = cv2.getPerspectiveTransform(src, dest)
    warped = cv2.warpPerspective(undistorted, M, img.shape[1::-1], flags=cv2.INTER_LINEAR)
    return warped

# img = cv2.imread('test_images/straight_lines1.jpg')
# undistorted=cv2.undistort(img,mtx,dist,None,mtx)
# cv2.imwrite('test_images/straight_lines1_undistorted.jpg',undistorted)
# cv2.imwrite('test_images/straight_lines1_warped.jpg',warped)
#
#file_name='test_images/straight_lines2'

#cv2.imwrite(file_name+'_warped.jpg',top_view(cv2.imread(file_name+'.jpg')))

images = glob.glob('test_images/*.jpg')

for idx, fname in enumerate(images):
    img = cv2.imread(fname)
    tv = top_view(img)
    undistorted = cv2.undistort(img, mtx, dist, None, mtx)
    out_name='output_'+fname[5:-4]+'_undistorted.jpg'
    cv2.imwrite(out_name, undistorted)

