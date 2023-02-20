import cv2
import numpy as np
import math

# Variables
cone_width_reference = 90 #  90 pixel width at 6 ft
height = 0
width = 0
x_pos = 0
distance_from_robot = 10
current_obj = None
distance = 0
x=0

# reading image
vid = cv2.VideoCapture(0)
#(hMin = 19 , sMin = 108, vMin = 71), (hMax = 30 , sMax = 255, vMax = 255)


def convex_hull_pointing_up(ch):

    points_above_center, points_below_center = [], []

    x, y, w, h = cv2.boundingRect(ch)
    aspect_ratio = w / h

    if aspect_ratio < 0.8:
        vertical_center = y + h / 2

        for point in ch:
            if point[0][
                1] < vertical_center:
                points_above_center.append(point)
            elif point[0][1] >= vertical_center:
                points_below_center.append(point)

        left_x = points_below_center[0][0][0]
        right_x = points_below_center[0][0][0]

        for point in points_below_center:
            if point[0][0] < left_x:
                left_x = point[0][0]
            if point[0][0] > right_x:
                right_x = point[0][0]

        for point in points_above_center:
            if (point[0][0] < left_x) or (point[0][0] > right_x):
                return False
    else:
        return False

    return True


while True:
    distance_from_robot = 69420
    _, frame = vid.read()

    ORIGv = frame.copy()
    original = frame.copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_y = np.array([22, 151, 71], dtype="uint8") # 5, 10, 130
    upper_y = np.array([28, 255, 255], dtype="uint8") # 30, 240, 24z
    mask_y = cv2.inRange(frame, lower_y, upper_y)

    lower_p = np.array([117, 75, 75], dtype="uint8")  # 110, 141, 47
    upper_p = np.array([126, 255, 250], dtype="uint8")  # 130, 255, 255
    mask_p = cv2.inRange(frame, lower_p, upper_p)

    lower_g = np.array([0, 0, 255], dtype="uint8")  # 110, 141, 47
    upper_g = np.array([0, 255, 255], dtype="uint8")  # 130, 255, 255
    mask_g = cv2.inRange(frame, lower_g, upper_g)

    cnts_y = cv2.findContours(mask_y, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_y = cnts_y[0] if len(cnts_y) == 2 else cnts_y[1]

    cnts_p = cv2.findContours(mask_p, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_p = cnts_p[0] if len(cnts_p) == 2 else cnts_p[1]

    cnts_g = cv2.findContours(mask_g, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_g = cnts_g[0] if len(cnts_g) == 2 else cnts_g[1]


    if cnts_y != None:
        for c in cnts_y:
            x, y, w, h = cv2.boundingRect(c)
            if (w > 10):
                if (convex_hull_pointing_up(c)):
                    distance = (407 / h) * 2
                    if (distance_from_robot > distance):
                        current_obj = c
                        distance_from_robot = distance
                        height = h
                        x_pos = x

    if (cnts_p != None):
        for c in cnts_p:
            x, y, w, h = cv2.boundingRect(c)
            if (w > 62.5):
                distance = (635 / h) * 2
                if (distance_from_robot > distance):
                    current_obj = c
                    distance_from_robot = distance
                    height = h
                    x_pos = x

    if cnts_g != None:
        for c in cnts_g:
            x, y, w, h = cv2.boundingRect(c)
            if w > 20:
                distance = (110/w) *2
                if distance_from_robot > distance:
                    width = w
                    current_obj = c
                    height = h
                    x_pos = x

    try:
        if (type(current_obj) != None):
            x, y, w, h = cv2.boundingRect(current_obj)
            cv2.rectangle(original, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.circle(original, (x + int(w / 2), y + int(h / 2)), 20, (36, 255, 12), 2)
        else:
            distance_from_robot = 69420
            x_pos = 0
            height=0

    except:
        continue


    print(f"distance is {distance}", f" and Pixel width is {width}")
    print(f"Horizontal distance (px): {x_pos-360}")

    cv2.imshow("in_range", original)
    #cv2.imshow("Yellow Video", mask_y)
    #cv2.imshow("Purple Video", mask_p)
    cv2.imshow("Green Video", mask_g)
    cv2.waitKey(1)
    current_obj = None



