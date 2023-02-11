import cv2
import numpy as np
from matplotlib import pyplot as plt

# Variables

cone_width_reference = 90 #  90 pixel width at 6 ft

# reading image
# vid = cv2.VideoCapture(0)



while True:
    frame = cv2.imread("cone_test.jpg")

    # Transform the image to HSV and Detect yellow
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    img_thresh_low = cv2.inRange(hsv_frame, np.array([25, 50, 100]), # (25,25,199)
                                 np.array([60,255, 255]))  #everything that is included in the "left red"
    img_thresh_high = cv2.inRange(hsv_frame, np.array([159, 135, 135]), # (159, 135, 135
                                  np.array([179, 255, 255]))

    # everything that is included in the "right yellow"
    img_thresh = cv2.bitwise_or(img_thresh_low, img_thresh_high)


    kernel = np.ones((5, 5))
    img_thresh_opened = cv2.morphologyEx(img_thresh, cv2.MORPH_OPEN, kernel)
    img_thresh_blurred = cv2.medianBlur(img_thresh_opened, 5)
    img_edges = cv2.Canny(img_thresh_blurred, 80, 160)


    # Contours

    #contours, _ = cv2.findContours(img_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Select a contour
    #cnt = contours[0]

    # Approximate the contour using cv2.approxPolyDP
    #epsilon = 0.1 * cv2.arcLength(cnt, True)
    #approx = cv2.approxPolyDP(cnt, epsilon, True)
    #cv2.drawContours(img_thresh_blurred, [approx], 0, (0, 255, 0), 2)

    """
    for c in contours[0]:
        epsilon = 0.1 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)
        approx_contours.append(approx)
    """

    """
    all_convex_hulls = []
    for ac in approx_contours:
        all_convex_hulls.append(cv2.convexHull(ac))
    """

    cv2.imshow("edges", img_edges)
    cv2.imshow("iN_rnage", img_thresh_blurred)
    cv2.imshow("video", frame)
    cv2.waitKey(1)

