import cv2

image = cv2.imread('solidWhiteCurve.jpg') # '/home/pi/solidWhiteCurve.jpg'
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
