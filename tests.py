import cv2
img = cv2.imread('test_images/straight_lines1_undistorted.jpg')
cv2.line(img,(240,695),(635,425),(255,0,0),2)
cv2.line(img,(1070,695),(645,425),(255,0,0),2)
cv2.imshow('img',img)
cv2.imwrite('test_images/straight_lines1_undistorted_hand_lines.jpg',img)
cv2.waitKey(3500)