import cv2
import numpy as np

image = cv2.imread('solidWhiteCurve.jpg') # '/home/pi/solidWhiteCurve.jpg'
mark = np.copy(image)

#  BGR settings
blue_threshold = 200
green_threshold = 200
red_threshold = 200
bgr_threshold = [blue_threshold, green_threshold, red_threshold]


thresholds = (image[:,:,0] < bgr_threshold[0]) \
            | (image[:,:,1] < bgr_threshold[1]) \
            | (image[:,:,2] < bgr_threshold[2])
mark[thresholds] = [0,0,0]

cv2.imshow('Image', image)
cv2.imshow('Threshold result', mark)
cv2.waitKey(0)
cv2.destroyAllWindows()
