import cv2
import numpy as np
import math
from cscore import CameraServer, VideoSource, UsbCamera, MjpegServer
from ntcore import NetworkTableInstance, EventFlags
import time

# Network Tables
ntinst = NetworkTableInstance.getDefault()
ntinst.startServer()
table = ntinst.getTable("Vision")
time.sleep(0.5)

CameraServer.startAutomaticCapture()
input_stream = CameraServer.getVideo()
print(input_stream.getDescription())
output_stream = CameraServer.putVideo('Processed', 160, 120)

# Variables
cone_width_reference = 90 # 90 pixel width at 6 ft
angle_per_pixels = 60/160


# reading image
#vid = cv2.VideoCapture(0)
#(hMin = 19 , sMin = 108, vMin = 71), (hMax = 30 , sMax = 255, vMax = 255)


lower_y = np.array([14, 163, 109], dtype="uint8") # 22, 151, 71
upper_y = np.array([30, 255, 255], dtype="uint8") # 28, 255, 255

lower_p = np.array([117, 75, 75], dtype="uint8")  # 110, 141, 47
upper_p = np.array([126, 255, 250], dtype="uint8")  # 130, 255, 255

lower_g = np.array([0, 0, 255], dtype="uint8")  # 0, 0, 255
upper_g = np.array([0, 255, 254], dtype="uint8")  # 0, 255, 255

img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)

time.sleep(0.5)


def convex_hull_pointing_up(ch):
    points_above_center, points_below_center = [], []

    x, y, w, h = cv2.boundingRect(ch)
    aspect_ratio = w / h

    if aspect_ratio < 0.9:  # 0.8
        vertical_center = y + h / 2

        for point in ch:
            if point[0][1] < vertical_center:
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
    # Reset variables
    distance_from_robot = 69420
    angle = 0
    x_pos = 0
    distance = 0
    current_obj = None

    # Start time
    start_time = time.time()
    frame_time, input_img = input_stream.grabFrame(img)


    if frame_time == 0:
        output_stream.notifyError(input_stream.getError())
        continue

    output_img = np.copy(input_img)
    frame = input_img

    original = frame.copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Masks
    mask_y = cv2.inRange(frame, lower_y, upper_y)
    mask_p = cv2.inRange(frame, lower_p, upper_p)
    mask_g = cv2.inRange(frame, lower_g, upper_g)

    mask_y = cv2.medianBlur(mask_y, 5)
    mask_p = cv2.medianBlur(mask_p, 5)
    mask_g = cv2.medianBlur(mask_g, 5)
    # Contours
    cnts_y = cv2.findContours(mask_y, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_y = cnts_y[0] if len(cnts_y) == 2 else cnts_y[1]

    cnts_p = cv2.findContours(mask_p, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_p = cnts_p[0] if len(cnts_p) == 2 else cnts_p[1]

    cnts_g = cv2.findContours(mask_g, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_g = cnts_g[0] if len(cnts_g) == 2 else cnts_g[1]

    # Contour detection
    if cnts_y != None:
        for c in cnts_y:
            x, y, w, h = cv2.boundingRect(c)
            if cv2.contourArea(c) < 0:
                continue
            else:
                if (convex_hull_pointing_up(c)):
                    distance = (69 / h) * 3
                    if (distance_from_robot > distance):
                        current_obj = c
                        distance_from_robot = distance
                        height = h
                        x_pos = x + (w / 2)

    if (cnts_p != None):
        for c in cnts_p:
            x, y, w, h = cv2.boundingRect(c)
            if cv2.contourArea(c) < 15:
                continue
            else:
                distance = (635 / h) * 2
                if (distance_from_robot > distance):
                    current_obj = c
                    distance_from_robot = distance
                    height = h
                    x_pos = x + (w/2)

    if cnts_g != None:
        for c in cnts_g:
            x, y, w, h = cv2.boundingRect(c)
            if cv2.contourArea(c) < 15:
                continue
            else:
                distance = (110/w) * 2
                if distance_from_robot > distance:
                    width = w
                    current_obj = c
                    height = h
                    x_pos = x + (w/2) - 320



    try:
        if (type(current_obj) != None):
            x, y, w, h = cv2.boundingRect(current_obj)
            cv2.rectangle(original, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.circle(original, (x + int(w / 2), y + int(h / 2)), 2, (36, 255, 12), 2)
            table.putNumber("Distance", distance)
    except:
        continue

    processing_time = time.time() - start_time
    fps = 1 / processing_time

    cv2.line(original, (80, 0), (80, 120), (255, 0, 0), 2)
    output_stream.putFrame(original)

    print("Pixel Height: " )

    # Networktable values
    table.putNumber("Angle", angle_per_pixels * x_pos - 30)
    table.putNumber("FPS",fps)

    #cv2.imshow("video", mask_y)
    #cv2.waitKey(1)
    current_obj = None



