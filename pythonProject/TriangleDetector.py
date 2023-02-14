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

    lower_y = np.array([22, 108, 71], dtype="uint8") # 5, 10, 130
    upper_y = np.array([30, 255, 255], dtype="uint8") # 80, 240, 24z
    mask_y = cv2.inRange(frame, lower_y, upper_y)

    lower_p = np.array([117, 75, 75], dtype="uint8")  # 110, 141, 47
    upper_p = np.array([126, 255, 250], dtype="uint8")  # 130, 255, 255
    mask_p = cv2.inRange(frame, lower_p, upper_p)




    cnts_y = cv2.findContours(mask_y, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_y = cnts_y[0] if len(cnts_y) == 2 else cnts_y[1]
    cnts_p = cv2.findContours(mask_p, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_p = cnts_p[0] if len(cnts_p) == 2 else cnts_p[1]

    for c in cnts_y:
        x, y, w, h = cv2.boundingRect(c)
        if (w > 92.5):
            cv2.rectangle(original, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.circle(original, (x+ int(w/2),y + int(h/2)), 20,  (36, 255, 12), 10)
            height = h
            x_pos = x

    for c in cnts_p:
        x, y, w, h = cv2.boundingRect(c)
        if (w > 92.5):
            cv2.rectangle(original, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.circle(original, (x+ int(w/2),y + int(h/2)), 20,  (36, 255, 12), 10)


    if (height != 0):
        distance = (635 / height) * 2
    else:
        distance = 0
    print(f"distance is {distance}", f" and Pixel height is {height}")
    print(f"Horizontal distance (px): {x_pos-360}")

    cv2.imshow("in_range", original)
    cv2.imshow("Yellow Video", mask_y)
    cv2.imshow("Purple Video", mask_p)
    cv2.waitKey(1)

