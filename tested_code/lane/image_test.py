import cv2

img = cv2.imread("/home/pi/codes/lenna.png") 

cv2.imshow("Test", img)

img_canny = cv2.Canny(img, 50, 150)
cv2.imshow("Test img Edge", img_canny)

cv2.waitKey(0)
cv2.destroyAllWindows()
