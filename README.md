## Advanced Lane Lines Project Writeup

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./examples/undistort_output.png "Undistorted"
[image2]: ./test_images/test1.jpg "Road Transformed"
[image3]: ./examples/binary_combo_example.jpg "Binary Example"
[image4]: ./examples/warped_straight_lines.jpg "Warp Example"
[image5]: ./examples/color_fit_lines.jpg "Fit Visual"
[image6]: ./examples/example_output.jpg "Output"
[image_calibration]: ./examples/calibration2_composite.jpg "Calibration result"
[image_distortion]: ./examples/sample_distortion.png "Distortion removal"
[image_binarized]: ./examples/sample_binarized.png "Binarized"
[image_mask]: ./examples/sample_mask.jpg "Mask"
[image_lines]: ./examples/sample_lines.png "Mask"
[image_topview]: ./examples/sample_topview.png "Top view"
[image_interior]: ./examples/sample_interior.png "Interior view from top view"
[image_lane]: ./examples/sample_lane.png "Final result"
[video1]: ./output_videos/project_video.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  [Here](https://github.com/udacity/CarND-Advanced-Lane-Lines/blob/master/writeup_template.md) is a template writeup for this project you can use as a guide and a starting point.  

You're reading it!

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in the python file "camera_calibration.py".

I start by preparing "object points", which will be the (x, y,z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result: 

![alt text][image_calibration]

These camera calibration coefficients are saved to be used in all subsequent images to be processed.

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

Distortion correction is applied in cell 3 of the 'Lane_Detection.ipynb' jupyter notebook, using 'cv2.undistort()' with the coefficients saved in the previous step. This is the result applying it to an image:
![alt text][image_distortion]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

This step is implemented in cell 5 of the jupyter notebook. I used a combination of color and gradient thresholds to generate a binary image.

* Images were transformed to an HLS colorspace, and a threshold applied to the saturation channel to keep values from 130 to 255. 
* A Sobel operator with kernel size 3 was applied to the luminance channel in the x axis, with threshold (15,135).

Values for the thresholds were selected using images with manually colored lines such as this one:

![alt text][image_mask]

to calculate a score for each threshold combination, considering the number of actual lane pixels detected, and the number of "not lane" detected as well. Code for this process can be seen starting at line 53 in the 'color_and_gradient.py' python file. This process proved to be quite time consuming, and not necessarily very effective (as the final result is not much different than the initial ballpark estimate).

The final binarized image for one of the test images can be seen below:

![alt text][image_binarized]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform includes a function called `warp()`, which appears in cell 4 of the jupyter notebook.   The `warper()` function takes as inputs an image (`img`), as well as source (`src`) and destination (`dst`) points.  I chose the hardcode the source and destination points in the following manner:

```python
src=np.float32([(240,695),(595,450),(1070,695),(685,450)])
dest=np.float32([(300,720),(300,50),(1000,720),(1000,50)])

```

This resulted in the following source and destination points:

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 240, 695      | 300, 720        | 
| 595, 450      | 300, 50      |
| 1070, 695     | 1000, 720      |
| 685, 450      | 1000, 50        |

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

![alt text][image_lines]

Here is the transformation applied to one of the test images with a curve in view:
![alt text][image_topview]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

Using the undistorted binarized image with perspective correction applied, lane line pixels were initially identified using the sliding windows algorithm (cell 7 in the notebook), and a 2nd order polynomial was fit to those pixel positions. 
For subsequent frames, the previous fitted lines were used as a starting point, and pixels were identified in its immediate surroundings (cell 8 in the notebook). If the fit was not too good (measured just by the residuals), the sliding windows approach was used again. This process is implemented in function 'find_lane_lines' in cell 11.

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I did this in cell 12 from the jupyter notebook. Calculations were done assuming a lane width of 3.7 meters, and that 30 meters of the road are visible in the top view image. Curve radius was estimated at the bottom of the image (in the car position), calculating the curvature of both lanes, and taking the mean value. The position of the car was estimated comparing the center of the lane to the center of the image (which is assumed to correspon to the center of the car).

Considering the road curvature radius wont change rapidly, exponential smoothing was used to avoid changes from frame to frame.

Additionally, the resulting values were interpreted in function 'curvature_and_position_text' in cell 13:

* Curvature values over 10Km were shown as '>10Km', as exact values when not in a curve are not really representative. 
* Position values from 10cm left to 10cm right of the center of the lane are reported as 'Around lane center', to avoid quickly changing from left to right of the lane.

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

Function 'draw_lane' in cell 9 of the notebook takes the image and the fitted lane lines and paints the lane area in green. It also writes a text to the top of the image, in this case, the curvature and position of the vehicule. Here is an example of my result on a test image:

![alt text][image_lane]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./output_videos/project_video.mp4)

