import cv2
import numpy as np
import math
# Variables

cone_width_reference = 90 #  90 pixel width at 6 ft
height = 0
x_pos = 0
distance_from_cone = 0

# reading image
vid = cv2.VideoCapture(0)
#(hMin = 19 , sMin = 108, vMin = 71), (hMax = 30 , sMax = 255, vMax = 255)


while True:
    _, frame = vid.read()
    ORIGv = frame.copy()
    original = frame.copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([22, 108, 71], dtype="uint8") # 5, 10, 130
    upper = np.array([30, 255, 255], dtype="uint8") # 80, 240, 245
    mask = cv2.inRange(frame, lower, upper)     


    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]


    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if (w > 92.5):
            cv2.rectangle(original, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.circle(original, (x+ int(w/2),y + int(h/2)), 20,  (36, 255, 12), 10)
            height = h
            x_pos = x


    if (height != 0):
        distance = (353. / height) * 2
    else:
        distance = 0
    print(f"distance is {distance}", f" and Pixel height is {height}")
    print(f"Horizontal distance (px): {x_pos-360}")

    cv2.imshow("in_range", original)
    cv2.imshow("Video", mask)
    cv2.waitKey(1)

