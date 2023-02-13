import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
# Variables

cone_width_reference = 90 #  90 pixel width at 6 ft
x = 0
y = 0
w = 0
h = 0

distance = 0

# reading image
vid = cv2.VideoCapture(0)



while True:
    _, frame = vid.read()
    ORIGv = frame.copy()
    original = frame.copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([5, 104, 182], dtype="uint8") # 20, 70, 130
    upper = np.array([90, 255, 255], dtype="uint8") # 80, 240, 245
    mask = cv2.inRange(frame, lower, upper)     


    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]


    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(original, (x, y), (x + w, y + h), (36, 255, 12), 2)

    if (w != 0):
        distance = 92.5 / w  * 6
    else:
        distance = 0
    print(f"distance is {distance}", f"/nand Pixel width is {w}")

    cv2.imshow("in_range", original)
    cv2.imshow("Video", mask)
    cv2.waitKey(1)

