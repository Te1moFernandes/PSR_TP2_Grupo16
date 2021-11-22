#!/usr/bin/python3
# import the opencv library
import cv2
import json
import sys
from colorama import *
# define a video capture object

#callback para as trackbars


def limit_image(B, G, R, final_threshred=None):
    _, thresh1 = cv2.threshold(B, cv2.getTrackbarPos('Blue_max', 'frame'), 255, cv2.THRESH_BINARY_INV)
    _, thresh2 = cv2.threshold(B, cv2.getTrackbarPos('Blue_min', 'frame'), 255, cv2.THRESH_BINARY)
    _, thresh3 = cv2.threshold(G, cv2.getTrackbarPos('Red_max', 'frame'), 255, cv2.THRESH_BINARY_INV)
    _, thresh4 = cv2.threshold(G, cv2.getTrackbarPos('Red_min', 'frame'), 255, cv2.THRESH_BINARY)
    _, thresh5 = cv2.threshold(R, cv2.getTrackbarPos('Green_max', 'frame'), 255, cv2.THRESH_BINARY_INV)
    _, thresh6 = cv2.threshold(R, cv2.getTrackbarPos('Green_min', 'frame'), 255, cv2.THRESH_BINARY)

    thresh_blue = cv2.bitwise_and(thresh1, thresh2)
    thresh_red = cv2.bitwise_and(thresh3, thresh4)
    thresh_green = cv2.bitwise_and(thresh5, thresh6)
    final_thresh = cv2.bitwise_and(thresh_blue, thresh_green)
    cv2.imshow('image_blue', thresh_blue)
    cv2.imshow('image_green', thresh_green)
    cv2.imshow('image_red', thresh_red)
    final_thresh = cv2.bitwise_and(final_thresh, thresh_red)
    cv2.imshow('image', final_thresh)
    return final_thresh

def segment(data, windowname, frame):



    # Capture the video frame by frame
    (B, G, R) = cv2.split(frame)
    img_w_thresh = limit_image(B, G, R)
    # Display the resulting frame
    return img_w_thresh


