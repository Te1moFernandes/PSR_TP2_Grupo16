#!/usr/bin/python3
# import the opencv library
import cv2
import json
import sys
from colorama import *


def find_centroid(th):
    ret=False
    contours, hierarchy = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cX=0
    cY=0
    connectivity = 4  
    output = cv2.connectedComponentsWithStats(th, connectivity, cv2.CV_32S)
    max_area=-1
    index=None
    print(output[0])
    if output[0]<=1:
        return ret, None, None
    for i in range(1,output[0]):
        if output[2][i,cv2.CC_STAT_AREA]>max_area:
            index=i
            max_area=output[2][i,cv2.CC_STAT_AREA]
            ret=True
    return ret, output[3][index][0], output[3][index][1]


def limit_image(B, G, R):
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
    final_thresh = cv2.bitwise_and(final_thresh, thresh_red)
    cv2.imshow('image', final_thresh)
    return final_thresh

def segment(data, windowname, frame):



    # Capture the video frame by frame
    B=frame[:,:,0]
    G=frame[:,:,1]
    R=frame[:,:,2]
    img_w_thresh = limit_image(B, G, R)
    ret, cX, cY = find_centroid(img_w_thresh)
    # Display the resulting frame
    return ret, cX, cY


