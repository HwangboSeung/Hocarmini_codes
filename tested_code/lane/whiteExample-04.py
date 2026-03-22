import cv2
import numpy as np

def region_of_interest(img, vertices, color3=(255, 255, 255), color1=255):
    mask = np.zeros_like(img)

    if len(img.shape) > 2:
        color = color3
    else:
        color = color1

    cv2.fillPoly(mask, vertices, color)
    ROI_image = cv2.bitwise_and(img, mask)
    return ROI_image

def mark_img(roi_img, image, blue_threshold=200, green_threshold=200, red_threshold=200):
    mark = np.copy(roi_img)
    bgr_threshold = [blue_threshold, green_threshold, red_threshold]

    thresholds = (image[:, :, 0] < bgr_threshold[0]) \
                 | (image[:, :, 1] < bgr_threshold[1]) \
                 | (image[:, :, 2] < bgr_threshold[2])
    mark[thresholds] = [0, 0, 0]
    return mark

image = cv2.imread('solidWhiteCurve.jpg') # '/home/pi/solidWhiteCurve.jpg'
height, width = image.shape[:2]

vertices = np.array(
    [[(10, height), (width / 2 - 60, height / 2 + 60), (width / 2 + 60, height / 2 + 60), (width - 10, height)]],
    dtype=np.int32)

roi_img = region_of_interest(image, vertices, (0, 0, 255))  # (255, 255, 255)

mark = mark_img(roi_img, image)

# color_thresholds = (mark[:, :, 0] > 200) & (mark[:, :, 1] > 200) & (mark[:, :, 2] > 200)  # white lane
color_thresholds = (mark[:, :, 0] == 0) & (mark[:, :, 1] == 0) & (mark[:, :, 2] > 200)
image[color_thresholds] = [0, 0, 255]

cv2.imshow('roi_white', mark)
cv2.imshow('result', image)
cv2.waitKey(0)