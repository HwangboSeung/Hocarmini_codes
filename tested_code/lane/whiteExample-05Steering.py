import cv2
import numpy as np

pre_leftx = 200
pre_rightx = 960
threshold = 100
offset_x = 10

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

def img_process(img, color_thresholds):
    global pre_leftx, pre_rightx, threshold, offset_x
    height, width = image.shape[:2]

    x_margin, x_width, y_min, y_max = int(0.2 * width), int(0.25 * width), int(0.75 * height), int(0.8 * height)
    y_middle = int((y_min + y_max) / 2)

    cv2.rectangle(img, (x_margin, y_min), (x_margin + x_width, y_max), (150, 150, 100), 2)  # draw rectangle
    cv2.rectangle(img, (width - x_width - x_margin, y_min), (width - x_margin, y_max), (150, 150, 100), 2)

    l_y, l_x = color_thresholds[y_min: y_max, x_margin: x_margin + x_width].nonzero()
    r_y, r_x = color_thresholds[y_min: y_max, width - x_margin - x_width: width - x_margin].nonzero()
    print(len(l_x), len(r_x))

    leftx = np.average(l_x) + x_margin if len(l_x) > threshold else pre_leftx
    rightx = np.average(r_x) + (width - x_margin - x_width) if len(r_x) > threshold else pre_rightx
    midx = int((leftx + rightx) / 2)
    pre_leftx, pre_rightx = leftx, rightx

    cv2.circle(img, (int(leftx), y_middle), 10, 0, -1)
    cv2.circle(img, (int(rightx), y_middle), 10, 0, -1)
    cv2.circle(img, (int(midx), y_middle), 10, (255, 0, 0), -1)

    steer = np.arctan2(midx - (width/2) - offset_x, height - y_middle)
    steer = round(steer, 2)
    cv2.line(img, (width//2 + offset_x, height), (midx, y_middle), (255, 0, 0), 3)  # draw line
    cv2.putText(img, str(steer), (width_center - 150, height - 40), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2)

    return img, steer

cap = cv2.VideoCapture('solidWhiteRight.mp4') # '/home/pi/codes/solidWhiteRight.mp4'

while (cap.isOpened()):
    ret, image = cap.read()
    if not ret:
        break 
    height, width = image.shape[:2]
    width_center = width // 2
    height_center = height // 2

    vertices = np.array(
        [[(10, height), (width_center - 60, height_center + 60), (width_center + 60, height_center + 60),
          (width - 10, height)]],
        dtype=np.int32)

    roi_img = region_of_interest(image, vertices, (0, 0, 255))
    mark = mark_img(roi_img, image)

    color_thresholds = (mark[:, :, 0] == 0) & (mark[:, :, 1] == 0) & (mark[:, :, 2] > 200)
    image[color_thresholds] = [0, 0, 255]

    img, steer = img_process(image, color_thresholds)
    print(steer)

    cv2.imshow('results', image)
    if cv2.waitKey(1) != -1 :
        break

cap.release()
cv2.destroyAllWindows()
