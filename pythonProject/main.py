import cv2
import numpy as np
import threading
from networktables import NetworkTables, NetworkTablesInstance

cond = threading.Condition()
notified = [False]

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()


NetworkTables.initialize(server='10.11.24.2')
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

with cond:
    print("Waiting")
    if not notified[0]:
        cond.wait()

table = NetworkTables.getTable('SmartDashboard')

# Insert your processing code here
print("Connected!")

# Get the camera stream
cam_id = 0
x = 0
vid = cv2.VideoCapture(cam_id)

yellow_lower_threshold = np.array([30, 70, 70]) # 60, 125, 110
yellow_higher_threshold = np.array([100, 255, 255]) #100, 225, 255]

purple_higher_threshold = np.array([170, 255, 255]) # 179, 255, 255
purple_lower_threshold = np.array([115, 100, 90]) # 105, 125, 120

green_lower_threshold = np.array([60, 90, 90])
green_higher_threshold = np.array([110, 255, 255])



while(True):
    _, frame = vid.read()
    x += 1

    if x == 2: # Process frame every 5 frames
        # Convert image to HSV format
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Detect the colors
        purple_frame_inrange = cv2.inRange(hsv_frame, purple_lower_threshold, purple_higher_threshold)
        yellow_frame_inrange = cv2.inRange(hsv_frame, yellow_lower_threshold, yellow_higher_threshold)
        green_frame_inrange = cv2.inRange(hsv_frame, green_lower_threshold, green_higher_threshold)

        # Get the edges of the colors
        p_contours, hiearchy = cv2.findContours(purple_frame_inrange, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        g_contours, hiearchy = cv2.findContours(green_frame_inrange, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(frame, g_contours, -1, (255, 255, 255), 2)

        # Stream the images
        #cv2.imshow("processed_purple", green_frame_inrange)
        #cv2.imshow("processed_yellow", yellow_frame_inrange)
        x = 0

    green = np.uint8([[[0, 255, 0]]])
    print(cv2.cvtColor(green, cv2.COLOR_BGR2HSV))

    table.putNumberArray("camera", frame)
    cv2.waitKey(1)
