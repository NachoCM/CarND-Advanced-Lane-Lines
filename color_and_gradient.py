import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob




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

    # Threshold color channel
    s_binary = np.zeros_like(s_channel)
    s_binary[(s_channel >= s_thresh[0]) & (s_channel <= s_thresh[1])] = 1
    # Stack each channel
    # Note color_binary[:, :, 0] is all 0s, effectively an all black image. It might
    # be beneficial to replace this channel with something else.
    color_binary = np.dstack((np.zeros_like(sxbinary), sxbinary, s_binary)) * 255
    combined_binary = np.zeros_like(sxbinary)
    combined_binary[(s_binary == 1) | (sxbinary == 1)] = 1
    return np.uint8(color_binary), combined_binary



image = mpimg.imread('thresholding/test4_undistorted.jpg')
mask = mpimg.imread('thresholding/test4_undistorted_mask.jpg')
mask=cv2.cvtColor(mask,cv2.COLOR_RGB2GRAY)

def target(pars):
    result, combined = binarize(image, s_thresh=(pars[0], pars[1]),
                                sx_thresh=(pars[2], pars[3]))
    pct_detected = np.sum(combined[mask > 0] == 1) / np.sum(mask > 0)
    pct_blank_ok = np.sum(combined[mask == 0] == 0) / np.sum(mask == 0)
    score = pct_detected * pct_blank_ok
    return score
#result, combined = binarize(image, s_thresh=(140, 240), sx_thresh=(20, 100))  # Plot the result
#pct_detected=np.sum(result[mask>0]==255)/np.sum(mask>0)
#print(pct_detected)

max_score=0
s_thresh=(0,0)
sx_thresh=(0,0)
for s_thresh_low in range(125,135,1):
    for s_thresh_width in range(125,255-s_thresh_low+1,1):
        for sx_thresh_low in range(10,20,1):
            for sx_thresh_width in range(115,125,1):
                result, combined = binarize(image, s_thresh=(s_thresh_low,s_thresh_low+s_thresh_width),
                                            sx_thresh=(sx_thresh_low,sx_thresh_low+sx_thresh_width) ) # Plot the result
                pct_detected = np.sum(combined[mask > 0] == 1) / np.sum(mask > 0)
                pct_blank_ok = np.sum(combined[mask == 0] == 0) / np.sum(mask == 0)
                score=pct_detected*pct_blank_ok
                if score>max_score:
                    max_score=score
                    s_thresh=(s_thresh_low, s_thresh_low + s_thresh_width)
                    sx_thresh = (sx_thresh_low, sx_thresh_low + sx_thresh_width)
                    print('Max detected:', max_score)
                    print('s_thresh=', s_thresh)
                    print('sx_thresh=', sx_thresh)
        print('Finished with s_thresh_witdth=',s_thresh_width)
    print('Finished with s_thresh_low=',s_thresh_low)

print('Max detected:',max_score)
print('s_thresh=',s_thresh)
print('sx_thresh=',sx_thresh)


#
# for idx, fname in enumerate(images):
#     image = mpimg.imread(fname)
#     result, combined = binarize(image, s_thresh=(140, 240), sx_thresh=(20, 100))
#
#     # Plot the result
#     f, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 9))
#     f.tight_layout()
#
#     ax1.imshow(image)
#     ax1.set_title('Original Image', fontsize=40)
#
#     ax2.imshow(np.uint8(result))
#     ax2.set_title('Pipeline Result', fontsize=40)
#     plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
#     out_name = 'output_' + fname[5:-4] + '_binarized.jpg'
#     plt.savefig(out_name)